import flet as ft
from services.producto_service import ProductoService
from services.carrito_service import CarritoService


class VistaTienda:
    def __init__(self, page: ft.Page, producto_service: ProductoService, carrito: CarritoService):
        self.page = page
        self.producto_service = producto_service
        self.carrito = carrito

        self.lista_catalogo = ft.Column()
        self.lista_carrito = ft.Column()
        self.texto_total = ft.Text("Total: $0.00", size=18, weight=ft.FontWeight.BOLD)
        self.mensaje = ft.Text()

    def construir(self) -> ft.Control:
        self.actualizar_catalogo()
        self.actualizar_carrito()

        return ft.Row([
            ft.Column([
                ft.Text("Catalogo", size=22, weight=ft.FontWeight.BOLD),
                self.lista_catalogo,
            ], expand=2, scroll=ft.ScrollMode.AUTO),
            ft.VerticalDivider(),
            ft.Column([
                ft.Text("Carrito", size=22, weight=ft.FontWeight.BOLD),
                self.lista_carrito,
                self.texto_total,
                ft.ElevatedButton("Confirmar compra", on_click=self.confirmar_compra),
                self.mensaje,
            ], expand=1),
        ], expand=True)

    def actualizar_catalogo(self):
        self.lista_catalogo.controls.clear()
        productos = self.producto_service.listar_productos()

        if not productos:
            self.lista_catalogo.controls.append(ft.Text("No hay productos en el catalogo."))

        for p in productos:
            if p.imagen:
                imagen_widget = ft.Image(src=f"assets/{p.imagen}", width=60, height=60, fit=ft.ImageFit.COVER)
            else:
                imagen_widget = ft.Container(width=60, height=60, bgcolor=ft.Colors.GREY_200, border_radius=8)

            tarjeta = ft.Container(
                content=ft.Row([
                    imagen_widget,
                    ft.Column([
                        ft.Text(f"{p.nombre} ({p.categoria})", weight=ft.FontWeight.BOLD),
                        ft.Text(f"${p.precio:.2f}   Stock: {p.stock}"),
                    ], expand=True),
                    ft.ElevatedButton("Agregar al carrito", on_click=lambda e, prod=p: self.agregar_al_carrito(prod)),
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(bottom=8),
            )
            self.lista_catalogo.controls.append(tarjeta)

        self.page.update()

    def actualizar_carrito(self):
        self.lista_carrito.controls.clear()
        items = self.carrito.obtener_items()

        if not items:
            self.lista_carrito.controls.append(ft.Text("Carrito vacio"))

        for item in items:
            self.lista_carrito.controls.append(ft.Row([
                ft.Text(f"{item.producto.nombre} x{item.cantidad}", expand=True),
                ft.Text(f"${item.subtotal:.2f}"),
                ft.IconButton(ft.Icons.CLOSE, on_click=lambda e, id=item.producto.id: self.quitar_del_carrito(id)),
            ]))

        self.texto_total.value = f"Total: ${self.carrito.calcular_total():.2f}"
        self.page.update()

    def agregar_al_carrito(self, producto):
        self.mensaje.value = ""
        try:
            self.carrito.agregar_item(producto, 1)
            self.actualizar_carrito()
        except ValueError as error:
            self.mensaje.color = ft.Colors.RED
            self.mensaje.value = str(error)
            self.page.update()

    def quitar_del_carrito(self, producto_id):
        self.carrito.quitar_item(producto_id)
        self.actualizar_carrito()

    def confirmar_compra(self, e):
        try:
            pedido = self.carrito.confirmar_compra()
            self.mensaje.color = ft.Colors.GREEN
            self.mensaje.value = f"Compra confirmada! Pedido #{pedido.id} - Total ${pedido.total:.2f}"
            self.actualizar_catalogo()
            self.actualizar_carrito()
        except ValueError as error:
            self.mensaje.color = ft.Colors.RED
            self.mensaje.value = str(error)
            self.page.update()
