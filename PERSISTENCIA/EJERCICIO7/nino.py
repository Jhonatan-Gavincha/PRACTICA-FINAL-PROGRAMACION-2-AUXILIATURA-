import json
import os
from typing import List, Optional, Dict, Any

# --- Helpers de Persistencia JSON ---
def _cargar_data(nombre_archivo: str) -> List[Dict[str, Any]]:
    """Carga datos crudos (lista de diccionarios) desde un archivo JSON."""
    if not os.path.exists(nombre_archivo):
        return []
    try:
        with open(nombre_archivo, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return []

def _guardar_data(nombre_archivo: str, data: List[Dict[str, Any]]) -> None:
    """Guarda una lista de diccionarios a un archivo JSON."""
    try:
        with open(nombre_archivo, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f" Error al guardar en {nombre_archivo}: {e}")

# --- TABLA DE REFERENCIA FICTICIA (Simplificada para el ejercicio) ---
# Peso Mínimo Aceptable (PMA) y Talla Mínima Aceptable (TMA) según la edad.
# El peso y talla se almacenan como cadenas (ej: "15 kg", "110 cm"), por lo que convertiremos a float.
RANGOS_ADECUADOS = {
    # Edad: (Peso Mínimo kg, Talla Mínima cm)
    3: (13.0, 90.0),   # 3 años: 13.0 kg, 90 cm
    4: (15.0, 100.0),  # 4 años: 15.0 kg, 100 cm
    5: (17.0, 105.0),  # 5 años: 17.0 kg, 105 cm
    6: (19.0, 110.0),  # 6 años: 19.0 kg, 110 cm
    7: (21.0, 115.0),  # 7 años: 21.0 kg, 115 cm
}

# ====================================================================
# --- CLASES DE ENTIDAD (Con Herencia) ---
# ====================================================================

class Persona:
    """Clase base que representa una persona."""
    def __init__(self, nombre: str, apellidoPaterno: str, apellidoMaterno: str, ci: int):
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.ci = ci

    def get_nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellidoPaterno} {self.apellidoMaterno}"

    def get_ci(self) -> int:
        return self.ci

    # Método base para la conversión a diccionario (usado por Niño)
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellidoPaterno": self.apellidoPaterno,
            "apellidoMaterno": self.apellidoMaterno,
            "ci": self.ci
        }

class Nino(Persona):
    """Clase que hereda de Persona y añade atributos específicos."""
    def __init__(self, nombre: str, apellidoPaterno: str, apellidoMaterno: str, ci: int,
                 edad: int, peso: str, talla: str):
        super().__init__(nombre, apellidoPaterno, apellidoMaterno, ci)
        self.edad = edad
        self.peso = peso   # Ej: "15 kg"
        self.talla = talla # Ej: "110 cm"

    def __str__(self):
        return f"Niño(Nombre: {self.get_nombre_completo()}, CI: {self.ci}, Edad: {self.edad}, Peso: {self.peso}, Talla: {self.talla})"

    # Métodos para obtener valores numéricos
    def _get_peso_kg(self) -> float:
        """Extrae el valor numérico del peso (ej: "15 kg" -> 15.0)."""
        try:
            return float(self.peso.split()[0])
        except (ValueError, IndexError):
            return 0.0

    def _get_talla_cm(self) -> float:
        """Extrae el valor numérico de la talla (ej: "110 cm" -> 110.0)."""
        try:
            return float(self.talla.split()[0])
        except (ValueError, IndexError):
            return 0.0

    def to_dict(self):
        # Combina atributos de Persona y Niño
        data = super().to_dict()
        data.update({
            "edad": self.edad,
            "peso": self.peso,
            "talla": self.talla
        })
        return data

    @staticmethod
    def from_dict(data: dict):
        return Nino(
            data['nombre'], data['apellidoPaterno'], data['apellidoMaterno'], data['ci'],
            data['edad'], data['peso'], data['talla']
        )

# ====================================================================
# --- CLASE DE ARCHIVO (GESTORA) ---
# ====================================================================

