from biblioteca import (
    Libro, ArchLibro, Cliente, ArchCliente, Prestamo, ArchPrestamo, os
)

# --- Configuración y Limpieza ---
ARCH_LIBRO = "arch_libros.json"
ARCH_CLIENTE = "arch_clientes.json"
ARCH_PRESTAMO = "arch_prestamos.json"

def limpiar_archivos():
    for arch in [ARCH_LIBRO, ARCH_CLIENTE, ARCH_PRESTAMO]:
        if os.path.exists(arch):
            os.remove(arch)
            print(f" Archivo previo '{arch}' eliminado.")

limpiar_archivos()

# --- Inicialización de Gestores ---
arch_libros = ArchLibro(ARCH_LIBRO)
arch_clientes = ArchCliente(ARCH_CLIENTE)
arch_prestamos = ArchPrestamo(ARCH_PRESTAMO, arch_libros, arch_clientes)

# Crear archivos vacíos
arch_libros.crearArchivo()
arch_clientes.crearArchivo()
arch_prestamos.crearArchivo()
print(" Archivos inicializados.")

# --- DATOS DE PRUEBA ---

# 1. Libros
l1 = Libro(1, "El Principito", 15.00)
l2 = Libro(2, "Cien Años de Soledad", 25.50)
l3 = Libro(3, "Don Quijote", 10.00)
l4 = Libro(4, "Ficción Moderna", 35.00)
l5 = Libro(5, "Poesía Clásica", 18.00) # Este no tendrá préstamos (punto c)

arch_libros.guardar(l1)
arch_libros.guardar(l2)
arch_libros.guardar(l3)
arch_libros.guardar(l4)
arch_libros.guardar(l5)

# 2. Clientes
c1 = Cliente(101, "1234567", "Ana", "García")
c2 = Cliente(102, "7654321", "Beto", "López")
c3 = Cliente(103, "1122334", "Carla", "Díaz")

arch_clientes.guardar(c1)
arch_clientes.guardar(c2)
arch_clientes.guardar(c3)

# 3. Préstamos (Ventas)
# Cliente 101: Préstamo de L1 (x2) y L3 (x1)
arch_prestamos.guardar(Prestamo(101, 1, "2024-01-10", 2)) 
arch_prestamos.guardar(Prestamo(101, 3, "2024-01-15", 1))

# Cliente 102: Préstamo de L2 (x1) y L4 (x1) - Tiene 2 préstamos (registros)
arch_prestamos.guardar(Prestamo(102, 2, "2024-02-01", 1))
arch_prestamos.guardar(Prestamo(102, 4, "2024-02-05", 1))

# Cliente 103: Préstamo de L1 (x3) y L2 (x1) - Mayor cantidad (5) para L1, Mayor Cant. Préstamos (2) para C101
arch_prestamos.guardar(Prestamo(103, 1, "2024-03-01", 3)) 
arch_prestamos.guardar(Prestamo(103, 2, "2024-03-10", 1))


# ====================================================================
# --- EJECUCIÓN DE LOS PUNTOS ---
# ====================================================================

# --- a) Listar los libros cuyo precio estén entre 2 valores (x e y). ---
print("\n--- a) Libros con precio entre $15.00 y $25.00 ---")
min_p = 15.00
max_p = 25.00
libros_rango = arch_prestamos.listarLibrosEntrePrecios(min_p, max_p)
for l in libros_rango:
    print(f"  - {l.titulo} (${l.precio:.2f})")


# --- b) Calcular el ingreso total generado por un libro especifico. ---
print("\n--- b) Ingreso Total por 'El Principito' (Cód: 1) ---")
codigo_b = 1 # Total de copias prestadas/vendidas: 2 + 3 = 5
ingreso = arch_prestamos.calcularIngresoTotalPorLibro(codigo_b)
print(f"💰 Ingreso total generado por Cód {codigo_b} ('{l1.titulo}'): ${ingreso:.2f}")


# --- c) Mostrar la lista de libros que nunca fueron vendidos. ---
print("\n--- c) Libros que nunca fueron prestados/vendidos ---")
libros_no_vendidos = arch_prestamos.mostrarLibrosNoVendidos()
if libros_no_vendidos:
    for l in libros_no_vendidos:
        print(f"  - {l.titulo} (Cód: {l.codLibro})")
else:
    print("Todos los libros tienen al menos un registro de préstamo/venta.")


# --- d) Mostrar a todos los clientes que compraron un libro especifico (dado su código). ---
print("\n--- d) Clientes que compraron/prestaron 'Cien Años de Soledad' (Cód: 2) ---")
codigo_d = 2
clientes_libro = arch_prestamos.mostrarClientesPorLibro(codigo_d)
for c in clientes_libro:
    print(f"  - {c.nombre} {c.apellido} (Cód: {c.codCliente})")


# --- e) Definir el libro más prestado. ---
print("\n--- e) Libro más prestado (por cantidad total) ---")
# L1 (Principito) total: 2 + 3 = 5 copias
libro_mas_prestado = arch_prestamos.definirLibroMasPrestado()
if libro_mas_prestado:
    print(f" Libro más prestado: {libro_mas_prestado.titulo} (Cód: {libro_mas_prestado.codLibro})")
else:
    print("No hay préstamos registrados.")


# --- f) Mostrar el cliente que tuvo más préstamos. ---
print("\n--- f) Cliente con más préstamos (por número de registros) ---")
# C101: 2 registros, C102: 2 registros, C103: 2 registros (Empate)
cliente_mas_prestamos = arch_prestamos.mostrarClienteConMasPrestamos()
if cliente_mas_prestamos:
    print(f" Cliente con más préstamos: {cliente_mas_prestamos.nombre} {cliente_mas_prestamos.apellido} (Cód: {cliente_mas_prestamos.codCliente})")
else:
    print("No hay préstamos registrados.")