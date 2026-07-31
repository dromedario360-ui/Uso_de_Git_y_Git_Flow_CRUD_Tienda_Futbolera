import flet as ft
from database.conexion import crear_base_datos
from repositories.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from repositories.autenticacion_repository_estatica import AutenticacionRepositoryEstatica
from services.producto_service import ProductoService
from ui.vista_principal import VistaPrincipal
from ui.vista_login import VistaLogin


def main(page: ft.Page):
    crear_base_datos()

    producto_repositorio = ProductoRepositorySQLAlchemy()
    producto_service = ProductoService(producto_repositorio)

    autenticacion_repositorio = AutenticacionRepositoryEstatica("GEM3322", "flotus1")

    page.title = "Panel de Administrador"
    page.scroll = ft.ScrollMode.AUTO

    def mostrar_admin():
        page.controls.clear()
        vista_admin = VistaPrincipal(page, producto_service)
        page.add(vista_admin.construir())
        page.update()

    login = VistaLogin(page, autenticacion_repositorio, mostrar_admin)
    page.add(login.construir())


ft.app(target=main, assets_dir="assets")
