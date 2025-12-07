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

# ====================================================================
# --- CLASE 1: ANIMAL ---
# ====================================================================

class Animal:
    """Representa un grupo de animales de una especie en un zoológico."""
    def __init__(self, especie: str, nombre: str, cantidad: int):
        self.especie = especie # Ej: Mamífero, Ave, Reptil
        self.nombre = nombre   # Ej: León, Águila, Serpiente
        self.cantidad = cantidad # Número de individuos de esta especie/nombre

    def __str__(self):
        return f"Animal(Nombre: {self.nombre}, Especie: {self.especie}, Cantidad: {self.cantidad})"

    def to_dict(self):
        return {"especie": self.especie, "nombre": self.nombre, "cantidad": self.cantidad}

    @staticmethod
    def from_dict(data: dict):
        return Animal(data['especie'], data['nombre'], data['cantidad'])

# ====================================================================
# --- CLASE 2: ZOOLOGICO ---
# ====================================================================

class Zoologico:
    """Representa un zoológico con su inventario de animales."""
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre
        self.animales: List[Animal] = [] # Adaptación del arreglo estático animales[30]
        self.nroAnimales = 0 # Número de *variedades* de animales (especies/nombres únicos)

    def __str__(self):
        total_individuos = sum(a.cantidad for a in self.animales)
        return f"Zoologico(ID: {self.id}, Nombre: {self.nombre}, Variedades: {self.nroAnimales}, Total Indiv: {total_individuos})"

    def adicionar_animal(self, a: Animal):
        """Añade una variedad de animal o actualiza la cantidad si ya existe por nombre."""
        encontrado = False
        for animal in self.animales:
            if animal.nombre.lower() == a.nombre.lower():
                animal.cantidad += a.cantidad
                encontrado = True
                break
        
        if not encontrado:
            self.animales.append(a)
            self.nroAnimales = len(self.animales)

    # Métodos auxiliares
    def obtener_variedad_por_nombre(self, nombre_animal: str) -> Optional[Animal]:
        """Busca una variedad de animal por su nombre."""
        for a in self.animales:
            if a.nombre.lower() == nombre_animal.lower():
                return a
        return None
    
    def obtener_animales_por_especie(self, especie_x: str) -> List[Animal]:
        """Retorna todos los animales que pertenecen a una especie dada."""
        return [a for a in self.animales if a.especie.lower() == especie_x.lower()]

    # Conversión para JSON
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nroAnimales": self.nroAnimales,
            "animales": [a.to_dict() for a in self.animales]
        }
    
    @staticmethod
    def from_dict(data: dict):
        zoo = Zoologico(data['id'], data['nombre'])
        zoo.animales = [Animal.from_dict(d) for d in data.get('animales', [])]
        zoo.nroAnimales = len(zoo.animales) # Recalculamos nroAnimales al cargar
        return zoo

# ====================================================================
# --- CLASE 3: ARCHZOO ---
# ====================================================================

