from zoo import Animal, Zoologico, ArchZoo, os

# --- Configuración y Limpieza ---
ARCH_ZOO = "arch_zoos.json"

if os.path.exists(ARCH_ZOO):
    os.remove(ARCH_ZOO)
    print(f"Archivo previo '{ARCH_ZOO}' eliminado.")

arch_zoo = ArchZoo(ARCH_ZOO)
arch_zoo.crearArchivo()

# --- DATOS DE PRUEBA ---

# Animales
a1 = Animal("Mamífero", "León", 5)
a2 = Animal("Mamífero", "Tigre", 3)
a3 = Animal("Ave", "Águila", 8)
a4 = Animal("Ave", "Loro", 15)
a5 = Animal("Reptil", "Serpiente", 10)
a6 = Animal("Mamífero", "Jirafa", 4)
a7 = Animal("Reptil", "Cocodrilo", 2)

# Zoológicos
# Z1: 3 variedades (León, Tigre, Águila)
z1 = Zoologico(1, "Zoo Metropolitano")
z1.adicionar_animal(a1)
z1.adicionar_animal(a2)
z1.adicionar_animal(a3)

# Z2: 4 variedades (Loro, Serpiente, Jirafa, Cocodrilo) - Mayor variedad inicialmente
z2 = Zoologico(2, "Zoo Central")
z2.adicionar_animal(a4)
z2.adicionar_animal(a5)
z2.adicionar_animal(a6)
z2.adicionar_animal(a7)

# Z3: 0 variedades (Vacío) - Para el punto c
z3 = Zoologico(3, "Zoo Abandono")

# Z4: 3 variedades (Águila, Loro, Jirafa) - Mismo número de variedades que Z1 (para empate en b)
z4 = Zoologico(4, "Zoo Norte")
z4.adicionar_animal(a3) # Águila
z4.adicionar_animal(a4) # Loro
z4.adicionar_animal(a6) # Jirafa

# Guardar los zoológicos
print("\n--- Guardando registros de Zoológicos ---")
arch_zoo.adicionar(z1)
arch_zoo.adicionar(z2)
arch_zoo.adicionar(z3)
arch_zoo.adicionar(z4)


# ====================================================================
# --- EJECUCIÓN DE LOS PUNTOS ---
# ====================================================================

# --- a) Implementar los métodos crear, modificar y eliminar de ArchZoo ---
print("\n--- a) Modificar y Eliminar ---")
arch_zoo.modificar(4, "Zoo Norte Renovado")
arch_zoo.eliminar(3) # Eliminar el Zoo Abandono (vacío, para que no interfiera con c)


# --- b) Listar los zoológicos que contengan mayor cantidad variedad de animales ---
print("\n--- b) Zoológicos con Mayor Variedad de Animales ---")
# Z2 tiene 4 variedades (Loro, Serpiente, Jirafa, Cocodrilo). Z1 y Z4 tienen 3.
zoos_mayor_variedad = arch_zoo.listarZoologicosMayorVariedad()
if zoos_mayor_variedad:
    max_variedades = zoos_mayor_variedad[0].nroAnimales
    print(f" Zoológicos con la máxima variedad ({max_variedades} variedades):")
    for z in zoos_mayor_variedad:
        print(f"  - {z.nombre} (ID: {z.id})")
else:
    print("No hay zoológicos registrados.")

# Volvemos a añadir el zoo vacío para la prueba c)
z3_nuevo = Zoologico(3, "Zoo Abandono")
arch_zoo.adicionar(z3_nuevo)

# --- c) Listar los zoológicos vacíos y eliminarlos ---
print("\n--- c) Listar Zoológicos Vacíos y Eliminarlos ---")
zoos_vacios_eliminados = arch_zoo.listarZoologicosVaciosYEliminar()
if zoos_vacios_eliminados:
    print(f"Se listaron y eliminaron los siguientes zoológicos vacíos:")
    for z in zoos_vacios_eliminados:
        print(f"  - {z.nombre} (ID: {z.id})")
    
# Verificar que el zoo 3 se haya ido
if not arch_zoo.buscar_por_id(3):
    print(" Verificación: El Zoológico ID 3 (Vacío) fue eliminado del archivo.")


# --- d) Mostrar a los animales de la especie x. ---
print("\n--- d) Animales de la Especie 'Ave' ---")
especie_x = "Ave"
animales_especie = arch_zoo.mostrarAnimalesPorEspecie(especie_x)
if animales_especie:
    print(f"Animales de la especie '{especie_x}':")
    for id_zoo, animales in animales_especie.items():
        zoo_nombre = arch_zoo.buscar_por_id(id_zoo).nombre
        print(f"* En '{zoo_nombre}' (ID: {id_zoo}):")
        for a in animales:
            print(f"  - {a.nombre} ({a.cantidad} individuos)")
else:
    print(f"No se encontraron animales de la especie '{especie_x}'.")


# --- e) Mover los animales de un zoológico x a un zoológico y. ---
print("\n--- e) Mover Animales: Zoo 1 -> Zoo 4 ---")
id_origen = 1 # Zoo Metropolitano (3 variedades: León, Tigre, Águila)
id_destino = 4 # Zoo Norte Renovado (3 variedades: Águila, Loro, Jirafa)
# Águila (a3) ya existe en 4, por lo que su cantidad se sumará. León y Tigre se añadirán.

arch_zoo.moverAnimales(id_origen, id_destino)

# Verificar el resultado
print("\n Inventario Final después del movimiento:")
zoos_final = arch_zoo._cargar_zoologicos()

for z in zoos_final:
    print(f"\n* {z.nombre} (ID: {z.id}, Variedades: {z.nroAnimales}):")
    if not z.animales:
        print("  (Vacío)")
    for a in z.animales:
        print(f"  - {a.nombre} (Cant: {a.cantidad})")