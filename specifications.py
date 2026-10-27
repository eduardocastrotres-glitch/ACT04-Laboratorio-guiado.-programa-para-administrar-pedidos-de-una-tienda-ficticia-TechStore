from abc import ABC, abstractmethod
from decimal import Decimal
from .domain import Order


class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, order: Order) -> bool:
        """Determina si la orden cumple con la regla de negocio."""

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left, self.right = left, right

    def is_satisfied_by(self, order: Order) -> bool:
        return self.left.is_satisfied_by(order) and self.right.is_satisfied_by(order)


class OrSpecification(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left, self.right = left, right

    def is_satisfied_by(self, order: Order) -> bool:
        return self.left.is_satisfied_by(order) or self.right.is_satisfied_by(order)


class NotSpecification(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, order: Order) -> bool:
        return not self.spec.is_satisfied_by(order)


# --- Reglas de negocio específicas ---

class MinimumAmountSpec(Specification):
    """Total ESTRICTAMENTE mayor al umbral."""
    def __init__(self, threshold):
        self.threshold = Decimal(str(threshold))

    def is_satisfied_by(self, order: Order) -> bool:
        return order.total.amount > self.threshold


class VIPCustomerSpec(Specification):
    def is_satisfied_by(self, order: Order) -> bool:
        return order.customer.is_vip and order.customer.active


class MinimumUnitsSpec(Specification):
    def __init__(self, min_units: int):
        self.min_units = min_units

    def is_satisfied_by(self, order: Order) -> bool:
        return order.units >= self.min_units


class ActivePromotionSpec(Specification):
    def is_satisfied_by(self, order: Order) -> bool:
        return order.has_promotion


# 10%: VIP AND monto > 500 AND unidades >= 4 AND NOT promoción
class TenPercentDiscountSpec(Specification):
    def __init__(self):
        self.rule = (VIPCustomerSpec()
                     & MinimumAmountSpec(500)
                     & MinimumUnitsSpec(4)
                     & ~ActivePromotionSpec())

    def is_satisfied_by(self, order: Order) -> bool:
        return self.rule.is_satisfied_by(order)


# 5%: monto > 5000 AND NOT promoción
class FivePercentDiscountSpec(Specification):
    def __init__(self):
        self.rule = MinimumAmountSpec(5000) & ~ActivePromotionSpec()

    def is_satisfied_by(self, order: Order) -> bool:
        return self.rule.is_satisfied_by(order)


def discount_for(order: Order) -> int:
    """Porcentaje de descuento aplicable (el de 10% tiene prioridad)."""
    if TenPercentDiscountSpec().is_satisfied_by(order):
        return 10
    if FivePercentDiscountSpec().is_satisfied_by(order):
        return 5
    return 0
