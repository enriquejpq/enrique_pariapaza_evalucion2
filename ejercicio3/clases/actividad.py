from datetime import datetime
from typing import Any

# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, campo: str, anterior: Any, nuevo: Any):
    """Registra un cambio de valor en el historial de eventos."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "campo_modificado": campo,
        "valor_anterior": anterior,
        "valor_nuevo": nuevo
    })

class Actividad:
    """Modelo 1 — Actividad
    Gestión de actividades físicas generales.
    """
    
    def __init__(self, id_actividad: str, nombre: str, duracion_min: int):
        if duracion_min < 1:
            raise ValueError("La duración mínima debe ser de 1 minuto o más.")
        if not nombre:
            raise ValueError("El nombre de la actividad no puede estar vacío.")

        self._id_actividad = id_actividad
        self._nombre = nombre
        self._duracion_min = duracion_min
        self._historial_eventos = []

        registrar_evento(self._historial_eventos, "Creacion", "N/A", f"Nombre: {nombre}, Duracion: {duracion_min} min")

    # Propiedades de solo lectura
    @property
    def id_actividad(self):
        return self._id_actividad
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def duracion_min(self):
        return self._duracion_min
    
    @property
    def historial_eventos(self):
        return list(self._historial_eventos)

    # --- Operaciones ---

    def actualizar_nombre(self, nuevo_nombre: str):
        """actualizar_nombre(nuevo_nombre) -> valida no vacío."""
        if not nuevo_nombre or not isinstance(nuevo_nombre, str):
            print("ERROR: El nuevo nombre no puede ser una cadena vacía.")
            return

        anterior = self._nombre
        self._nombre = nuevo_nombre
        registrar_evento(self._historial_eventos, "Nombre", anterior, nuevo_nombre)
        print(f"OK: Nombre de actividad actualizado de '{anterior}' a '{nuevo_nombre}'.")

    def actualizar_duracion(self, nueva_duracion: int):
        """actualizar_duracion(nueva_duracion) -> valida ≥ 1, registra cambio en historial."""
        if nueva_duracion < 1:
            print("ERROR: La duración mínima aceptada es 1 minuto.")
            return
        
        anterior = self._duracion_min
        self._duracion_min = nueva_duracion
        registrar_evento(self._historial_eventos, "Duracion_min", anterior, nueva_duracion)
        print(f"OK: Duración actualizada de {anterior} min a {nueva_duracion} min.")