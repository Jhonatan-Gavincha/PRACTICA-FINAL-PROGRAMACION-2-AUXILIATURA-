from jugador import Jugador
from archivo_jugadores import ArchivoJugadores

archivo = ArchivoJugadores()

while True:
    print("\n--- GESTIÓN DE JUGADORES ---")
    print("1. Registrar jugador")
    print("2. Mostrar todos")
    print("3. Buscar por nombre")
    print("4. Salir")

    op = input("Elige una opción: ")

    if op == "1":
        nom = input("Nombre: ")
        niv = int(input("Nivel: "))
        pun = int(input("Puntaje: "))
        archivo.guardar(Jugador(nom, niv, pun))
        print("Jugador guardado exitosamente.")

    elif op == "2":
        archivo.mostrar_todos()

    elif op == "3":
        nombre = input("Nombre del jugador a buscar: ")
        archivo.buscar(nombre)

    elif op == "4":
        break
    else:
        print("Opción no válida.")
