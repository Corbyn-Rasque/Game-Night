from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from src import database as db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(auth.get_api_key)],
)

# In the current state, contributions cannot be made unless already requested (foreign key violation otherwise).
# Consider how we might want to handle this (allow / disallow based on event & table logic?)

# Should deletion of users items happen separately in the Users endpoint? URL setup doesn't lend well to deleting
# by items here.

class Item(BaseModel):
    name: str
    type: str
    quantity: int
    payment: int

# Insert item requests for an event, or update if it's been added
@router.post("/{event_id}/requests", status_code=200)
def request_item(event_id: int, item: Item):
    request = text('''INSERT INTO event_items (event_id, name, type, requested, cost)
                      VALUES (:event_id, :name, :type, :quantity, :payment)
                      ON CONFLICT (event_id, name)
                      DO UPDATE SET (type, requested, cost) = (EXCLUDED.type, EXCLUDED.requested, EXCLUDED.cost)''') 
    try:
        with db.engine.begin() as connection:
            connection.execute(request, dict(item) | {'event_id': event_id})
            return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error inserting item")

# Insert an individual contribution, or update if it's been added
@router.post("/{event_id}/contributions/user/{username}")
def contribute_item(event_id: int, username: str, item: Item):
    check_item_exists = text('''SELECT TRUE
                                FROM event_items
                                WHERE (event_id, name) IN ((:event_id, :name))''')

    contribute = text('''INSERT INTO items_ledger (event_id, username, item_name, quantity, payment)
                         VALUES (:event_id, :username, :name, :quantity, :payment)
                         ON CONFLICT (event_id, username, item_name)
                         DO UPDATE SET (quantity, payment) = (EXCLUDED.quantity, EXCLUDED.payment)''')
    try:
        with db.engine.begin() as connection:
            if not connection.execute(check_item_exists, dict(item) | {'event_id': event_id, 'username': username}).scalar_one_or_none():
                request_item(event_id, item)

            connection.execute(contribute, dict(item) | {'event_id': event_id, 'username': username})
        return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400, detail="Error adding contributed item")

# Get contributions overall, grouped by item
@router.get("/{event_id}/contributions/")
def contributions(event_id: int):
    get_contributions = text('''SELECT item_name, SUM(quantity)::INTEGER AS total, SUM(payment)::INTEGER AS contribution
                                FROM items_ledger
                                WHERE (event_id, deleted) IN ((:event_id, FALSE))
                                GROUP BY item_name''')
    
    try:
        with db.engine.begin() as connection:
            contributions = connection.execute(get_contributions, {'event_id': event_id}).mappings().all()
        return contributions
    except Exception:
        raise HTTPException(status_code=400,detail="Error retrieving contributions")

# Get contributions from a single user
@router.get("/{event_id}/contributions/{username}")
def user_contribution(event_id: int, username: str):
    get_contributions = text('''SELECT item_name, SUM(quantity)::INTEGER AS total, SUM(payment)::INTEGER AS contribution
                                FROM items_ledger
                                WHERE (event_id, username, deleted) IN ((:event_id, :username, FALSE))
                                GROUP BY item_name''')
    try:
        with db.engine.begin() as connection:
            contributions = connection.execute(get_contributions, {'event_id': event_id, 'username': username}).mappings().all()
        return contributions
    except Exception:
        raise HTTPException(status_code=400, detail="Error retrieving contributions")

@router.patch("/{event_id}/requests/{item_name}")
def remove_request(event_id: int, item_name: str):
    remove_request = text('''UPDATE event_items
                             SET deleted = TRUE
                             WHERE (event_id, name) IN ((:event_id, :item_name))''')
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_request, {'event_id': event_id, 'item_name': item_name})
        return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error removing item request")

# Delete single item contribution by an individual
@router.patch("/{event_id}/contributions/{username}/{item_name}")
def remove_user_contribution(event_id: int, username: str, item_name: str):
    remove_contributions = text('''UPDATE items_ledger
                                   SET deleted = TRUE
                                   WHERE (event_id, username, item_name) IN ((:event_id, :username, :item_name))''')
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_contributions, {'event_id': event_id, 'username': username, 'item_name': item_name})
        return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error while removing items")

# Delete all contributions by an individual
@router.patch("/{event_id}/contributions/{username}")
def remove_user_contributions(event_id: int, username: str):
    remove_contributions = text('''UPDATE items_ledger
                                   SET deleted = TRUE
                                   WHERE (event_id, username) IN ((:event_id, :username))''')
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_contributions, {'event_id': event_id, 'username': username})
        return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400,detail="Unexpected error while removing items")

# Delete all event contributions
@router.delete("/{event_id}/contributions")
def remove_all_event_contributions(event_id: int):
    remove_contributions = text('''UPDATE items_ledger
                                   SET deleted = TRUE
                                   WHERE event_id = :event_id''')
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_contributions, {'event_id': event_id})
        return {"status" : "ok"}
    except Exception:
        raise HTTPException(status_code=400, detail="Unexpected error while removing event contributions")