class ArchNino:
    def __init__(self, na: str):
        self.na = na # Nombre del archivo

    def crearArchivo(self):
        _guardar_data(self.na, [])

    def listar(self) -> List[Nino]:
        data = _cargar_data(self.na)
        return [Nino.from_dict(d) for d in data]

    # Implementación para el punto a) - Crear, leer, listar y mostrar
    def guardar(self, nino: Nino):
        """Guarda un nuevo registro de niño en el archivo."""
        ninos = self.listar()
        if any(n.ci == nino.ci for n in ninos):
            print(f" Niño con carnet {nino.ci} ya existe. No se añadió.")
            return

        ninos.append(nino)
        _guardar_data(self.na, [n.to_dict() for n in ninos])
        print(f" Niño '{nino.nombre}' (CI: {nino.ci}) guardado.")

    def leer(self, nino: Nino):
        """Simula la acción de 'leer' (cargar) un niño existente basado en CI."""
        return self.buscar_por_ci(nino.ci)

    def listar_y_mostrar(self) -> List[Nino]:
        """Lista y muestra todos los niños registrados."""
        ninos = self.listar()
        print(f"\ Lista de {len(ninos)} niños en el archivo:")
        for n in ninos:
            print(f"  - {n}")
        return ninos

    # --- IMPLEMENTACIÓN DE LOS PUNTOS DEL EJERCICIO 7 ---

    # Método auxiliar para evaluar rangos (basado en RANGOS_ADECUADOS)
    def es_adecuado(self, nino: Nino) -> bool:
        """Evalúa si el peso y la talla del niño son adecuados para su edad (según tabla ficticia)."""
        if nino.edad not in RANGOS_ADECUADOS:
            # Si la edad no está en la tabla, asumimos que no podemos evaluarlo o está fuera de rango
            return False 

        min_peso_kg, min_talla_cm = RANGOS_ADECUADOS[nino.edad]
        peso_actual = nino._get_peso_kg()
        talla_actual = nino._get_talla_cm()
        
        # Consideramos adecuado si el peso actual es MAYOR o IGUAL al mínimo, 
        # y la talla actual es MAYOR o IGUAL a la mínima.
        return peso_actual >= min_peso_kg and talla_actual >= min_talla_cm

    # b) Cuántos niños tienen el peso adecuado de acuerdo a su talla y edad
    def contarNinosAdecuados(self) -> int:
        """Cuenta cuántos niños cumplen con el peso y talla adecuados para su edad."""
        ninos = self.listar()
        contador = 0
        for n in ninos:
            if self.es_adecuado(n):
                contador += 1
        return contador

    # c) Mostrar a los niños que de acuerdo a la edad no tienen el peso o la talla adecuada.
    def mostrarNinosNoAdecuados(self) -> List[Nino]:
        """Retorna la lista de niños que no cumplen con los rangos adecuados."""
        ninos = self.listar()
        return [n for n in ninos if not self.es_adecuado(n)]

    # d) Determinar el promedio de edad en los niños.
    def determinarPromedioEdad(self) -> float:
        """Calcula el promedio de edad de todos los niños registrados."""
        ninos = self.listar()
        if not ninos:
            return 0.0
            
        suma_edades = sum(n.edad for n in ninos)
        return suma_edades / len(ninos)

    # e) Buscar al niño con el carnet x.
    def buscar_por_ci(self, ci_x: int) -> Optional[Nino]:
        """Busca y retorna un niño por su número de carnet (CI)."""
        ninos = self.listar()
        return next((n for n in ninos if n.ci == ci_x), None)

    # f) Mostrar a los niños con la talla más alta.
    def mostrarNinosTallaMasAlta(self) -> List[Nino]:
        """Retorna una lista de niños que tienen la talla más alta."""
        ninos = self.listar()
        if not ninos:
            return []
            
        # 1. Encontrar la talla máxima
        talla_maxima = max(n._get_talla_cm() for n in ninos)
        
        # 2. Filtrar todos los niños que tienen esa talla
        return [n for n in ninos if n._get_talla_cm() == talla_maxima]