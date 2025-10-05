import uuid
import datetime
import math

# Constantes para el cálculo de volumen
PI = math.pi
VOLUMEN_COEFICIENTE = 4/3 * PI

# Modelo 1 — Cuerpo Celeste (Clase Base)
class CuerpoCeleste:
    """Administra datos mínimos y operaciones para cualquier cuerpo celeste."""
    def __init__(self, nombre: str, masa_kg: float):
        # Validaciones iniciales
        if not nombre:
            raise ValueError("El nombre no puede ser una cadena vacía.")
        if masa_kg <= 0:
            raise ValueError("La masa debe ser un valor positivo (masa_kg > 0).")

        # Encapsulación de atributos
        self._id_celeste = uuid.uuid4()
        self._nombre = nombre
        self._masa_kg = masa_kg
        self._historial_eventos = []
        self._fecha_ultima_masa = datetime.datetime.now()
        self._num_modificaciones = 0

    # Propiedades de solo lectura
    @property
    def id_celeste(self):
        return self._id_celeste

    @property
    def historial_eventos(self):
        # Devolver una copia para evitar modificación directa externa
        return list(self._historial_eventos)
    
    # Propiedades reportables
    @property
    def fecha_ultima_masa(self):
        return self._fecha_ultima_masa

    @property
    def num_modificaciones(self):
        return self._num_modificaciones

    def _registrar_evento(self, campo: str, valor_anterior, nuevo_valor):
        """Registra una actualización en el historial."""
        evento = {
            "fecha_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo_modificado": campo,
            "valor_anterior": valor_anterior,
            "nuevo_valor": nuevo_valor
        }
        self._historial_eventos.append(evento)
        self._num_modificaciones += 1

    # Operaciones

    def actualizar_nombre(self, nuevo_nombre: str):
        """Actualiza el nombre, valida no vacío y registra si hay cambio."""
        if not nuevo_nombre:
            raise ValueError("El nuevo nombre no puede ser una cadena vacía.")
        
        if nuevo_nombre != self._nombre:
            self._registrar_evento("nombre", self._nombre, nuevo_nombre)
            self._nombre = nuevo_nombre

    def actualizar_masa(self, nueva_masa: float):
        """Actualiza la masa, valida > 0 y registra en historial."""
        if nueva_masa <= 0:
            raise ValueError("La nueva masa debe ser un valor positivo (masa_kg > 0).")
        
        if nueva_masa != self._masa_kg:
            self._registrar_evento("masa_kg", self._masa_kg, nueva_masa)
            self._masa_kg = nueva_masa
            self._fecha_ultima_masa = datetime.datetime.now()

    def consultar_ficha(self):
        """Devuelve datos actuales más últimos eventos."""
        ficha = {
            "Tipo": self.__class__.__name__,
            "ID": str(self._id_celeste),
            "Nombre": self._nombre,
            "Masa (kg)": f"{self._masa_kg:.2e}",
            "Última act. masa": self._fecha_ultima_masa.strftime("%Y-%m-%d %H:%M:%S"),
            "Modificaciones": self._num_modificaciones,
            "Últimos Eventos": self.historial_eventos[-3:] # Mostrar los últimos 3
        }
        return ficha