class ArchZoo:
    """Gestiona el archivo JSON que contiene la lista de Zoologicos."""
    def __init__(self, nombre: str):
        self.nombre = nombre # Nombre del archivo

    def _cargar_zoologicos(self) -> List[Zoologico]:
        """Carga la lista de Zoologicos desde el archivo JSON."""
        if not os.path.exists(self.nombre):
            self.crearArchivo()

        try:
            data = _cargar_data(self.nombre)
            return [Zoologico.from_dict(d) for d in data]
        except Exception:
            return []

    def _guardar_lista(self, zoologicos: List[Zoologico]) -> None:
        """Guarda la lista completa de Zoologicos al archivo JSON."""
        _guardar_data(self.nombre, [z.to_dict() for z in zoologicos])

    # Métodos auxiliares y del diagrama
    def crearArchivo(self) -> None:
        """Inicializa el archivo JSON con una lista vacía de zoológicos."""
        _guardar_data(self.nombre, [])
        print(f"✅ Archivo '{self.nombre}' creado.")

    def buscar_por_id(self, zoo_id: int) -> Optional[Zoologico]:
        """Busca un zoológico por su ID."""
        zoologicos = self._cargar_zoologicos()
        return next((z for z in zoologicos if z.id == zoo_id), None)

    # --- IMPLEMENTACIÓN DE LOS PUNTOS DEL EJERCICIO 9 ---

    # a) Implementar los métodos crear, modificar y eliminar de ArchZoo
    
    # a.1) Crear (adicionar)
    def adicionar(self, z: Zoologico) -> None:
        """Añade un nuevo zoológico al archivo, verificando ID único."""
        zoologicos = self._cargar_zoologicos()
        if any(zoo.id == z.id for zoo in zoologicos):
            print(f"⚠️ Zoológico con ID {z.id} ya existe. No se añadió.")
            return
        
        zoologicos.append(z)
        self._guardar_lista(zoologicos)
        print(f"➕ Zoológico '{z.nombre}' (ID: {z.id}) añadido con éxito.")

    # a.2) Modificar (modifica el nombre del zoológico por su ID)
    def modificar(self, zoo_id: int, nuevo_nombre: str) -> bool:
        """Modifica el nombre del zoológico identificado por su ID."""
        zoologicos = self._cargar_zoologicos()
        encontrado = False
        
        for z in zoologicos:
            if z.id == zoo_id:
                z.nombre = nuevo_nombre
                encontrado = True
                break
        
        if encontrado:
            self._guardar_lista(zoologicos)
            print(f"🔄 Zoológico ID {zoo_id} modificado a '{nuevo_nombre}'.")
            return True
        else:
            print(f" Zoológico ID {zoo_id} no encontrado para modificar.")
            return False

    # a.3) Eliminar
    def eliminar(self, zoo_id: int) -> bool:
        """Elimina un zoológico del archivo buscando por su ID."""
        zoologicos = self._cargar_zoologicos()
        
        zoologicos_antes = len(zoologicos)
        zoologicos = [z for z in zoologicos if z.id != zoo_id]
        
        if len(zoologicos) < zoologicos_antes:
            self._guardar_lista(zoologicos)
            print(f" Zoológico ID {zoo_id} eliminado con éxito.")
            return True
        else:
            print(f" Zoológico ID {zoo_id} no encontrado para eliminar.")
            return False

    # b) Listar los zoológicos que contengan mayor cantidad variedad de animales
    def listarZoologicosMayorVariedad(self) -> List[Zoologico]:
        """Retorna los zoológicos con la máxima cantidad de variedades de animales (nroAnimales)."""
        zoologicos = self._cargar_zoologicos()
        
        if not zoologicos:
            return []
            
        # 1. Encontrar la cantidad máxima de variedades
        max_variedades = max(z.nroAnimales for z in zoologicos)
        
        # 2. Filtrar todos los zoológicos que igualan esa cantidad máxima
        return [z for z in zoologicos if z.nroAnimales == max_variedades]

    # c) Listar los zoológicos vacíos y eliminarlos
    def listarZoologicosVaciosYEliminar(self) -> List[Zoologico]:
        """Identifica los zoológicos que tienen 0 variedades de animales y los elimina."""
        zoologicos_actuales = self._cargar_zoologicos()
        vacios = [z for z in zoologicos_actuales if z.nroAnimales == 0]
        
        if not vacios:
            print("No se encontraron zoológicos vacíos para eliminar.")
            return []

        # Crear la lista final excluyendo los vacíos
        zoologicos_final = [z for z in zoologicos_actuales if z.nroAnimales > 0]
        
        self._guardar_lista(zoologicos_final)
        print(f" Se eliminaron {len(vacios)} zoológicos vacíos.")
        
        return vacios

    # d) Mostrar a los animales de la especie x.
    def mostrarAnimalesPorEspecie(self, especie_x: str) -> Dict[int, List[Animal]]:
        """Retorna un diccionario de {ID_Zoo: Lista de Animales} de la especie x."""
        zoologicos = self._cargar_zoologicos()
        resultados = {}
        
        for z in zoologicos:
            animales_especie = z.obtener_animales_por_especie(especie_x)
            if animales_especie:
                resultados[z.id] = animales_especie
                
        return resultados

    # e) Mover los animales de un zoológico x a un zoológico y.
    # Interpretación: Mover *TODAS* las variedades de animales del zoo x al zoo y.
    def moverAnimales(self, id_origen: int, id_destino: int) -> bool:
        """Mueve todas las variedades de animales del zoológico de origen al de destino."""
        if id_origen == id_destino:
            print(" Los IDs de origen y destino no pueden ser iguales.")
            return False

        zoologicos = self._cargar_zoologicos()
        z_origen: Optional[Zoologico] = None
        z_destino: Optional[Zoologico] = None
        
        for z in zoologicos:
            if z.id == id_origen:
                z_origen = z
            elif z.id == id_destino:
                z_destino = z
        
        if not z_origen or not z_destino:
            print(" Uno o ambos zoológicos no fueron encontrados.")
            return False

        animales_a_mover = z_origen.animales.copy()
        
        if not animales_a_mover:
            print(f" Zoológico '{z_origen.nombre}' está vacío. Nada que mover.")
            return False
            
        # 1. Mover: Adicionar al destino
        for a in animales_a_mover:
            z_destino.adicionar_animal(a)
            
        # 2. Vaciar el zoológico de origen
        z_origen.animales = []
        z_origen.nroAnimales = 0
        
        # 3. Guardar la lista actualizada
        self._guardar_lista(zoologicos)
        print(f" Se movieron {len(animales_a_mover)} variedades de animales de '{z_origen.nombre}' (ID: {id_origen}) a '{z_destino.nombre}' (ID: {id_destino}).")
        return True