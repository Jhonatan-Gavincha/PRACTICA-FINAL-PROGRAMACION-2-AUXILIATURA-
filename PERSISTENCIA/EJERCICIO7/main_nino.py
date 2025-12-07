from nino import Nino, ArchNino, os

# --- Configuración y Limpieza ---
ARCH_NINO = "arch_ninos.json"

if os.path.exists(ARCH_NINO):
    os.remove(ARCH_NINO)
    print(f" Archivo previo '{ARCH_NINO}' eliminado.")

arch_ninos = ArchNino(ARCH_NINO)
arch_ninos.crearArchivo()
print(" Archivo inicializado.")

# --- DATOS DE PRUEBA ---

# Niños adecuados (siguiendo la tabla ficticia: Edad: (Peso Mínimo kg, Talla Mínima cm))
# 4 años: (15.0, 100.0)
n1 = Nino("Carlos", "Rojas", "Soliz", 101, 4, "15.5 kg", "101 cm") # Adecuado
# 6 años: (19.0, 110.0)
n2 = Nino("Laura", "Perez", "Vaca", 102, 6, "20 kg", "115 cm")    # Adecuado
# 7 años: (21.0, 115.0)
n3 = Nino("Matias", "Lanza", "Crespo", 103, 7, "22.1 kg", "116 cm") # Adecuado (Talla Máxima)

# Niños NO adecuados
# 4 años: (15.0, 100.0) -> Pesa menos
n4 = Nino("Sofia", "Vargas", "Mora", 104, 4, "14 kg", "102 cm")   # No adecuado (por peso)
# 6 años: (19.0, 110.0) -> Mide menos
n5 = Nino("Javier", "Guzman", "Lima", 105, 6, "19 kg", "105 cm")   # No adecuado (por talla)
# 7 años: (21.0, 115.0) -> Pesa y mide menos
n6 = Nino("Andrea", "Flores", "Duran", 106, 7, "20 kg", "110 cm")  # No adecuado (peso y talla)

# Guardar los niños
print("\n--- Guardando registros de Niños ---")
arch_ninos.guardar(n1)
arch_ninos.guardar(n2)
arch_ninos.guardar(n3)
arch_ninos.guardar(n4)
arch_ninos.guardar(n5)
arch_ninos.guardar(n6)


# ====================================================================
# --- EJECUCIÓN DE LOS PUNTOS ---
# ====================================================================

# -- a) Crear, leer, listar y mostrar. ---
print("\n--- a) Leer, Listar y Mostrar ---")
# Demostración de 'leer'
nino_leido = arch_ninos.leer(n2)
print(f"Lectura de niño 102: {nino_leido.get_nombre_completo()}")
# Demostración de 'listar_y_mostrar' (incluye el listado de todos)
arch_ninos.listar_y_mostrar()


# -- b) Cuántos niños tienen el peso adecuado de acuerdo a su talla y edad ---
print("\n--- b) Conteo de Niños con Peso/Talla Adecuado ---")
conteo_adecuados = arch_ninos.contarNinosAdecuados()
print(f" Cantidad de niños con peso y talla adecuados: {conteo_adecuados} (Esperado: 3)")


# -- c) Mostrar a los niños que de acuerdo a la edad no tienen el peso o la talla adecuada. ---
print("\n--- c) Niños No Adecuados (Peso o Talla) ---")
ninos_no_adecuados = arch_ninos.mostrarNinosNoAdecuados()
if ninos_no_adecuados:
    print(f"Lista de {len(ninos_no_adecuados)} niños no adecuados:")
    for n in ninos_no_adecuados:
        print(f"  - {n.get_nombre_completo()} (Edad: {n.edad}, Peso: {n.peso}, Talla: {n.talla})")
else:
    print("Todos los niños están dentro de los rangos adecuados.")


# -- d) Determinar el promedio de edad en los niños. ---
print("\n--- d) Promedio de Edad ---")
# Edades: 4, 6, 7, 4, 6, 7. Suma: 34. Promedio: 34/6 = 5.66...
promedio_edad = arch_ninos.determinarPromedioEdad()
print(f" El promedio de edad de los niños es: {promedio_edad:.2f} años.")


# -- e) Buscar al niño con el carnet x. ---
print("\n--- e) Buscar Niño con Carnet (CI) 105 ---")
ci_buscado = 105
nino_buscado = arch_ninos.buscar_por_ci(ci_buscado)
if nino_buscado:
    print(f" Niño encontrado (CI {ci_buscado}): {nino_buscado.get_nombre_completo()}")
else:
    print(f" Niño con CI {ci_buscado} no encontrado.")


# -- f) Mostrar a los niños con la talla más alta. ---
print("\n--- f) Niños con la Talla Más Alta ---")
# Talla más alta: 116 cm (Matias)
ninos_talla_alta = arch_ninos.mostrarNinosTallaMasAlta()
if ninos_talla_alta:
    talla_max = ninos_talla_alta[0].talla # Ya que todos tienen la misma talla máxima
    print(f" Niños con la talla más alta ({talla_max}):")
    for n in ninos_talla_alta:
        print(f"  - {n.get_nombre_completo()} (Talla: {n.talla})")
else:
    print("No hay niños registrados.")