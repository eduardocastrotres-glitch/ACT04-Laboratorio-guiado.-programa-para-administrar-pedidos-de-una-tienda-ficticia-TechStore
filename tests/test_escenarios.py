from .cargar_csv import load_fixture, load_prices
from .domain import DomainException, OrderItem, Money
from .specifications import discount_for


def _intenta(fn):
    """Devuelve 'exito' o 'rechazo' según si el dominio lanza excepción."""
    try:
        fn()
        return "exito"
    except DomainException:
        return "rechazo"


def _ciclo(o, *pasos):
    for paso in pasos:
        paso()


def escenarios():
    precios = load_prices()
    o = load_fixture()
    yield "E01", f"{discount_for(o['O001'])}%", "10%"
    yield "E02", f"{discount_for(o['O002'])}%", "0%"
    yield "E03", _intenta(o["O003"].confirm), "rechazo"
    yield "E04", f"{discount_for(o['O005'])}%", "0%"
    yield "E05", f"{discount_for(o['O006'])}%", "5%"
    yield "E06", _intenta(o["O007"].confirm), "rechazo"
    yield "E07", _intenta(o["O008"].confirm), "exito"
    yield "E08", _intenta(lambda: o["O009"].add_item(
        OrderItem("SKU003", 2, Money(precios["SKU003"])))), "rechazo"
    yield "E09", f"{discount_for(o['O010'])}%", "0%"
    yield "E10", f"{discount_for(o['O011'])}%", "0%"

    p = o["O012"]; p.confirm()
    yield "E11", _intenta(p.ship), "rechazo"          # sin guía

    p = o["O013"]; p.confirm()
    yield "E12", _intenta(p.confirm), "rechazo"       # segunda confirmación

    p = o["O014"]; p.confirm(); p.ship("GUIA-1")
    yield "E13", _intenta(p.cancel), "rechazo"        # cancelar desde SHIPPED

    p = o["O015"]; p.confirm(); p.ship("GUIA-2"); p.return_order()
    yield "E14", p.status.value, "RETURNED"

    p = o["O016"]; p.confirm(); p.ship("GUIA-3"); p.deliver()
    yield "E15", p.status.value, "DELIVERED"


def test_escenarios():
    print("--- Evaluando reglas de negocio en escenarios ---")
    fallos = 0
    for caso, obtenido, esperado in escenarios():
        ok = obtenido == esperado
        fallos += not ok
        estado = "OK  " if ok else "FALLA"
        # Usamos formato con sangría fija y alineación en columnas
        print(f"  {caso}: [{estado}]   ->   Obtenido: {obtenido:<10} | Esperado: {esperado}")
    
    print(f"\nResultado final: {15 - fallos}/15 escenarios correctos")


if __name__ == "__main__":
    test_escenarios()
