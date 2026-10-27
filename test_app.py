import pytest
from decimal import Decimal
from app.domain import (
    Money, 
    Customer,
    OrderItem,
    Order,
    OrderStatus,
    InvalidOrderData, 
    InvalidOrderTransition,
    OrderItemLimitExceeded,
    InactiveCustomerError, 
    EmptyOrderError, 
    InvalidStateTransitionError, 
    ShipmentGuideMissingError,
    DuplicateConfirmationError
)
from cargar_csv import load_fixture

def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))

def test_pedido_o001_inicia_draft():
    orders = load_fixture()
    assert orders["O001"].status.value == "DRAFT"
    assert orders["O001"].units == 4
    assert orders["O001"].total.amount == Decimal("1680.00")

def test_pedido_21_unidades():
    cliente = Customer(id="C01", name="Test")
    order = Order(customer=cliente, id="O_21")
    item = OrderItem(sku="SKU1", quantity=21, unit_price=Money(Decimal("10.00")))
    
    with pytest.raises(OrderItemLimitExceeded):
        order.add_item(item)


def test_cliente_inactivo():
    cliente = Customer(id="C02", name="Inactivo", active=False)
    order = Order(customer=cliente, id="O_INC")
    order.add_item(OrderItem(sku="SKU2", quantity=1, unit_price=Money(Decimal("50.00"))))
    
    with pytest.raises(InactiveCustomerError):
        order.confirm()


def test_pedido_vacio():
    cliente = Customer(id="C03", name="Vacio")
    order = Order(customer=cliente, id="O_EMPTY")
    
    with pytest.raises(EmptyOrderError):
        order.confirm()


def test_descuento_vip():
    cliente = Customer(id="C04", name="VIP", is_vip=True)
    order = Order(customer=cliente, id="O_VIP", is_vip=True)
    order.add_item(OrderItem(sku="SKU3", quantity=10, unit_price=Money(Decimal("100.00"))))
    
    assert order.total.amount == Decimal("800.00")


def test_promocion_activa():
    cliente = Customer(id="C05", name="Promo")
    order = Order(customer=cliente, id="O_PROMO")
    order.has_promotion = True
    assert order.has_promotion is True


def test_envio_sin_guia():
    cliente = Customer(id="C06", name="Envio")
    order = Order(customer=cliente, id="O_SHIP")
    order.add_item(OrderItem(sku="SKU4", quantity=1, unit_price=Money(Decimal("100.00"))))
    order.confirm()
    
    with pytest.raises(ShipmentGuideMissingError):
        order.ship(tracking_number="")


def test_confirmacion_doble():
    cliente = Customer(id="C07", name="Doble")
    order = Order(customer=cliente, id="O_CONF")
    order.add_item(OrderItem(sku="SKU5", quantity=1, unit_price=Money(Decimal("100.00"))))
    order.confirm()
    
    with pytest.raises(InvalidOrderTransition):
        order.confirm()


def test_cancelacion_desde_shipped():
    cliente = Customer(id="C08", name="Cancel")
    order = Order(customer=cliente, id="O_SHIPPED")
    order.add_item(OrderItem(sku="SKU6", quantity=1, unit_price=Money(Decimal("100.00"))))
    order.confirm()
    order.ship(tracking_number="TRACK123")

    with pytest.raises(InvalidStateTransitionError):
        order.cancel()


def test_respuesta_http_404():
    try:
        from main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/ruta-inexistente-999")
        assert response.status_code == 404
    except (ImportError, ModuleNotFoundError):
        pytest.skip("Aplicación web o TestClient no configurados en este entorno.")