from modelo import Estudiante, Nota
from archi_nota import ArchiNota

archivo = ArchiNota()

# b) Agregar varios estudiantes
lista = [
    Nota("Algebra", 85, Estudiante(1,"Juan","Perez","Lopez",19)),
    Nota("Fisica", 95, Estudiante(2,"Ana","Quispe","Mamani",18)),
    Nota("Algebra", 95, Estudiante(3,"Luis","Choque","Rojas",20))
]

archivo.agregar_notas(lista)

print("Promedio General:", archivo.promedio_general())
print("\nMejores notas:", *archivo.mejor_nota(), sep="\n")

archivo.eliminar_por_materia("Algebra")
print("\nArchivo después de eliminar Álgebra:")
for x in archivo.cargar(): print(x)
