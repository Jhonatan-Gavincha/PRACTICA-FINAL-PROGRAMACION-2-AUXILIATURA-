import json
import os
from typing import List, Optional, Dict, Any

# --- CLASE 1: MEDICAMENTO ---
class Medicamento:
    """Representa un medicamento individual."""
    def __init__(self, nombre: str, codMedicamento: int, tipo: str, precio: float):
        self.nombre = nombre
        self.codMedicamento = codMedicamento
        self.tipo = tipo  # Ej: 'Tos', 'Resfrío', 'Dolor'
        self.precio = precio

    def __str__(self):
        return f"Medicamento(Cod: {self.codMedicamento}, Nombre: {self.nombre}, Tipo: {self.tipo}, Precio: ${self.precio:.2f})"

    # Métodos del diagrama
    def getTipo(self) -> str:
        return self.tipo

    def getPrecio(self) -> float:
        return self.precio
    
    # Conversión para JSON
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "codMedicamento": self.codMedicamento,
            "tipo": self.tipo,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data: dict):
        return Medicamento(data['nombre'], data['codMedicamento'], data['tipo'], data['precio'])


# --- CLASE 2: FARMACIA ---
class Farmacia:
    """Representa una sucursal de farmacia con su inventario de medicamentos."""
    def __init__(self, nombreFarmacia: str, sucursal: int, direccion: str):
        self.nombreFarmacia = nombreFarmacia
        self.sucursal = sucursal
        self.direccion = direccion
        self.medicamentos: List[Medicamento] = [] # Adaptación del m[100] a lista dinámica

    def __str__(self):
        return f"Farmacia(Nombre: {self.nombreFarmacia}, Sucursal: {self.sucursal}, Dirección: {self.direccion}, #Med: {len(self.medicamentos)})"

    def adicionar_medicamento(self, m: Medicamento):
        """Añade un medicamento al inventario de la farmacia."""
        if any(med.codMedicamento == m.codMedicamento for med in self.medicamentos):
            print(f"  ⚠️ Código de medicamento {m.codMedicamento} ya existe en Sucursal {self.sucursal}.")
            return
        self.medicamentos.append(m)

    # Métodos del diagrama (simplificados o adaptados)
    def getDireccion(self) -> str:
        return self.direccion

    def getSucursal(self) -> int:
        return self.sucursal

    def mostrarMedicamentos(self, tipo_x: str) -> List[Medicamento]:
        """Muestra/retorna los medicamentos de un tipo específico (Punto a)."""
        return [m for m in self.medicamentos if m.getTipo().lower() == tipo_x.lower()]

    def buscaMedicamento(self, nombre_med: str) -> Optional[Medicamento]:
        """Busca un medicamento por nombre (similar a Punto b)."""
        nombre_med_lower = nombre_med.lower()
        for m in self.medicamentos:
            if m.nombre.lower() == nombre_med_lower:
                return m
        return None
    
    # Conversión para JSON
    def to_dict(self):
        return {
            "nombreFarmacia": self.nombreFarmacia,
            "sucursal": self.sucursal,
            "direccion": self.direccion,
            "medicamentos": [m.to_dict() for m in self.medicamentos]
        }
    
    @staticmethod
    def from_dict(data: dict):
        farmacia = Farmacia(data['nombreFarmacia'], data['sucursal'], data['direccion'])
        farmacia.medicamentos = [Medicamento.from_dict(d) for d in data.get('medicamentos', [])]
        return farmacia


