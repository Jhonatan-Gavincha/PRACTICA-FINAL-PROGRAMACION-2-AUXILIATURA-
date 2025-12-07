from alimento import Alimento, ArchRefri, os
from datetime import datetime, timedelta

# --- Configuración y Limpieza ---
ARCH_ALIMENTO = "arch_refri.json"

if os.path.exists(ARCH_ALIMENTO):
    os.remove(ARCH_ALIMENTO)
    print(f" Archivo previo '{ARCH_ALIMENTO}' eliminado.")

arch_refri = ArchRefri(ARCH_ALIMENTO)
arch_refri.crearArchivo()

# --- DATOS DE PRUEBA ---

# Fechas para simular:
HOY = datetime.now().strftime('%Y-%m-%d')
AYER = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
MANANA = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
FUTURO = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

# 1. Alimentos iniciales
a1 = Alimento("Leche", AYER, 2)         # Vencido
a2 = Alimento("Yogurt", MANANA, 5)      # Próximo a vencer (Cantidad alta)
a3 = Alimento("Queso", FUTURO, 1)       # Vence en 30 días
a4 = Alimento("Pan", HOY, 0)            # Cantidad 0 (Para punto c)
a5 = Alimento("Jugo", "2024-01-01", 3)  # Vencido (Para punto b y d)

# ---  a) Implementar los métodos para Crear, Modificar por nombre y Eliminar por nombre ---
print("\n--- a.1) Crear/Guardar Alimentos ---")
arch_refri.guardarAlimento(a1)
arch_refri.guardarAlimento(a2)
arch_refri.guardarAlimento(a3)
arch_refri.guardarAlimento(a4)
arch_refri.guardarAlimento(a5)
# Prueba de agregar un alimento ya existente (debe sumar cantidad)
a6_update = Alimento("Yogurt", FUTURO, 3) 
arch_refri.guardarAlimento(a6_update) # La cantidad de Yogurt será 5 + 3 = 8

print("\n--- a.2) Modificar Alimento ('Queso') ---")
arch_refri.modificarAlimento(
    nombre_antiguo="Queso", 
    nuevo_nombre="Queso Fresco", 
    nueva_cantidad=3, 
    nueva_fecha=MANANA
)

print("\n--- a.3) Eliminar Alimento ('Pan') ---")
arch_refri.eliminarAlimento("Pan")


# ---  b) Mostrar los alimentos que caducaron antes de una fecha dada X ---
print("\n--- b) Alimentos Caducados Antes de la Fecha de Hoy ---")
# Usamos la fecha de HOY como límite, que capturará los que vencieron AYER y antes.
caducados_antes = arch_refri.mostrarAlimentosCaducadosAntesDe(HOY)
if caducados_antes:
    print(f"Se encontraron {len(caducados_antes)} alimentos que vencieron ANTES de {HOY}:")
    for a in caducados_antes:
        print(f"  - {a.nombre} (Vence: {a.fechaVencimiento})")
else:
    print("No se encontraron alimentos caducados antes de la fecha límite.")


# ---  c) Eliminar los alimentos que tengan cantidad 0 ---
print("\n--- c) Eliminar Alimentos con Cantidad 0 ---")
# El 'Pan' fue eliminado en a.3. Si hubiera otro con cantidad 0, se eliminaría aquí.
arch_refri.eliminarAlimentosCantidadCero()

print("\n Inventario después de eliminaciones:")
for a in arch_refri.listar():
    print(f"  - {a}")


# ---  d) Buscar los alimentos ya vencidos. ---
print("\n--- d) Buscar Alimentos Vencidos (HOY o ANTES) ---")
alimentos_vencidos = arch_refri.buscarAlimentosVencidos()
if alimentos_vencidos:
    print(f"Se encontraron {len(alimentos_vencidos)} alimentos vencidos:")
    for a in alimentos_vencidos:
        print(f"  -  {a.nombre} (Venció el: {a.fechaVencimiento})")
else:
    print("No hay alimentos vencidos en el refrigerador.")


# ---  e) Mostrar el alimento que tenga más cantidad en el refri. ---
print("\n--- e) Alimento con Más Cantidad ---")
# 'Yogurt' tiene la cantidad más alta (8)
alimento_mas_cantidad = arch_refri.mostrarAlimentoMasCantidad()
if alimento_mas_cantidad:
    print(f" El alimento con más cantidad es: {alimento_mas_cantidad.nombre} ({alimento_mas_cantidad.cantidad} unidades)")
else:
    print("El refrigerador está vacío.")