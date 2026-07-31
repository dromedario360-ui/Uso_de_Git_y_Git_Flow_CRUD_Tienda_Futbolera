from abc import ABC, abstractmethod


class IPagoGateway(ABC):
    """Contrato del componente 'Pasarela de Pago'. Cualquier proveedor de
    pagos (Stripe, PayPal, Azul, etc.) debe implementar este metodo."""

    @abstractmethod
    def procesar_pago(self, monto: float) -> bool:
        pass