# --- CLASE 3: ARCHFARMACIA ---
class ArchFarmacia:
    """Gestiona el archivo JSON que contiene la lista de Farmacias."""
    def __init__(self, na: str):
        self.na = na # Nombre del archivo

    def _cargar_farmacias(self) -> List[Farmacia]:
        """Carga la lista de Farmacias desde el archivo JSON."""
        if not os.path.exists(self.na):
            self.crearArchivo()

        try:
            with open(self.na, 'r') as f:
                data = json.load(f)
                return [Farmacia.from_dict(d) for d in data]
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f" Error al cargar farmacias del archivo: {e}. Retornando lista vacía.")
            return []

    def _guardar_lista(self, farmacias: List[Farmacia]) -> None:
        """Guarda la lista completa de Farmacias al archivo JSON."""
        data = [f.to_dict() for f in farmacias]
        try:
            with open(self.na, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f" Error al guardar la lista en el archivo: {e}")

    # Métodos del diagrama
    def crearArchivo(self) -> None:
        """Inicializa el archivo JSON con una lista vacía de farmacias."""
        try:
            with open(self.na, 'w') as f:
                json.dump([], f, indent=4)
        except Exception as e:
            print(f" Error al crear el archivo '{self.na}': {e}")
            
    def adicionar(self, f: Farmacia) -> None:
        """Añade una nueva farmacia al archivo, verificando sucursal única."""
        farmacias = self._cargar_farmacias()
        if any(fm.sucursal == f.sucursal for fm in farmacias):
            print(f" Sucursal {f.sucursal} ya existe. No se añadió.")
            return
        
        farmacias.append(f)
        self._guardar_lista(farmacias)
        print(f" Farmacia '{f.nombreFarmacia}' Sucursal {f.sucursal} añadida con éxito.")

    def listar(self) -> List[Farmacia]:
        """Retorna la lista de todas las farmacias."""
        return self._cargar_farmacias()

    def buscar_farmacia_por_sucursal(self, num_sucursal: int) -> Optional[Farmacia]:
        """Retorna una farmacia por su número de sucursal."""
        farmacias = self._cargar_farmacias()
        for f in farmacias:
            if f.getSucursal() == num_sucursal:
                return f
        return None

    # Implementación de los puntos del Ejercicio 5:

    # a) Mostrar los medicamentos para la tos, de la Sucursal número X
    def mostrarMedicamentosTosSucursal(self, num_sucursal: int) -> List[Medicamento]:
        """Busca la sucursal y retorna sus medicamentos de tipo 'Tos'."""
        farmacia = self.buscar_farmacia_por_sucursal(num_sucursal)
        if farmacia:
            return farmacia.mostrarMedicamentos("Tos")
        else:
            print(f"⚠️ Sucursal {num_sucursal} no encontrada.")
            return []

    # b) Mostrar el número de sucursal y su dirección que tienen el medicamento "Tapsin".
    def buscarFarmaciasPorMedicamento(self, nombre_medicamento: str) -> List[Dict[str, Any]]:
        """Retorna una lista de sucursales y direcciones que tienen el medicamento."""
        farmacias = self._cargar_farmacias()
        resultados = []
        for f in farmacias:
            if f.buscaMedicamento(nombre_medicamento):
                resultados.append({
                    "sucursal": f.getSucursal(),
                    "direccion": f.getDireccion()
                })
        return resultados

    # c) Buscar medicamentos por tipo.
    def buscarMedicamentosPorTipo(self, tipo_med: str) -> List[Medicamento]:
        """Busca y retorna todos los medicamentos de un tipo dado, de todas las farmacias."""
        farmacias = self._cargar_farmacias()
        medicamentos_encontrados = []
        for f in farmacias:
            medicamentos_encontrados.extend(f.mostrarMedicamentos(tipo_med))
        return medicamentos_encontrados

    # d) Ordenar las farmacias según su dirección en orden alfabético.
    def ordenarFarmaciasPorDireccion(self) -> List[Farmacia]:
        """Retorna una nueva lista de farmacias ordenada por dirección."""
        farmacias = self._cargar_farmacias()
        # Ordena usando la dirección como clave (key)
        farmacias_ordenadas = sorted(farmacias, key=lambda f: f.getDireccion().lower())
        return farmacias_ordenadas

    # e) Mover los medicamentos de tipo x de la farmacia y a la farmacia z.
    def moverMedicamentosPorTipo(self, tipo_x: str, suc_origen: int, suc_destino: int) -> bool:
        """Mueve medicamentos de tipo x de la sucursal de origen a la de destino."""
        if suc_origen == suc_destino:
            print("⚠️ Las sucursales de origen y destino no pueden ser iguales.")
            return False

        farmacias = self._cargar_farmacias()
        f_origen: Optional[Farmacia] = None
        f_destino: Optional[Farmacia] = None
        
        for f in farmacias:
            if f.getSucursal() == suc_origen:
                f_origen = f
            elif f.getSucursal() == suc_destino:
                f_destino = f
        
        if not f_origen or not f_destino:
            print("⚠️ Una o ambas sucursales no fueron encontradas.")
            return False
            
        movidos = []
        quedan = []
        
        # 1. Separar los medicamentos a mover y los que se quedan en origen
        for m in f_origen.medicamentos:
            if m.getTipo().lower() == tipo_x.lower():
                # 2. Verificar que no haya duplicados en destino antes de mover (por código)
                if not any(dm.codMedicamento == m.codMedicamento for dm in f_destino.medicamentos):
                    movidos.append(m)
                else:
                    print(f"  ⚠️ Medicamento {m.nombre} (Cod: {m.codMedicamento}) ya existe en destino, no se mueve.")
                    quedan.append(m)
            else:
                quedan.append(m)
        
        if not movidos:
            print(f" No se encontraron medicamentos de tipo '{tipo_x}' para mover, o todos ya existen en destino.")
            return False
        
        # 3. Actualizar el inventario de origen
        f_origen.medicamentos = quedan
        
        # 4. Actualizar el inventario de destino
        f_destino.medicamentos.extend(movidos)
        
        # 5. Guardar la lista actualizada de farmacias
        self._guardar_lista(farmacias)
        print(f"✅ Se movieron {len(movidos)} medicamentos de tipo '{tipo_x}' de Sucursal {suc_origen} a Sucursal {suc_destino}.")
        return True