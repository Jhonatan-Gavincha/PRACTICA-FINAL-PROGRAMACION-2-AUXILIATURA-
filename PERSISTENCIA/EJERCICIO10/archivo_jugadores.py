from jugador import Jugador
import os

class ArchivoJugadores:
    def __init__(self, archivo="jugadores.txt"):
        self.archivo = archivo

    def guardar(self, jugador):
        with open(self.archivo, "a") as f:
            f.write(jugador.to_line())

    def mostrar_todos(self):
        if not os.path.exists(self.archivo):
            print("No hay jugadores registrados.")
            return
        with open(self.archivo, "r") as f:
            for linea in f:
                print(Jugador.from_line(linea))

    def buscar(self, nombre):
        if not os.path.exists(self.archivo):
            print("Archivo no encontrado.")
            return
        with open(self.archivo, "r") as f:
            for linea in f:
                jugador = Jugador.from_line(linea)
                if jugador.nombre.lower() == nombre.lower():
                    print("\nJugador encontrado:\n", jugador)
                    return
        print("No se encontró al jugador.")
