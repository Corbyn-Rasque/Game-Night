from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth
from sqlalchemy import text, exc
from fastapi.responses import JSONResponse
from src import database as db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(auth.get_api_key)],
)


class Item(BaseModel):
    name: str
    type: str
    quantity: int
    cost: int


@router.post("/{event_id}/request", status_code = status.HTTP_201_CREATED)
def request_new_item(event_id: int, item: Item):
    request =    '''INSERT INTO event_items (event_id, name, type, requested, cost)
                    VALUES (:event_id, :name, :type, :quantity, :cost)
                    ON CONFLICT (event_id, name)
                    DO UPDATE SET type = EXCLUDED.type,
                                  requested = EXCLUDED.requested,
                                  cost = EXCLUDED.cost
                    RETURNING event_id, name'''
    
    with db.engine.begin() as connection:
        try:
            connection.execute(text(request), dict(item) | {'event_id': event_id}).one()
        except exc.IntegrityError as e:
            error = str(e.orig)

            if 'name' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Name cannot be default.')
            elif 'type' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Type cannot be default.')
            elif 'quantity' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Quantity must be one or more.')
            elif 'cost' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Cost must be zero or more.')

        except exc.NoResultFound:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = 'Error adding requested item.')



@router.get("/{event_id}/requests", status_code = status.HTTP_200_OK)
def get_current_contributions(event_id: int):
    get_contributions = '''with item_quantity as  (SELECT event_id, item_name, 
                                                    SUM(quantity)::int AS total, 
                                                    SUM(payment)::int AS payments
                                                    FROM item_contributions
                                                    GROUP BY event_id, item_name)

                            SELECT  name, type, requested, COALESCE(total ,0) AS Total, 
                                    COALESCE(payments, 0) AS Payments
                            FROM event_items
                            LEFT JOIN item_quantity ON item_quantity.event_id = event_items.event_id 
                                AND item_quantity.item_name= event_items.name
                            WHERE (event_items.event_id, deleted) IN ((:event_id, FALSE))'''
    
    with db.engine.begin() as connection:
        contributions = connection.execute(text(get_contributions), {'event_id': event_id}).mappings().all()

        if not contributions: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No requests found for event.')
        else: return contributions


@router.delete("/{event_id}/request", status_code = status.HTTP_204_NO_CONTENT)
def remove_item_request(event_id: int, name: str):
    remove = '''DELETE FROM event_items
                WHERE event_id = :event_id AND name = :name'''
    
    with db.engine.being() as connection:
        result = connection.execute(text(remove), {'event_id': event_id, 'name': name})

        if not result.rowcount:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Event ID or Item doesn\'t exist')


@router.get("/{event_id}/{username}", status_code = status.HTTP_200_OK)
def user_contributions(event_id: int, username: str):
    get_contributions =  '''SELECT item_name, SUM(quantity) AS total, SUM(payment) AS payment
                            FROM item_contributions
                            WHERE (event_id, username, deleted) IN ((:event_id, :username, FALSE))
                            GROUP BY item_name'''
    
    with db.engine.begin() as connection:
        contributions = connection.execute(text(get_contributions), {'event_id': event_id, 'username': username}).mappings().all()
    
        if not contributions: raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'No contributions found for user.')
        else: return contributions


@router.post("/{event_id}/{username}", status_code = status.HTTP_201_CREATED)
def contribute_item(event_id: int, username: str, item: Item):
    add_item =   '''WITH item_cost AS  (SELECT cost
                                        FROM event_items
                                        WHERE event_id = :event_id AND name = :name)
                    INSERT INTO item_contributions (event_id, username, item_name, quantity, payment)
                    SELECT :event_id, :username, :name, :quantity, cost * :quantity AS payemnt
                    FROM item_cost
                    WHERE (:event_id, :name) IN (SELECT event_id, name FROM event_items WHERE NOT deleted)
                    ON CONFLICT (event_id, username, item_name)
                    DO UPDATE SET quantity = :quantity,
                                  payment = (SELECT cost
                                             FROM event_items
                                             WHERE event_id = :event_id AND name = :name) * :quantity'''
    
    with db.engine.begin() as connection:
        try: 
            result = connection.execute(text(add_item), dict(item) | {'event_id': event_id, 'username': username})

            if not result.rowcount: raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Unable to add item.')
        
        except exc.IntegrityError as e:
            error = str(e.orig)

            if 'quantity' in error:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Quantity must be one or more.')


@router.patch("/{event_id}/{username}", status_code = status.HTTP_204_NO_CONTENT)
def remove_user_contributions(event_id: int, username: str, item_name: str):
    remove_item =    '''UPDATE item_contributions
                        SET delete = TRUE
                        WHERE event_id = :event_id,
                              username = :username,
                              item_name = :item_name'''
    
    with db.engine.begin() as connection:
        result = connection.execute(text(remove_item), {'event_id': event_id, 'username': username, 'item_name': item_name})

        if not result.rowcount: raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'No matching contribution found.')