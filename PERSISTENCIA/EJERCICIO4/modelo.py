import json
import os

class Estudiante:
    def __init__(self, ru, nombre, paterno, materno, edad):
        self.ru = ru
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.edad = edad

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Estudiante(data['ru'], data['nombre'], data['paterno'], data['materno'], data['edad'])

    def __str__(self):
        return f"{self.nombre} {self.paterno} {self.materno} (RU:{self.ru})"


class Nota:
    def __init__(self, materia, notaFinal, estudiante: Estudiante):
        self.materia = materia
        self.notaFinal = notaFinal
        self.estudiante = estudiante

    def to_dict(self):
        return {
            "materia": self.materia,
            "notaFinal": self.notaFinal,
            "estudiante": self.estudiante.to_dict()
        }

    @staticmethod
    def from_dict(data):
        est = Estudiante.from_dict(data["estudiante"])
        return Nota(data['materia'], data['notaFinal'], est)

    def __str__(self):
        return f"{self.estudiante} - {self.materia}: {self.notaFinal}"
