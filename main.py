import flet as ft
from database.conexion import crear_base_datos
from repositories.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from repositories.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from repositories.pago_gateway_simulado import PagoGatewaySimulado
from repositories.autenticacion_repository_estatica import AutenticacionRepositoryEstatica
from services.producto_service import ProductoService
from services.carrito_service import CarritoService
from ui.vista_tienda import VistaTienda
from ui.vista_login import VistaLogin


def main(page: ft.Page):
    crear_base_datos()

    producto_repositorio = ProductoRepositorySQLAlchemy()
    pedido_repositorio = PedidoRepositorySQLAlchemy()
    pago_gateway = PagoGatewaySimulado()
    producto_service = ProductoService(producto_repositorio)
    carrito = CarritoService(producto_service, pedido_repositorio, pago_gateway)

    autenticacion_repositorio = AutenticacionRepositoryEstatica("Rey6611", "flotus1")

    page.title = "Tienda de Futbol - Cliente"
    page.scroll = ft.ScrollMode.AUTO

    def mostrar_tienda():
        page.controls.clear()
        vista_tienda = VistaTienda(page, producto_service, carrito)
        page.add(vista_tienda.construir())
        page.update()

    login = VistaLogin(page, autenticacion_repositorio, mostrar_tienda)
    page.add(login.construir())


ft.app(target=main, assets_dir="assets")
