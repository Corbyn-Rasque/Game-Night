from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text
from fastapi.responses import JSONResponse
from src import database as db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(auth.get_api_key)],
)

# In the current state, contributions cannot be made unless already requested (foreign key violation otherwise).
# Consider how we might want to handle this (allow / disallow based on event & table logic?)


class Item(BaseModel):
    name: str
    type: str
    quantity: int
    cost: int

# Insert item requests for an event, or update if it's been added
@router.post("/{event_id}/request")
def request_new_item(event_id: int, item: Item):
    request = text('''INSERT INTO event_items (event_id, name, type, requested, cost)
                      VALUES (:event_id, :name, :type, :quantity, :cost)''')
    
    try:
        with db.engine.begin() as connection:
            connection.execute(request, dict(item) | {'event_id': event_id})
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Item requested successfully")




# Get contributions overall, grouped by item
@router.get("/{event_id}/request")
def get_current_contributions(event_id: int):

    get_contributions = text('''
                            with item_quantity as (
                            SELECT event_id, item_name, 
                            SUM(quantity)::int AS total, 
                            SUM(payment)::int AS payments
                            FROM item_contributions
                            GROUP BY event_id, item_name)

                            SELECT name, type, requested, COALESCE(total,0) as Total, 
                            COALESCE(payments,0) as Payments FROM event_items
                            LEFT JOIN item_quantity ON item_quantity.event_id = event_items.event_id 
                            AND item_quantity.item_name= event_items.name
                            WHERE (event_items.event_id, deleted) IN ((:event_id, FALSE))''')
    
    try:
        with db.engine.begin() as connection:
            contributions = connection.execute(get_contributions, {'event_id': event_id}).mappings().all()
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
    
    return contributions

class delete_items(BaseModel):
    name: str

@router.delete("/{event_id}/request")
def remove_item_request(event_id: int, to_delete: list[delete_items]):

    items_to_delete = []
    for item in to_delete:
        items_to_delete.append(
            {'name': item.name,
            'event_id': event_id})

    remove_contributions = text('''
                                DELETE FROM item_contributions
                                WHERE event_id = :event_id AND
                                item_name = :name; 

                                DELETE FROM event_items
                                WHERE event_id = :event_id AND
                                name = :name;  ''')
    
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_contributions, items_to_delete)
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
    
    print("ITEM REQUEST DELETE:")
    print(items_to_delete)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


# Get contributions from a single user
@router.get("/{event_id}/{username}")
def user_contributions(event_id: int, username: str):
    get_contributions = text('''SELECT item_name, SUM(quantity) AS total, SUM(payment) AS payment
                                FROM item_contributions
                                WHERE (event_id, username, deleted) IN ((:event_id, :username, FALSE))
                                GROUP BY item_name''')
    try:
        with db.engine.begin() as connection:
            contributions = connection.execute(get_contributions, {'event_id': event_id, 'username': username}).mappings().all()
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
    
    return contributions


class contribution(BaseModel):
    item_name: str
    quantity: int

# Allows users to make a contribution 
@router.post("/{event_id}/{username}")
def contribute_item(event_id: int, username: str, item: contribution):

    with db.engine.begin() as connection:

        check = text('''SELECT TRUE as bool FROM event_items 
                        WHERE name = :name AND event_id = :id ''')
        check_params = {"name": item.item_name, "id" : event_id}
        requested = connection.execute(check, check_params).fetchone()

        if not requested:
            raise HTTPException(status_code=404, detail=f"{item.item_name} is not currently requested for this event")
        
        contribute = text('''WITH item_cost AS (
                    SELECT cost FROM event_items
                    WHERE event_id = 40 AND name = :item_name
                    )
                    INSERT INTO item_contributions (event_id, username, item_name, quantity, payment)
                    SELECT :event_id, :username, :item_name, :quantity, cost * :quantity
                    FROM item_cost
                    ON CONFLICT (event_id, username, item_name) DO NOTHING;''')        
        
        try:
            connection.execute(contribute, dict(item) | {'event_id': event_id, 'username': username})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
        
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Item added to contributions successfully")




class Updated_Item(BaseModel):
    item_name: str
    new_quantity: int

@router.patch("/{event_id}/{username}")
def update_item_contribuition(event_id: int, username: str, item: Updated_Item):

    with db.engine.begin() as connection:
        
        #This can be deleted if it causes concurrency issues
        check = text('''SELECT TRUE as bool FROM item_contributions 
                        WHERE username = :username AND item_name = :name 
                        AND event_id = :id ''')
        
        check_params = {"username": username, "name" : item.item_name, "id": event_id}
        request = connection.execute(check, check_params).fetchone()

        if not request:
            raise HTTPException(status_code=404, detail="contribuition not found")
        
        update = text('''UPDATE item_contributions
            SET 
                quantity = new_info.quantity,
                payment = new_info.payment
            FROM (
                SELECT 
                    :quantity as quantity,
                    cost * :quantity as payment
                FROM event_items
                WHERE event_items.event_id = :id AND event_items.name = :name
            ) as new_info
            WHERE item_contributions.event_id = :id AND item_contributions.username = :username
            ''')
                      
        update_params = {"username": username, "name" : item.item_name, "id": event_id, "quantity": item.new_quantity}
        try:
            connection.execute(update, update_params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
            
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{event_id}/{username}")
def remove_user_contributions(event_id: int, username: str, to_delete: list[delete_items]):
    items_to_delete = []
    for item in to_delete:
        items_to_delete.append(
            {'name': item.name,
            'event_id': event_id,
            'username': username})
        
    remove_contributions = text('''
                                DELETE FROM item_contributions
                                WHERE (event_id, username, item_name) IN ((:event_id, :username, :name))
                                ''')
    try:
        with db.engine.begin() as connection:
            connection.execute(remove_contributions, items_to_delete)
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating the contribution: {str(e)}")
    
    print("ITEM CONTRIBUTIONS DELETE:")
    print(items_to_delete)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
