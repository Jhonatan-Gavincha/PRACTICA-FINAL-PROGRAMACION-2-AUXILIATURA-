import json
import os

class Charango:
    def __init__(self, material, cuerdas):
        self.material = material
        self.cuerdas = cuerdas
        self.nroCuerdas = len(cuerdas)

    def contar_malas(self):
        return sum(1 for c in self.cuerdas if not c)

    def to_dict(self):
        return {
            "material": self.material,
            "nroCuerdas": self.nroCuerdas,
            "cuerdas": self.cuerdas
        }

    @staticmethod
    def from_dict(data):
        return Charango(data["material"], data["cuerdas"])


class ArchivoCharango:
    archivo = "charangos.json"

    # Cargar archivo
    @staticmethod
    def cargar():
        if not os.path.exists(ArchivoCharango.archivo):
            return []
        with open(ArchivoCharango.archivo, "r") as f:
            data = json.load(f)
            return [Charango.from_dict(d) for d in data]

    # Guardar en archivo
    @staticmethod
    def guardar(lista):
        with open(ArchivoCharango.archivo, "w") as f:
            json.dump([c.to_dict() for c in lista], f, indent=4)

    # Agregar objeto
    @staticmethod
    def agregar(charango):
        lista = ArchivoCharango.cargar()
        lista.append(charango)
        ArchivoCharango.guardar(lista)

    # b) Eliminar charangos con más de 6 cuerdas malas
    @staticmethod
    def eliminar_malos():
        lista = ArchivoCharango.cargar()
        lista = [c for c in lista if c.contar_malas() <= 6]
        ArchivoCharango.guardar(lista)

    # c) Listar por material
    @staticmethod
    def listar_material(mat):
        for c in ArchivoCharango.cargar():
            if c.material.lower() == mat.lower():
                print(c.to_dict())

    # d) Buscar con 10 cuerdas
    @staticmethod
    def buscar_10():
        for c in ArchivoCharango.cargar():
            if c.nroCuerdas == 10:
                print(c.to_dict())

    # e) Ordenar alfabéticamente por material
    @staticmethod
    def ordenar():
        lista = ArchivoCharango.cargar()
        lista.sort(key=lambda c: c.material.lower())
        ArchivoCharango.guardar(lista)
