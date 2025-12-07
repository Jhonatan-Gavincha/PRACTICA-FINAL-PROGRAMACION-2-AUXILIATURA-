from modelo import Estudiante, Nota
import json, os

class ArchiNota:
    def __init__(self, nombreArchi="notas.json"):
        self.nombreArchi = nombreArchi

    def cargar(self):
        if not os.path.exists(self.nombreArchi): return []
        with open(self.nombreArchi, "r") as f:
            data = json.load(f)
            return [Nota.from_dict(n) for n in data]

    def guardar(self, lista):
        with open(self.nombreArchi, "w") as f:
            json.dump([n.to_dict() for n in lista], f, indent=4)

    # b) Agregar varios estudiantes con notas
    def agregar_notas(self, listaNotas):
        data = self.cargar()
        data.extend(listaNotas)
        self.guardar(data)

    # c) Promedio general de notas
    def promedio_general(self):
        datos = self.cargar()
        if not datos: return 0
        return sum(n.notaFinal for n in datos) / len(datos)

    # d) Mejor(es) nota(s)
    def mejor_nota(self):
        datos = self.cargar()
        if not datos: return []
        max_nota = max(n.notaFinal for n in datos)
        return [n for n in datos if n.notaFinal == max_nota]

    # e) Eliminar estudiantes por materia
    def eliminar_por_materia(self, materia):
        datos = self.cargar()
        nuevos = [n for n in datos if n.materia.lower() != materia.lower()]
        self.guardar(nuevos)
