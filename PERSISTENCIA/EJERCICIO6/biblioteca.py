import json
import os
from typing import List, Optional, Dict, Any, Union

# --- Helpers de Persistencia JSON ---
# Simplificamos la carga y guardado para las 3 clases de archivo

def _cargar_data(nombre_archivo: str) -> List[Dict[str, Any]]:
    """Carga datos crudos (lista de diccionarios) desde un archivo JSON."""
    if not os.path.exists(nombre_archivo):
        return []
    try:
        with open(nombre_archivo, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return []

def _guardar_data(nombre_archivo: str, data: List[Dict[str, Any]]) -> None:
    """Guarda una lista de diccionarios a un archivo JSON."""
    try:
        with open(nombre_archivo, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f" Error al guardar en {nombre_archivo}: {e}")

# ====================================================================
# --- CLASES DE ENTIDAD ---
# ====================================================================

class Libro:
    def __init__(self, codLibro: int, titulo: str, precio: float):
        self.codLibro = codLibro
        self.titulo = titulo
        self.precio = precio # Interpretado como precio de venta para el punto b)

    def to_dict(self):
        return {"codLibro": self.codLibro, "titulo": self.titulo, "precio": self.precio}

    @staticmethod
    def from_dict(data: dict):
        return Libro(data['codLibro'], data['titulo'], data['precio'])
    
    def __str__(self):
        return f"Libro(Cód: {self.codLibro}, Título: {self.titulo}, Precio: ${self.precio:.2f})"

class Cliente:
    def __init__(self, codCliente: int, ci: str, nombre: str, apellido: str):
        self.codCliente = codCliente
        self.ci = ci
        self.nombre = nombre
        self.apellido = apellido

    def to_dict(self):
        return {"codCliente": self.codCliente, "ci": self.ci, "nombre": self.nombre, "apellido": self.apellido}

    @staticmethod
    def from_dict(data: dict):
        return Cliente(data['codCliente'], data['ci'], data['nombre'], data['apellido'])
    
    def __str__(self):
        return f"Cliente(Cód: {self.codCliente}, CI: {self.ci}, Nombre: {self.nombre} {self.apellido})"

class Prestamo:
    def __init__(self, codCliente: int, codLibro: int, fechaPrestamo: str, cantidad: int):
        self.codCliente = codCliente
        self.codLibro = codLibro
        self.fechaPrestamo = fechaPrestamo
        self.cantidad = cantidad # Interpretado como cantidad de copias prestadas

    def to_dict(self):
        return {"codCliente": self.codCliente, "codLibro": self.codLibro, "fechaPrestamo": self.fechaPrestamo, "cantidad": self.cantidad}

    @staticmethod
    def from_dict(data: dict):
        return Prestamo(data['codCliente'], data['codLibro'], data['fechaPrestamo'], data['cantidad'])
    
    def __str__(self):
        return f"Préstamo(Clt: {self.codCliente}, Lib: {self.codLibro}, Cant: {self.cantidad}, Fecha: {self.fechaPrestamo})"

# ====================================================================
# --- CLASES DE ARCHIVO (GESTORAS) ---
# ====================================================================

class ArchLibro:
    def __init__(self, nomArch: str):
        self.nomArch = nomArch

    def crearArchivo(self):
        _guardar_data(self.nomArch, [])

    def listar(self) -> List[Libro]:
        data = _cargar_data(self.nomArch)
        return [Libro.from_dict(d) for d in data]

    def guardar(self, libro: Libro):
        libros = self.listar()
        if any(l.codLibro == libro.codLibro for l in libros):
            print(f"⚠️ Libro con código {libro.codLibro} ya existe. No se añadió.")
            return
        libros.append(libro)
        _guardar_data(self.nomArch, [l.to_dict() for l in libros])
        print(f"➕ Libro '{libro.titulo}' guardado.")

    def buscar_por_codigo(self, cod: int) -> Optional[Libro]:
        libros = self.listar()
        return next((l for l in libros if l.codLibro == cod), None)


class ArchCliente:
    def __init__(self, nomArch: str):
        self.nomArch = nomArch

    def crearArchivo(self):
        _guardar_data(self.nomArch, [])

    def listar(self) -> List[Cliente]:
        data = _cargar_data(self.nomArch)
        return [Cliente.from_dict(d) for d in data]

    def guardar(self, cliente: Cliente):
        clientes = self.listar()
        if any(c.codCliente == cliente.codCliente for c in clientes):
            print(f"⚠️ Cliente con código {cliente.codCliente} ya existe. No se añadió.")
            return
        clientes.append(cliente)
        _guardar_data(self.nomArch, [c.to_dict() for c in clientes])
        print(f"➕ Cliente '{cliente.nombre}' guardado.")

    def buscar_por_codigo(self, cod: int) -> Optional[Cliente]:
        clientes = self.listar()
        return next((c for c in clientes if c.codCliente == cod), None)


class ArchPrestamo:
    def __init__(self, nomArch: str, arch_libro: ArchLibro, arch_cliente: ArchCliente):
        self.nomArch = nomArch
        self.arch_libro = arch_libro      # Para buscar datos de Libro
        self.arch_cliente = arch_cliente  # Para buscar datos de Cliente

    def crearArchivo(self):
        _guardar_data(self.nomArch, [])

    def listar(self) -> List[Prestamo]:
        data = _cargar_data(self.nomArch)
        return [Prestamo.from_dict(d) for d in data]

    def guardar(self, prestamo: Prestamo):
        # Validar que los códigos existan antes de guardar el préstamo
        if not self.arch_cliente.buscar_por_codigo(prestamo.codCliente):
            print(f" Error: Cliente con código {prestamo.codCliente} no encontrado. Préstamo no registrado.")
            return
        if not self.arch_libro.buscar_por_codigo(prestamo.codLibro):
            print(f" Error: Libro con código {prestamo.codLibro} no encontrado. Préstamo no registrado.")
            return

        prestamos = self.listar()
        prestamos.append(prestamo)
        _guardar_data(self.nomArch, [p.to_dict() for p in prestamos])
        print(f" Préstamo (Clt: {prestamo.codCliente}, Lib: {prestamo.codLibro}) registrado.")

    # --- IMPLEMENTACIÓN DE LOS PUNTOS DEL EJERCICIO 6 ---

    # a) Listar los libros cuyo precio estén entre 2 valores (x e y).
    def listarLibrosEntrePrecios(self, x: float, y: float) -> List[Libro]:
        """Retorna libros cuyo precio está entre x (mínimo) y y (máximo)."""
        libros = self.arch_libro.listar()
        return [l for l in libros if x <= l.precio <= y]

    # b) Calcular el ingreso total generado por un libro especifico.
    # Nota: Interpretamos "prestamo" como "venta" dado el atributo 'precio' en Libro y el punto b).
    def calcularIngresoTotalPorLibro(self, cod_libro: int) -> float:
        """Calcula el ingreso total (Precio * Cantidad) generado por un libro."""
        libro = self.arch_libro.buscar_por_codigo(cod_libro)
        if not libro:
            return 0.0

        prestamos = self.listar()
        ingreso_total = 0.0
        
        for p in prestamos:
            if p.codLibro == cod_libro:
                # Ingreso = Precio del Libro * Cantidad Prestada/Vendida
                ingreso_total += libro.precio * p.cantidad
        
        return ingreso_total

    # c) Mostrar la lista de libros que nunca fueron vendidos (prestados).
    def mostrarLibrosNoVendidos(self) -> List[Libro]:
        """Retorna la lista de libros que no tienen ningún registro de préstamo/venta."""
        libros = self.arch_libro.listar()
        prestamos = self.listar()
        
        codigos_prestados = {p.codLibro for p in prestamos}
        
        # Filtra los libros cuyo código NO está en el conjunto de códigos prestados
        libros_no_vendidos = [l for l in libros if l.codLibro not in codigos_prestados]
        return libros_no_vendidos

    # d) Mostrar a todos los clientes que compraron un libro especifico (dado su código).
    def mostrarClientesPorLibro(self, cod_libro: int) -> List[Cliente]:
        """Retorna la lista de clientes que compraron/prestaron un libro específico."""
        prestamos = self.listar()
        
        # 1. Obtener los códigos de clientes únicos que prestaron ese libro
        codigos_clientes = {p.codCliente for p in prestamos if p.codLibro == cod_libro}
        
        # 2. Buscar los objetos Cliente correspondientes
        clientes_encontrados = []
        for cod_c in codigos_clientes:
            cliente = self.arch_cliente.buscar_por_codigo(cod_c)
            if cliente:
                clientes_encontrados.append(cliente)
                
        return clientes_encontrados

    # e) Definir el libro más prestado.
    def definirLibroMasPrestado(self) -> Optional[Libro]:
        """Encuentra y retorna el libro con la mayor cantidad total de copias prestadas."""
        prestamos = self.listar()
        
        if not prestamos:
            return None
            
        # Contar la cantidad total prestada por código de libro
        conteo_prestamos: Dict[int, int] = {}
        for p in prestamos:
            conteo_prestamos[p.codLibro] = conteo_prestamos.get(p.codLibro, 0) + p.cantidad

        # Encontrar el código del libro con el valor máximo
        cod_mas_prestado = max(conteo_prestamos, key=conteo_prestamos.get)
        
        # Retornar el objeto Libro
        return self.arch_libro.buscar_por_codigo(cod_mas_prestado)

    # f) Mostrar el cliente que tuvo más préstamos.
    def mostrarClienteConMasPrestamos(self) -> Optional[Cliente]:
        """Encuentra y retorna el cliente que tiene la mayor cantidad de préstamos (registros)."""
        prestamos = self.listar()
        
        if not prestamos:
            return None
            
        # Contar el número de registros de préstamo por cliente
        conteo_clientes: Dict[int, int] = {}
        for p in prestamos:
            conteo_clientes[p.codCliente] = conteo_clientes.get(p.codCliente, 0) + 1 # Contamos un registro por préstamo

        # Encontrar el código del cliente con el valor máximo
        cod_mas_prestamos = max(conteo_clientes, key=conteo_clientes.get)
        
        # Retornar el objeto Cliente
        return self.arch_cliente.buscar_por_codigo(cod_mas_prestamos)