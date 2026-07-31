import flet as ft
from repositories.autenticacion_repository import IAutenticacionRepository


class VistaLogin:
    def __init__(self, page: ft.Page, autenticacion_repositorio: IAutenticacionRepository, on_login_exitoso):
        self.page = page
        self.autenticacion_repositorio = autenticacion_repositorio
        self.on_login_exitoso = on_login_exitoso

        self.campo_usuario = ft.TextField(label="Usuario", autofocus=True)
        self.campo_password = ft.TextField(label="Contrasena", password=True, can_reveal_password=True)
        self.mensaje = ft.Text(color=ft.Colors.RED)

    def construir(self) -> ft.Control:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Iniciar sesion", size=28, weight=ft.FontWeight.BOLD),
                    self.campo_usuario,
                    self.campo_password,
                    ft.ElevatedButton("Entrar", on_click=self.verificar),
                    self.mensaje,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                width=320,
            ),
            alignment=ft.alignment.center,
            expand=True,
            padding=40,
        )

    def verificar(self, e):
        usuario_escrito = (self.campo_usuario.value or "").strip()
        password_escrito = (self.campo_password.value or "").strip()

        if self.autenticacion_repositorio.validar_credenciales(usuario_escrito, password_escrito):
            self.mensaje.value = ""
            self.on_login_exitoso()
        else:
            self.mensaje.value = "Usuario o contrasena incorrectos"
            self.page.update()
