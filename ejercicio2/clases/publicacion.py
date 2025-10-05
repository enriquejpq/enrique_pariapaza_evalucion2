from datetime import datetime
import math

# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, campo: str, anterior: Any, nuevo: Any):
    """Registra un cambio de valor en el historial de eventos."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "campo_modificado": campo,
        "valor_anterior": anterior,
        "valor_nuevo": nuevo
    })

class Publicacion:
    """Modelo 1 — Publicación
    Gestión básica de publicaciones con validación de año.
    """
    
    MIN_ANIO_IMPRENTA = 1450

    def __init__(self, id_publicacion: str, titulo: str, anio: int):
        if anio < self.MIN_ANIO_IMPRENTA:
            raise ValueError(f"ERROR: El año ({anio}) debe ser posterior o igual a {self.MIN_ANIO_IMPRENTA}.")
        if not titulo:
            raise ValueError("ERROR: El título no puede estar vacío.")

        self._id_publicacion = id_publicacion
        self._titulo = titulo
        self._anio = anio
        self._historial_eventos = []

        registrar_evento(self._historial_eventos, "Inicializacion", "N/A", f"Título: {titulo}, Año: {anio}")

    # Propiedades de solo lectura
    @property
    def id_publicacion(self):
        return self._id_publicacion
    
    @property
    def titulo(self):
        return self._titulo
    
    @property
    def anio(self):
        return self._anio
    
    @property
    def historial_eventos(self):
        return list(self._historial_eventos)

    # --- Operaciones ---

    def actualizar_titulo(self, nuevo_titulo: str):
        """actualizar_titulo(nuevo_titulo) -> valida que no sea vacío."""
        if not nuevo_titulo or not isinstance(nuevo_titulo, str):
            print("ERROR: El nuevo título no puede ser una cadena vacía.")
            return

        anterior = self._titulo
        self._titulo = nuevo_titulo
        registrar_evento(self._historial_eventos, "Titulo", anterior, nuevo_titulo)
        print(f"OK: Título actualizado de '{anterior}' a '{nuevo_titulo}'.")

    def actualizar_anio(self, nuevo_anio: int):
        """actualizar_anio(nuevo_anio) -> valida ≥ 1450; registra en historial."""
        if nuevo_anio < self.MIN_ANIO_IMPRENTA:
            print(f"ERROR: El año de publicación ({nuevo_anio}) debe ser posterior o igual a {self.MIN_ANIO_IMPRENTA}.")
            return
        
        anterior = self._anio
        self._anio = nuevo_anio
        registrar_evento(self._historial_eventos, "Anio", anterior, nuevo_anio)
        print(f"OK: Año actualizado de {anterior} a {nuevo_anio}.")

