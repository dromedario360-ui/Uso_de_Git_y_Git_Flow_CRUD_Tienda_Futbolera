from repositories.pago_gateway import IPagoGateway


class PagoGatewaySimulado(IPagoGateway):
    """Implementacion de prueba. En un sistema real aqui se conectaria
    con un proveedor de pagos externo."""

    def procesar_pago(self, monto: float) -> bool:
        if monto <= 0:
            return False
        return True
