class Jugador:
    def __init__(self, nombre, nivel, puntaje):
        self.nombre = nombre
        self.nivel = nivel
        self.puntaje = puntaje

    def to_line(self):
        return f"{self.nombre},{self.nivel},{self.puntaje}\n"

    @staticmethod
    def from_line(linea):
        nombre, nivel, puntaje = linea.strip().split(",")
        return Jugador(nombre, int(nivel), int(puntaje))

    def __str__(self):
        return f"Jugador: {self.nombre} | Nivel: {self.nivel} | Puntaje: {self.puntaje}"
