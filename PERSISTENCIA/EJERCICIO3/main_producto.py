from producto import Producto, ArchivoProducto
import os

# --- Configuración ---
NOMBRE_ARCHIVO = "datos_productos.json"

# Limpieza: Si el archivo existe de una ejecución previa, lo eliminamos
if os.path.exists(NOMBRE_ARCHIVO):
    os.remove(NOMBRE_ARCHIVO)
    print(f" Archivo previo '{NOMBRE_ARCHIVO}' eliminado.")

archivo_gestion = ArchivoProducto(NOMBRE_ARCHIVO)

# ---a) Implementar el diagrama de clases: Constructor y crearArchivo ---
print("\n--- a) Inicialización y Creación de Archivo ---")
archivo_gestion.crearArchivo()
print(f" Gestor de productos creado para el archivo '{NOMBRE_ARCHIVO}'.")


# ---b) Implementa guardarProducto(Producto p) para almacenar productos. ---
print("\n--- b) Almacenar Productos ---")
p1 = Producto(1001, "Leche Entera", 1.99)
p2 = Producto(1002, "Pan Integral", 3.50)
p3 = Producto(1003, "Manzanas", 5.00)
p4 = Producto(1004, "Cereales Premium", 6.50)
p5 = Producto(1005, "Agua Mineral (Pack)", 4.01)

archivo_gestion.guardarProducto(p1)
archivo_gestion.guardarProducto(p2)
archivo_gestion.guardarProducto(p3)
archivo_gestion.guardarProducto(p4)
archivo_gestion.guardarProducto(p5)

print("\n Lista de productos guardados:")
lista_actual = archivo_gestion._cargar_productos()
for p in lista_actual:
    print(f"  - {p}")


# ---c) Implementa buscaProducto(int c) buscando el código. ---
print("\n--- c) Buscar Producto por Código ---")
codigo_a_buscar = 1003
producto_encontrado = archivo_gestion.buscaProducto(codigo_a_buscar)

if producto_encontrado:
    print(f" Producto encontrado (Cód. {codigo_a_buscar}): {producto_encontrado.nombre} con precio ${producto_encontrado.precio:.2f}")
else:
    print(f" Producto con código {codigo_a_buscar} no encontrado.")


# ---d) Calcular el promedio de precios de los productos. ---
print("\n--- d) Calcular Promedio de Precios ---")
promedio = archivo_gestion.calcularPromedioPrecios()
print(f" El promedio de precios de todos los productos es: ${promedio:.2f}")


# ---e) Mostrar el producto mas caro. ---
print("\n--- e) Mostrar el Producto Más Caro ---")
producto_mas_caro = archivo_gestion.mostrarProductoMasCaro()

if producto_mas_caro:
    print(f"💰 El producto más caro es: {producto_mas_caro.nombre} (Código: {producto_mas_caro.codigo}) con un precio de ${producto_mas_caro.precio:.2f}")
else:
    print("No hay productos para buscar el más caro.")