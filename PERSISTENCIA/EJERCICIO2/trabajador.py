import json
import os
from typing import List, Optional

# --- Definición de la Clase Trabajador ---
class Trabajador:
    """Representa un trabajador individual con nombre, carnet y salario."""
    def __init__(self, nombre: str, carnet: int, salario: float):
        self.nombre = nombre
        self.carnet = carnet
        self.salario = salario

    def __str__(self):
        # Representación en cadena para imprimir el objeto
        return f"Trabajador(Nombre: {self.nombre}, Carnet: {self.carnet}, Salario: {self.salario:.2f})"
    
    def to_dict(self):
        # Método para convertir el objeto a diccionario (útil para guardar en JSON)
        return {
            "nombre": self.nombre,
            "carnet": self.carnet,
            "salario": self.salario
        }
    
    @staticmethod
    def from_dict(data: dict):
        # Método estático para crear un objeto Trabajador a partir de un diccionario
        return Trabajador(data['nombre'], data['carnet'], data['salario'])

# --- Definición de la Clase ArchivoTrabajador ---
class ArchivoTrabajador:
    """Gestiona la colección de Trabajadores y la persistencia de datos usando JSON."""
    def __init__(self, nombre_arch: str):
        self.nombre_arch = nombre_arch

    # a) Implementa un método para crear y guardar el archivo.
    def crearArchivo(self) -> None:
        """Inicializa el archivo JSON con una lista vacía de trabajadores."""
        try:
            with open(self.nombre_arch, 'w') as f:
                json.dump([], f, indent=4)
            print(f"✅ Archivo '{self.nombre_arch}' creado y guardado con éxito.")
        except Exception as e:
            print(f"❌ Error al crear el archivo: {e}")

    def _cargar_trabajadores(self) -> List[Trabajador]:
        """Método interno para cargar la lista de Trabajadores desde el archivo JSON."""
        if not os.path.exists(self.nombre_arch):
            self.crearArchivo()

        try:
            with open(self.nombre_arch, 'r') as f:
                data = json.load(f)
                return [Trabajador.from_dict(d) for d in data]
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            # Maneja archivos corruptos o vacíos
            print(f"❌ Error al cargar trabajadores del archivo: {e}. Retornando lista vacía.")
            return []

    def _guardar_lista(self, trabajadores: List[Trabajador]) -> None:
        """Método interno para guardar la lista completa de Trabajadores al archivo JSON."""
        data = [t.to_dict() for t in trabajadores]
        try:
            with open(self.nombre_arch, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"❌ Error al guardar la lista en el archivo: {e}")

    # b) Implementa un método para guardar trabajadores.
    def guardarTrabajador(self, t: Trabajador) -> None:
        """Carga la lista, añade el nuevo trabajador y guarda la lista de vuelta al archivo."""
        trabajadores = self._cargar_trabajadores()
        
        if any(tr.carnet == t.carnet for tr in trabajadores):
            print(f"⚠️ Trabajador con carnet {t.carnet} ya existe. No se añadió.")
            return

        trabajadores.append(t)
        self._guardar_lista(trabajadores)
        print(f"➕ Trabajador '{t.nombre}' guardado con éxito.")

    # c) Implementa un método para aumentar el salario de un trabajador t.
    def aumentaSalario(self, aumento: float, carnet_t: int) -> bool:
        """Aumenta el salario del trabajador identificado por su carnet."""
        trabajadores = self._cargar_trabajadores()
        encontrado = False
        
        for t in trabajadores:
            if t.carnet == carnet_t:
                salario_original = t.salario
                t.salario += aumento
                encontrado = True
                print(f"📈 Salario de '{t.nombre}' (Carnet {carnet_t}) aumentado de ${salario_original:.2f} a ${t.salario:.2f}.")
                break
        
        if encontrado:
            self._guardar_lista(trabajadores)
            return True
        else:
            print(f"⚠️ Trabajador con carnet {carnet_t} no encontrado.")
            return False

    # d) Buscar el trabajador con el mayor salario.
    def buscarMayorSalario(self) -> Optional[Trabajador]:
        """Busca y retorna el trabajador con el salario más alto."""
        trabajadores = self._cargar_trabajadores()
        
        if not trabajadores:
            return None
        
        trabajador_mayor_salario = max(trabajadores, key=lambda t: t.salario)
        return trabajador_mayor_salario

    # e) Ordenar a los trabajadores por su salario.
    def ordenarPorSalario(self, ascendente: bool = False) -> List[Trabajador]:
        """Retorna una nueva lista de trabajadores ordenada por salario."""
        trabajadores = self._cargar_trabajadores()
        
        trabajadores_ordenados = sorted(trabajadores, key=lambda t: t.salario, reverse=not ascendente)
        return trabajadores_ordenados