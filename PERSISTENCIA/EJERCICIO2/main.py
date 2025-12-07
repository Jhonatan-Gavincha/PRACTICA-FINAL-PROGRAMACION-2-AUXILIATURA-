from trabajador import Trabajador, ArchivoTrabajador
import os

# --- Configuración ---
NOMBRE_ARCHIVO = "datos_trabajadores.json"

# Si el archivo existe de una ejecución previa, lo eliminamos para tener una prueba limpia
if os.path.exists(NOMBRE_ARCHIVO):
    os.remove(NOMBRE_ARCHIVO)
    print(f"🗑️ Archivo previo '{NOMBRE_ARCHIVO}' eliminado.")

archivo_gestion = ArchivoTrabajador(NOMBRE_ARCHIVO)


# ---  a) Crear y guardar el archivo ---
print("\n--- a) Crear Archivo ---")
# La clase lo crea automáticamente, pero lo llamamos explícitamente:
archivo_gestion.crearArchivo()


# ---  b) Implementar un método para guardar trabajadores. ---
print("\n--- b) Guardar Trabajadores ---")
t1 = Trabajador("Ana López", 101, 30000.00)
t2 = Trabajador("Roberto Pérez", 102, 55000.00)
t3 = Trabajador("Carla Díaz", 103, 40000.00)
t4 = Trabajador("Miguel Soto", 104, 55000.00)

archivo_gestion.guardarTrabajador(t1)
archivo_gestion.guardarTrabajador(t2)
archivo_gestion.guardarTrabajador(t3)
archivo_gestion.guardarTrabajador(t4) # Mismo salario que t2 para probar el ordenamiento

# Mostrar la lista actual después de guardar
print("\n Lista de trabajadores guardados:")
lista_actual = archivo_gestion._cargar_trabajadores()
for t in lista_actual:
    print(f"  - {t}")


# ---  c) Implementar un método para aumentar el salario de un trabajador t. ---
print("\n--- c) Aumentar Salario ---")
# Aumentar el salario de Roberto (Carnet 102) en 5000.00
archivo_gestion.aumentaSalario(5000.00, 102)

# Verificar el cambio
print("\n Lista de trabajadores después del aumento:")
lista_despues_aumento = archivo_gestion._cargar_trabajadores()
for t in lista_despues_aumento:
    print(f"  - {t}")


# ---  d) Buscar el trabajador con el mayor salario. ---
print("\n--- d) Buscar Mayor Salario ---")
mayor_salario = archivo_gestion.buscarMayorSalario()
if mayor_salario:
    print(f" El trabajador con el mayor salario es: {mayor_salario}")
else:
    print("No hay trabajadores para buscar.")


# ---  e) Ordenar a los trabajadores por su salario. ---
print("\n--- e) Ordenar por Salario (Descendente - Mayor a Menor) ---")
trabajadores_ordenados_desc = archivo_gestion.ordenarPorSalario(ascendente=False)
for i, t in enumerate(trabajadores_ordenados_desc):
    print(f"  {i+1}. {t}")

print("\n--- e) Ordenar por Salario (Ascendente - Menor a Mayor) ---")
trabajadores_ordenados_asc = archivo_gestion.ordenarPorSalario(ascendente=True)
for i, t in enumerate(trabajadores_ordenados_asc):
    print(f"  {i+1}. {t}")