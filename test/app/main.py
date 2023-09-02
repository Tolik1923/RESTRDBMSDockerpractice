from fastapi import FastAPI, HTTPException
import services

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ordering service"}

@app.get("/orders")
async def get_all_orders():
    orders = services.get_all_orders()
    return orders

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = services.get_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@app.post("/orders/")
async def create_new_order(order_data: dict):
    try:
        order_id = services.create_order(order_data)
        return {"message": "Order created successfully", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating order")
    
@app.put("/orders/{order_id}")
async def update_order(order_id: int, order_data: dict):
    updated_order_id = services.update_order_by_id(order_id, order_data)
    
    if not updated_order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated successfully", "order_id": updated_order_id}
    
@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    try:
        result = services.delete_order(order_id)
        if result:
            return {"message": f"Order with id {order_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleting order")
    
@app.get("/stats")
async def get_stats():
    stats = services.get_stats()
    return stats

@app.get("/orders/{order_id}/items")
async def get_order_items(order_id: int):
    items = services.get_order_items(order_id)
    return items

@app.get("/orders/{order_id}/items/{item_id}")
async def get_order_item(order_id: int, item_id: int):
    item = await services.get_order_item(order_id, item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    
    return item

@app.post("/orders/{order_id}/items") #time
async def add_item_to_order(order_id: int, item_data: dict):
    try:
        item_id = await services.add_item_to_order(order_id, item_data)
        return {"message": "Item added to order", "item_id": item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding item to order")
    
@app.put("/orders/{order_id}/items/{item_id}") 
async def update_order_item(order_id: int, item_id: int, item_data: dict):
    try:
        await services.update_order_item(order_id, item_id, item_data)
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating item")
    
@app.delete("/orders/{order_id}/items/{item_id}")
async def delete_order_item(order_id: int, item_id: int):
    try:
        await services.delete_order_item(order_id, item_id)
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error deleted item")