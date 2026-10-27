import pytest

from .domain import Order, Customer, Money

def test_creacion_pedido_valido():
    cliente = Customer(id="C001")
    ...

def test_transicion_estado_invalida():
    cliente = Customer(id="C002")
    orden = Order(customer=cliente, id="ORD-002", has_promotion=False)
    ...