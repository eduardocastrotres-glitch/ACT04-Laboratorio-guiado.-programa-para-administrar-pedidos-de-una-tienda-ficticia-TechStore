from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

from app.domain import DomainException, InvalidOrderData, InvalidOrderTransition, OrderItemLimitExceeded, OrderStatus
from app.cargar_csv import load_fixture

app = FastAPI(title="TechStore API", version="1.0")

orders_db = load_fixture()

class ShipRequest(BaseModel):
    tracking_number: str

@app.get("/orders", summary="Listar todos los pedidos")
def get_orders():
    return [
        {
            "id": o.id,
            "customer_id": o.customer.id,
            "status": o.status.value,
            "units": o.units,
            "total": float(o.total.amount),
            "has_promotion": o.has_promotion
        }
        for o in orders_db.values()
    ]

@app.get("/orders/{order_id}", summary="Obtener detalle de un pedido")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    o = orders_db[order_id]
    return {
        "id": o.id,
        "customer_id": o.customer.id,
        "status": o.status.value,
        "units": o.units,
        "total": float(o.total.amount),
        "tracking_number": o.tracking_number,
        "items": [
            {"sku": item.sku, "quantity": item.quantity, "subtotal": float(item.subtotal.amount)}
            for item in o.items
        ],
        "events": o.events
    }

@app.post("/orders/{order_id}/confirm", summary="Confirmar un pedido")
def confirm_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    o = orders_db[order_id]
    try:
        o.confirm()
        return {"message": f"Pedido {order_id} confirmado con éxito", "status": o.status.value}
    except InvalidOrderTransition as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidOrderData as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/orders/{order_id}/ship", summary="Enviar un pedido")
def ship_order(order_id: str, body: ShipRequest):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    o = orders_db[order_id]
    try:
        o.ship(body.tracking_number)
        return {"message": f"Pedido {order_id} enviado", "tracking_number": o.tracking_number, "status": o.status.value}
    except InvalidOrderTransition as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidOrderData as e:
        raise HTTPException(status_code=422, detail=str(e))
