from charango import Charango, ArchivoCharango

# Crear charangos
c1 = Charango("Madera",  [True,True,False,False,False,False,False,False,False,False])
c2 = Charango("Nogal",   [True]*10)
c3 = Charango("Roble",   [True,True,True,False,True,True,True,True,True,True])

# Guardar objetos
ArchivoCharango.agregar(c1)
ArchivoCharango.agregar(c2)
ArchivoCharango.agregar(c3)

print("=== Lista inicial ===")
print([c.to_dict() for c in ArchivoCharango.cargar()])

print("\nEliminando charangos con más de 6 cuerdas malas...")
ArchivoCharango.eliminar_malos()

print("\nCharangos con material 'Nogal':")
ArchivoCharango.listar_material("Nogal")

print("\nCharangos con 10 cuerdas:")
ArchivoCharango.buscar_10()

print("\nOrdenando por material:")
ArchivoCharango.ordenar()
print([c.to_dict() for c in ArchivoCharango.cargar()])
