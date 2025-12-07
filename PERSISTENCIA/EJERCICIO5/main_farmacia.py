from farmacia import Medicamento, Farmacia, ArchFarmacia
import os

# --- Configuración ---
NOMBRE_ARCHIVO = "datos_farmacias.json"

# Limpieza: Si el archivo existe de una ejecución previa, lo eliminamos
if os.path.exists(NOMBRE_ARCHIVO):
    os.remove(NOMBRE_ARCHIVO)
    print(f"🗑️ Archivo previo '{NOMBRE_ARCHIVO}' eliminado.")

archivo_gestion = ArchFarmacia(NOMBRE_ARCHIVO)
archivo_gestion.crearArchivo()

# --- DATOS DE PRUEBA ---
# Medicamentos
m1 = Medicamento("Tapsin", 10, "Resfrío", 4.50)
m2 = Medicamento("JarabeToux", 20, "Tos", 6.00)
m3 = Medicamento("Ibuprofeno 400", 30, "Dolor", 2.00)
m4 = Medicamento("Aspirina", 40, "Dolor", 1.50)
m5 = Medicamento("Gripalgin", 50, "Resfrío", 3.00)
m6 = Medicamento("Tossecalm", 60, "Tos", 7.50)
m7 = Medicamento("Tapsin Forte", 70, "Resfrío", 5.50)

# Farmacias
f1 = Farmacia("Cruz del Sur", 1, "Av. Siempre Viva 742")
f1.adicionar_medicamento(m1) # Tapsin (Resfrío)
f1.adicionar_medicamento(m2) # JarabeToux (Tos)
f1.adicionar_medicamento(m3) # Ibuprofeno (Dolor)

f2 = Farmacia("Farmacia Central", 2, "Calle B #123")
f2.adicionar_medicamento(m4) # Aspirina (Dolor)
f2.adicionar_medicamento(m5) # Gripalgin (Resfrío)
f2.adicionar_medicamento(m6) # Tossecalm (Tos)
f2.adicionar_medicamento(m7) # Tapsin Forte (Resfrío)

f3 = Farmacia("Farmacia Norte", 3, "Av. América 45")
f3.adicionar_medicamento(m3) # Ibuprofeno (Dolor) - Mismo código, no se añade
f3.adicionar_medicamento(m7) # Tapsin Forte (Resfrío)

# Guardar Farmacias en el archivo
print("\n--- Adición de Farmacias al Archivo ---")
archivo_gestion.adicionar(f1)
archivo_gestion.adicionar(f2)
archivo_gestion.adicionar(f3)

# --- a) Mostrar los medicamentos para la tos, de la Sucursal número X ---
print("\n--- a) Medicamentos para la Tos de la Sucursal 2 ---")
sucursal_x = 2
medicamentos_tos = archivo_gestion.mostrarMedicamentosTosSucursal(sucursal_x)

if medicamentos_tos:
    print(f"Med. Tipo 'Tos' en Sucursal {sucursal_x} ({f2.direccion}):")
    for m in medicamentos_tos:
        print(f"  - {m.nombre} (${m.precio:.2f})")
else:
    print(f"No se encontraron medicamentos 'Tos' en Sucursal {sucursal_x}.")


# --- b) Mostrar el número de sucursal y su dirección que tienen el medicamento "Tapsin". ---
print("\n--- b) Sucursales con el medicamento 'Tapsin' ---")
med_buscado = "Tapsin"
sucursales_con_tapsin = archivo_gestion.buscarFarmaciasPorMedicamento(med_buscado)

if sucursales_con_tapsin:
    print(f"Sucursales que tienen '{med_buscado}':")
    for res in sucursales_con_tapsin:
        print(f"  - Sucursal: {res['sucursal']}, Dirección: {res['direccion']}")
else:
    print(f"Ninguna sucursal tiene el medicamento '{med_buscado}'.")


# --- c) Buscar medicamentos por tipo. ---
print("\n--- c) Buscar Medicamentos por Tipo: 'Dolor' (Global) ---")
tipo_buscado = "Dolor"
medicamentos_dolor = archivo_gestion.buscarMedicamentosPorTipo(tipo_buscado)

if medicamentos_dolor:
    print(f"Todos los medicamentos de tipo '{tipo_buscado}' encontrados:")
    for m in medicamentos_dolor:
        print(f"  - {m.nombre} (Cod: {m.codMedicamento}, Precio: ${m.precio:.2f})")
else:
    print(f"No se encontraron medicamentos de tipo '{tipo_buscado}'.")


# --- d) Ordenar las farmacias según su dirección en orden alfabético. ---
print("\n--- d) Farmacias ordenadas por Dirección ---")
farmacias_ordenadas = archivo_gestion.ordenarFarmaciasPorDireccion()
print("Orden Alfabético por Dirección:")
for f in farmacias_ordenadas:
    print(f"  - Sucursal {f.getSucursal()}: {f.getDireccion()}")


# --- e) Mover los medicamentos de tipo x de la farmacia y a la farmacia z. ---
print("\n--- e) Mover Medicamentos (Tipo 'Tos'): Sucursal 2 -> Sucursal 3 ---")
tipo_a_mover = "Tos"
sucursal_origen = 2
sucursal_destino = 3

archivo_gestion.moverMedicamentosPorTipo(tipo_a_mover, sucursal_origen, sucursal_destino)

# Verificar el inventario después del movimiento
print("\n Inventario después del movimiento:")
farmacias_final = archivo_gestion._cargar_farmacias()

for f in farmacias_final:
    print(f"\n* {f.nombreFarmacia} (Sucursal {f.sucursal}):")
    if not f.medicamentos:
        print("  (Sin medicamentos)")
    for m in f.medicamentos:
        print(f"  - {m.nombre} (Tipo: {m.tipo})")