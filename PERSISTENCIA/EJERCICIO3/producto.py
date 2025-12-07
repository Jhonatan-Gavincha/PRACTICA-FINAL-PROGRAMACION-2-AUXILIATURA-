import json
import os
from typing import List, Optional

# --- Definición de la Clase Producto ---
class Producto:
    """Representa un producto individual con código, nombre y precio."""
    def __init__(self, codigo: int, nombre: str, precio: float):
        # Atributos: codigo: int, nombre: String, precio: float
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        # Representación en cadena para imprimir el objeto
        return f"Producto(Código: {self.codigo}, Nombre: {self.nombre}, Precio: ${self.precio:.2f})"
    
    def to_dict(self):
        # Método para convertir el objeto a diccionario (útil para guardar en JSON)
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio
        }
    
    @staticmethod
    def from_dict(data: dict):
        # Método estático para crear un objeto Producto a partir de un diccionario
        return Producto(data['codigo'], data['nombre'], data['precio'])

# --- Definición de la Clase ArchivoProducto ---
class ArchivoProducto:
    """Gestiona la colección de Productos y la persistencia de datos usando JSON."""
    def __init__(self, noma: str):
        # Atributo noma: String (Nombre del archivo)
        self.noma = noma

    def _cargar_productos(self) -> List[Producto]:
        """Método interno para cargar la lista de Productos desde el archivo JSON."""
        if not os.path.exists(self.noma):
            self.crearArchivo()

        try:
            with open(self.noma, 'r') as f:
                data = json.load(f)
                # Convertimos cada diccionario de JSON a un objeto Producto
                return [Producto.from_dict(d) for d in data]
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f" Error al cargar productos del archivo: {e}. Retornando lista vacía.")
            return []

    def _guardar_lista(self, productos: List[Producto]) -> None:
        """Método interno para guardar la lista completa de Productos al archivo JSON."""
        data = [p.to_dict() for p in productos]
        try:
            with open(self.noma, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f" Error al guardar la lista en el archivo: {e}")

    # a) Implementar el diagrama de clases: Método constructor y crearArchivo
    def crearArchivo(self) -> None:
        """Inicializa el archivo JSON con una lista vacía de productos."""
        try:
            with open(self.noma, 'w') as f:
                json.dump([], f, indent=4)
            # Nota: No se imprime mensaje para mantenerlo silencioso al usarlo internamente
        except Exception as e:
            print(f" Error al crear el archivo '{self.noma}': {e}")


    # b) Implementa guardarProducto(Producto p) para almacenar productos.
    def guardarProducto(self, p: Producto) -> None:
        """Almacena un producto en el archivo, evitando códigos duplicados."""
        productos = self._cargar_productos()
        
        # Opcional: Evitar duplicados por código
        if any(prod.codigo == p.codigo for prod in productos):
            print(f" Producto con código {p.codigo} ya existe ('{p.nombre}'). No se añadió.")
            return

        productos.append(p)
        self._guardar_lista(productos)
        print(f" Producto '{p.nombre}' (Cód. {p.codigo}) guardado con éxito.")

    # c) Implementa buscaProducto(int c) buscando el código.
    def buscaProducto(self, c: int) -> Optional[Producto]:
        """Busca y retorna un producto por su código."""
        productos = self._cargar_productos()
        
        for p in productos:
            if p.codigo == c:
                return p
        
        return None

    # d) Calcular el promedio de precios de los productos.
    def calcularPromedioPrecios(self) -> float:
        """Calcula el precio promedio de todos los productos en el archivo."""
        productos = self._cargar_productos()
        
        if not productos:
            return 0.0
        
        total_precios = sum(p.precio for p in productos)
        promedio = total_precios / len(productos)
        return promedio

    # e) Mostrar el producto mas caro.
    def mostrarProductoMasCaro(self) -> Optional[Producto]:
        """Busca y retorna el producto con el precio más alto."""
        productos = self._cargar_productos()
        
        if not productos:
            return None
        
        # Usamos la función max() con una clave (key) lambda
        producto_mas_caro = max(productos, key=lambda p: p.precio)
        return producto_mas_caro