import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

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
# --- CLASE DE ENTIDAD ---
# ====================================================================

class Alimento:
    """Representa un alimento con su nombre, fecha de vencimiento y cantidad."""
    def __init__(self, nombre: str, fechaVencimiento: str, cantidad: int):
        self.nombre = nombre
        self.fechaVencimiento = fechaVencimiento # Formato 'YYYY-MM-DD'
        self.cantidad = cantidad

    def __str__(self):
        return f"Alimento(Nombre: {self.nombre}, Vence: {self.fechaVencimiento}, Cantidad: {self.cantidad})"

    def to_dict(self):
        return {"nombre": self.nombre, "fechaVencimiento": self.fechaVencimiento, "cantidad": self.cantidad}

    @staticmethod
    def from_dict(data: dict):
        return Alimento(data['nombre'], data['fechaVencimiento'], data['cantidad'])
    
    def esta_vencido(self) -> bool:
        """Verifica si el alimento ya caducó (fechaVencimiento < fecha actual)."""
        try:
            fecha_venc = datetime.strptime(self.fechaVencimiento, '%Y-%m-%d')
            return fecha_venc < datetime.now()
        except ValueError:
            print(f" Error de formato de fecha en {self.nombre}. Asumiendo no vencido.")
            return False

# ====================================================================
# --- CLASE DE ARCHIVO (GESTORA) ---
# ====================================================================

class ArchRefri:
    """Gestiona la lista de Alimentos en el refrigerador mediante un archivo JSON."""
    def __init__(self, nombre: str):
        self.nombre = nombre # Nombre del archivo

    def crearArchivo(self):
        _guardar_data(self.nombre, [])
        print(f" Archivo '{self.nombre}' creado.")

    def listar(self) -> List[Alimento]:
        data = _cargar_data(self.nombre)
        return [Alimento.from_dict(d) for d in data]

    def _guardar_lista(self, alimentos: List[Alimento]) -> None:
        """Guarda la lista completa de alimentos al archivo JSON."""
        _guardar_data(self.nombre, [a.to_dict() for a in alimentos])

    # --- IMPLEMENTACIÓN DE LOS PUNTOS DEL EJERCICIO 8 ---

    # a) Implementar los métodos para Crear, Modificar por nombre y Eliminar por nombre
    
    # a.1) Crear/Guardar (función análoga a 'guardarProducto' o 'adicionar')
    def guardarAlimento(self, alimento: Alimento):
        """Añade un alimento. Si el nombre ya existe, lo modifica sumando la cantidad."""
        alimentos = self.listar()
        encontrado = False
        
        for a in alimentos:
            if a.nombre.lower() == alimento.nombre.lower():
                # Si existe, actualiza cantidad y fecha (si la nueva es más lejana)
                a.cantidad += alimento.cantidad
                if datetime.strptime(alimento.fechaVencimiento, '%Y-%m-%d') > datetime.strptime(a.fechaVencimiento, '%Y-%m-%d'):
                    a.fechaVencimiento = alimento.fechaVencimiento
                encontrado = True
                print(f" Alimento '{alimento.nombre}' actualizado. Nueva cantidad: {a.cantidad}")
                break

        if not encontrado:
            alimentos.append(alimento)
            print(f" Alimento '{alimento.nombre}' añadido.")

        self._guardar_lista(alimentos)

    # a.2) Modificar por nombre
    def modificarAlimento(self, nombre_antiguo: str, nuevo_nombre: Optional[str] = None, nueva_cantidad: Optional[int] = None, nueva_fecha: Optional[str] = None) -> bool:
        """Modifica los atributos de un alimento buscando por su nombre."""
        alimentos = self.listar()
        encontrado = False
        
        for a in alimentos:
            if a.nombre.lower() == nombre_antiguo.lower():
                if nuevo_nombre is not None:
                    a.nombre = nuevo_nombre
                if nueva_cantidad is not None and nueva_cantidad >= 0:
                    a.cantidad = nueva_cantidad
                if nueva_fecha is not None:
                    # Validar formato de fecha simple 'YYYY-MM-DD'
                    try:
                        datetime.strptime(nueva_fecha, '%Y-%m-%d')
                        a.fechaVencimiento = nueva_fecha
                    except ValueError:
                        print(f" Formato de fecha '{nueva_fecha}' inválido. No se modificó la fecha.")
                        
                encontrado = True
                self._guardar_lista(alimentos)
                print(f"🔄 Alimento '{nombre_antiguo}' modificado.")
                return True
        
        print(f" Alimento '{nombre_antiguo}' no encontrado para modificar.")
        return False

    # a.3) Eliminar por nombre
    def eliminarAlimento(self, nombre_x: str) -> bool:
        """Elimina un alimento del archivo buscando por su nombre."""
        alimentos = self.listar()
        # Creamos una nueva lista excluyendo el alimento a eliminar
        alimentos_antes = len(alimentos)
        alimentos = [a for a in alimentos if a.nombre.lower() != nombre_x.lower()]
        
        if len(alimentos) < alimentos_antes:
            self._guardar_lista(alimentos)
            print(f" Alimento '{nombre_x}' eliminado con éxito.")
            return True
        else:
            print(f" Alimento '{nombre_x}' no encontrado para eliminar.")
            return False

    # b) Mostrar los alimentos que caducaron antes de una fecha dada X
    def mostrarAlimentosCaducadosAntesDe(self, fecha_limite_str: str) -> List[Alimento]:
        """Retorna alimentos cuya fecha de vencimiento es ANTERIOR a la fecha límite X."""
        alimentos = self.listar()
        
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d')
        except ValueError:
            print(" Formato de fecha límite debe ser 'YYYY-MM-DD'.")
            return []

        alimentos_caducados = []
        for a in alimentos:
            try:
                fecha_venc = datetime.strptime(a.fechaVencimiento, '%Y-%m-%d')
                # Un alimento caducó ANTES de la fecha límite si su fecha de vencimiento es anterior (menor)
                if fecha_venc < fecha_limite:
                    alimentos_caducados.append(a)
            except ValueError:
                continue # Ignora alimentos con formato de fecha incorrecto
                
        return alimentos_caducados

    # c) Eliminar los alimentos que tengan cantidad 0
    def eliminarAlimentosCantidadCero(self) -> int:
        """Elimina todos los alimentos cuya cantidad sea igual a 0."""
        alimentos = self.listar()
        
        alimentos_antes = len(alimentos)
        
        # Filtramos solo los que tienen cantidad > 0
        alimentos_final = [a for a in alimentos if a.cantidad > 0]
        
        eliminados = alimentos_antes - len(alimentos_final)
        
        if eliminados > 0:
            self._guardar_lista(alimentos_final)
            print(f"Se eliminaron {eliminados} alimentos con cantidad 0.")
        else:
            print("No se encontraron alimentos con cantidad 0 para eliminar.")
            
        return eliminados

    # d) Buscar los alimentos ya vencidos.
    def buscarAlimentosVencidos(self) -> List[Alimento]:
        """Busca y retorna todos los alimentos cuya fecha de vencimiento ya pasó."""
        alimentos = self.listar()
        return [a for a in alimentos if a.esta_vencido()]

    # e) Mostrar el alimento que tenga más cantidad en el refri.
    def mostrarAlimentoMasCantidad(self) -> Optional[Alimento]:
        """Busca y retorna el alimento con la cantidad más alta."""
        alimentos = self.listar()
        
        if not alimentos:
            return None
        
        # Usamos la función max() con la cantidad como clave
        alimento_mas_cantidad = max(alimentos, key=lambda a: a.cantidad)
        return alimento_mas_cantidad