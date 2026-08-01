import os
import shutil
import flet as ft
from services.producto_service import ProductoService


class VistaPrincipal:
    CATEGORIAS = ["Zapatos", "Balones", "Camisetas", "Balon de Oro"]

    def __init__(self, page: ft.Page, servicio: ProductoService):
        self.page = page
        self.servicio = servicio
        self.lista_productos = ft.Column()
        self.ruta_imagen_seleccionada = None
        self.dialogo_editar = None

        self.campo_nombre = ft.TextField(label="Nombre")
        self.campo_categoria = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(c) for c in self.CATEGORIAS],
        )
        self.campo_descripcion = ft.TextField(label="Descripcion", multiline=True)
        self.campo_talla = ft.TextField(label="Talla (opcional)", width=150)
        self.campo_precio = ft.TextField(label="Precio", width=120)
        self.campo_stock = ft.TextField(label="Stock", width=100)

        self.texto_imagen = ft.Text("Ninguna imagen seleccionada")
        self.file_picker = ft.FilePicker()
        self.file_picker.on_result = self.imagen_seleccionada
        self.page.overlay.append(self.file_picker)

        self.mensaje = ft.Text(color=ft.Colors.RED)

    def construir(self) -> ft.Control:
        formulario = ft.Container(
            content=ft.Column([
                ft.Text("Agregar nuevo producto", size=20, weight=ft.FontWeight.BOLD),
                self.campo_nombre,
                self.campo_categoria,
                self.campo_descripcion,
                ft.Row([self.campo_talla, self.campo_precio, self.campo_stock]),
                ft.Row([
                    ft.ElevatedButton(
                        "Seleccionar imagen",
                        on_click=lambda e: self.file_picker.pick_files(
                            allow_multiple=False,
                            allowed_extensions=["png", "jpg", "jpeg", "webp"],
                        ),
                    ),
                    self.texto_imagen,
                ]),
                ft.ElevatedButton("Agregar producto", on_click=self.agregar_producto),
                self.mensaje,
            ]),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
        )

        self.actualizar_lista()

        return ft.Column([
            ft.Text("Panel de Administrador", size=28, weight=ft.FontWeight.BOLD),
            formulario,
            self.lista_productos,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def imagen_seleccionada(self, e: ft.FilePickerResultEvent):
        if e.files:
            archivo = e.files[0]
            self.ruta_imagen_seleccionada = archivo.path
            self.texto_imagen.value = f"Seleccionada: {archivo.name}"
        else:
            self.ruta_imagen_seleccionada = None
            self.texto_imagen.value = "Ninguna imagen seleccionada"
        self.page.update()

    def actualizar_lista(self):
        self.lista_productos.controls.clear()
        productos = self.servicio.listar_productos()

        if not productos:
            self.lista_productos.controls.append(ft.Text("No hay productos todavia."))

        for p in productos:
            if p.imagen:
                imagen_widget = ft.Image(src=f"assets/{p.imagen}", width=70, height=70, fit=ft.ImageFit.COVER)
            else:
                imagen_widget = ft.Container(width=70, height=70, bgcolor=ft.Colors.GREY_200, border_radius=8)

            info = ft.Column([
                ft.Text(f"{p.nombre} ({p.categoria})", weight=ft.FontWeight.BOLD),
                ft.Text(p.descripcion or ""),
                ft.Text(f"Talla: {p.talla or 'N/A'}   Precio: ${p.precio:.2f}   Stock: {p.stock}"),
            ], expand=True)

            tarjeta = ft.Container(
                content=ft.Row([
                    imagen_widget,
                    info,
                    ft.ElevatedButton("Vender 1", on_click=lambda e, id=p.id: self.vender(id)),
                    ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, prod=p: self.abrir_editar(prod)),
                    ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, id=p.id: self.eliminar(id)),
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                margin=ft.margin.only(bottom=8),
            )
            self.lista_productos.controls.append(tarjeta)

        self.page.update()

    def agregar_producto(self, e):
        self.mensaje.value = ""
        try:
            nombre_archivo_guardado = None
            if self.ruta_imagen_seleccionada:
                os.makedirs("assets", exist_ok=True)
                nombre_archivo_guardado = os.path.basename(self.ruta_imagen_seleccionada)
                destino = os.path.join("assets", nombre_archivo_guardado)
                shutil.copy(self.ruta_imagen_seleccionada, destino)

            self.servicio.crear_producto(
                nombre=self.campo_nombre.value,
                categoria=self.campo_categoria.value,
                descripcion=self.campo_descripcion.value,
                talla=self.campo_talla.value or None,
                precio=float(self.campo_precio.value),
                stock=int(self.campo_stock.value),
                imagen=nombre_archivo_guardado,
            )
            self.campo_nombre.value = ""
            self.campo_categoria.value = None
            self.campo_descripcion.value = ""
            self.campo_talla.value = ""
            self.campo_precio.value = ""
            self.campo_stock.value = ""
            self.ruta_imagen_seleccionada = None
            self.texto_imagen.value = "Ninguna imagen seleccionada"
            self.actualizar_lista()
        except ValueError as error:
            self.mensaje.value = str(error)
            self.page.update()
        except Exception:
            self.mensaje.value = "Revisa que precio y stock sean numeros validos"
            self.page.update()

    def abrir_editar(self, producto):
        self.campo_editar_nombre = ft.TextField(label="Nombre", value=producto.nombre)
        self.campo_editar_categoria = ft.Dropdown(
            label="Categoria",
            options=[ft.dropdown.Option(c) for c in self.CATEGORIAS],
            value=producto.categoria,
        )
        self.campo_editar_descripcion = ft.TextField(label="Descripcion", multiline=True, value=producto.descripcion)
        self.campo_editar_talla = ft.TextField(label="Talla (opcional)", width=150, value=producto.talla or "")
        self.campo_editar_precio = ft.TextField(label="Precio", width=120, value=str(producto.precio))
        self.campo_editar_stock = ft.TextField(label="Stock", width=100, value=str(producto.stock))
        self.mensaje_editar = ft.Text(color=ft.Colors.RED)

        self.dialogo_editar = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar producto"),
            content=ft.Column([
                self.campo_editar_nombre,
                self.campo_editar_categoria,
                self.campo_editar_descripcion,
                ft.Row([self.campo_editar_talla, self.campo_editar_precio, self.campo_editar_stock]),
                self.mensaje_editar,
            ], tight=True, scroll=ft.ScrollMode.AUTO, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo()),
                ft.ElevatedButton(
                    "Guardar cambios",
                    on_click=lambda e, id=producto.id: self.guardar_edicion(id),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(self.dialogo_editar)
        self.dialogo_editar.open = True
        self.page.update()

    def cerrar_dialogo(self):
        if self.dialogo_editar:
            self.dialogo_editar.open = False
            self.page.update()

    def guardar_edicion(self, id_producto):
        self.mensaje_editar.value = ""
        self.campo_editar_nombre.value = (self.campo_editar_nombre.value or "").strip()
        try:
            self.servicio.actualizar_producto(
                id_producto=id_producto,
                nombre=self.campo_editar_nombre.value,
                categoria=self.campo_editar_categoria.value,
                descripcion=self.campo_editar_descripcion.value,
                talla=self.campo_editar_talla.value or None,
                precio=float(self.campo_editar_precio.value),
                stock=int(self.campo_editar_stock.value),
            )
            self.cerrar_dialogo()
            self.actualizar_lista()
        except ValueError as error:
            self.mensaje_editar.value = str(error)
            self.page.update()
        except Exception:
            self.mensaje_editar.value = "Revisa que precio y stock sean numeros validos"
            self.page.update()

    def vender(self, id_producto):
        try:
            self.servicio.vender_producto(id_producto, 1)
            self.actualizar_lista()
        except ValueError as error:
            self.mensaje.value = str(error)
            self.page.update()

    def eliminar(self, id_producto):
        self.servicio.eliminar_producto(id_producto)
        self.actualizar_lista()
