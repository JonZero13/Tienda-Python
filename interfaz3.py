import tkinter as tk
from tkinter import ttk

class Producto:
    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def mostrar_info(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}, Categoría: {self.categoria.nombre}\n"

class Cliente:
    def __init__(self, nombre, apellido, id_cliente):
        self.nombre = nombre
        self.apellido = apellido
        self.id_cliente = id_cliente

    def mostrar_info(self):
        return f"Cliente: {self.nombre} {self.apellido}, ID: {self.id_cliente}\n"

class Orden:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []
        self.total = 0.0

    def agregar_item(self, item):
        self.items.append(item)
        self.calcular_total()

    def calcular_total(self):
        self.total = sum(item.calcular_subtotal() for item in self.items)

    def mostrar_info(self):
        info = f"Orden de {self.cliente.nombre} {self.cliente.apellido}, Total: {self.total}\n"
        for item in self.items:
            info += item.mostrar_info()
        return info

class ItemOrden:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.cantidad * self.producto.precio

    def mostrar_info(self):
        return f"Item: {self.producto.nombre}, Cantidad: {self.cantidad}, Subtotal: {self.calcular_subtotal()}\n"

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_info(self):
        return f"Categoría: {self.nombre}\n"

class Tienda:
    def __init__(self, info_text):
        self.productos = []
        self.clientes = []
        self.ordenes = []
        self.categorias = []
        self.info_text = info_text

    def registrar_producto(self, producto):
        self.productos.append(producto)
        self.info_text.insert(tk.END, f"Producto '{producto.nombre}' registrado.\n")

    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.info_text.insert(tk.END, f"Cliente '{cliente.nombre} {cliente.apellido}' registrado.\n")

    def crear_orden(self, cliente):
        orden = Orden(cliente)
        self.ordenes.append(orden)
        self.info_text.insert(tk.END, f"Orden creada para el cliente '{cliente.nombre} {cliente.apellido}'\n")
        return orden

    def mostrar_productos(self):
        self.info_text.insert(tk.END, "Productos en la tienda:\n")
        for producto in self.productos:
            self.info_text.insert(tk.END, producto.mostrar_info())

class GestionTienda:
    def __init__(self, root):
        self.tienda = Tienda(None)

        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Pestaña de productos
        self.producto_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.producto_tab, text="Productos")

        self.producto_frame = tk.LabelFrame(self.producto_tab, text="Agregar Producto", padx=10, pady=10)
        self.producto_frame.pack(fill="x", padx=10, pady=10)

        self.producto_nombre_entry = self.crear_entrada(self.producto_frame, "Nombre del Producto:", 0, 0)
        self.producto_precio_entry = self.crear_entrada(self.producto_frame, "Precio:", 1, 0)
        self.categoria_nombre_entry = self.crear_entrada(self.producto_frame, "Categoría:", 2, 0)

        self.agregar_producto_button = tk.Button(self.producto_frame, text="Agregar Producto", command=self.agregar_producto)
        self.agregar_producto_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de clientes
        self.cliente_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cliente_tab, text="Clientes")

        self.cliente_frame = tk.LabelFrame(self.cliente_tab, text="Agregar Cliente", padx=10, pady=10)
        self.cliente_frame.pack(fill="x", padx=10, pady=10)

        self.cliente_nombre_entry = self.crear_entrada(self.cliente_frame, "Nombre del Cliente:", 0, 0)
        self.cliente_apellido_entry = self.crear_entrada(self.cliente_frame, "Apellido del Cliente:", 1, 0)
        self.cliente_id_entry = self.crear_entrada(self.cliente_frame, "ID del Cliente:", 2, 0)

        self.agregar_cliente_button = tk.Button(self.cliente_frame, text="Agregar Cliente", command=self.agregar_cliente)
        self.agregar_cliente_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de órdenes
        self.orden_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.orden_tab, text="Órdenes")

        self.orden_frame = tk.LabelFrame(self.orden_tab, text="Crear Orden", padx=10, pady=10)
        self.orden_frame.pack(fill="x", padx=10, pady=10)

        self.orden_cliente_id_entry = self.crear_entrada(self.orden_frame, "ID del Cliente:", 0, 0)

        self.agregar_orden_button = tk.Button(self.orden_frame, text="Crear Orden", command=self.crear_orden)
        self.agregar_orden_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de información
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text="Información")

        self.info_text = tk.Text(self.info_tab, height=20, width=50)
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Asociar info_text con tienda
        self.tienda.info_text = self.info_text

        # Botón para mostrar productos
        self.mostrar_productos_button = tk.Button(self.info_tab, text="Mostrar Productos", command=self.mostrar_productos)
        self.mostrar_productos_button.pack(pady=5)

    def crear_entrada(self, parent, texto, fila, columna):
        label = tk.Label(parent, text=texto)
        label.grid(row=fila, column=columna, sticky="w", padx=5, pady=5)
        entry = tk.Entry(parent)
        entry.grid(row=fila, column=columna+1, sticky="w", padx=5, pady=5)
        return entry

    def agregar_producto(self):
        nombre_producto = self.producto_nombre_entry.get()
        precio_producto = float(self.producto_precio_entry.get())
        nombre_categoria = self.categoria_nombre_entry.get()

        categoria = next((c for c in self.tienda.categorias if c.nombre == nombre_categoria), None)
        if not categoria:
            categoria = Categoria(nombre_categoria)
            self.tienda.categorias.append(categoria)

        producto = Producto(nombre_producto, precio_producto, categoria)
        self.tienda.registrar_producto(producto)

        for entry in [self.producto_nombre_entry, self.producto_precio_entry, self.categoria_nombre_entry]:
            entry.delete(0, tk.END)

    def agregar_cliente(self):
        nombre_cliente = self.cliente_nombre_entry.get()
        apellido_cliente = self.cliente_apellido_entry.get()
        id_cliente = self.cliente_id_entry.get()

        cliente = Cliente(nombre_cliente, apellido_cliente, id_cliente)
        self.tienda.registrar_cliente(cliente)

        for entry in [self.cliente_nombre_entry, self.cliente_apellido_entry, self.cliente_id_entry]:
            entry.delete(0, tk.END)

    def crear_orden(self):
        id_cliente = self.orden_cliente_id_entry.get()
        cliente = next((c for c in self.tienda.clientes if c.id_cliente == id_cliente), None)
        if cliente:
            self.tienda.crear_orden(cliente)
        else:
            self.info_text.insert(tk.END, f"Cliente con ID {id_cliente} no encontrado.\n")

        self.orden_cliente_id_entry.delete(0, tk.END)

    def mostrar_productos(self):
        self.tienda.mostrar_productos()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de Tienda")
    root.geometry("800x600")
    gestion_tienda = GestionTienda(root)
    root.mainloop()
