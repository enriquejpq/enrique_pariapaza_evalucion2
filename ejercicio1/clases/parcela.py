import uuid
from datetime import datetime
import math

# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, tipo: str, detalle: str):
    """Registra un evento con fecha y detalle en el historial."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "detalle": detalle
    })

class Parcela:
    """Modelo 1 — Parcela
    Gestión básica de una parcela agrícola.
    """
    
    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str, estado: str = 'activa'):
        if superficie_ha <= 0:
            raise ValueError("La superficie debe ser un valor positivo.")
        if not cultivo_actual:
            raise ValueError("El cultivo actual no puede estar vacío.")

        # Atributos protegidos (simulación de encapsulamiento con _)
        self._id_parcela = id_parcela
        self._superficie_ha = round(superficie_ha, 2)
        self._cultivo_actual = cultivo_actual
        self._estado = estado
        self._historial_eventos = []

        registrar_evento(self._historial_eventos, "Creacion", f"Parcela creada con {self._superficie_ha} ha y cultivo '{self._cultivo_actual}'.")

    # Propiedades de solo lectura (para acceder a datos mínimos)
    @property
    def id_parcela(self):
        return self._id_parcela
    
    @property
    def superficie_ha(self):
        return self._superficie_ha
    
    @property
    def cultivo_actual(self):
        return self._cultivo_actual
        
    @property
    def estado(self):
        return self._estado
    
    @property
    def historial_eventos(self):
        # Devuelve una copia para evitar modificación directa de la lista
        return list(self._historial_eventos)

    # --- Operaciones ---

    def actualizar_cultivo(self, nuevo_cultivo: str):
        """actualizar_cultivo(nuevo_cultivo) -> valida no vacía; registra en historial."""
        if self._estado == 'inactiva':
            print(f"ERROR: No se puede actualizar el cultivo. La parcela {self.id_parcela} está inactiva.")
            return

        if not nuevo_cultivo or not isinstance(nuevo_cultivo, str):
            print("ERROR: El nuevo cultivo no puede ser una cadena vacía.")
            return
        
        anterior = self._cultivo_actual
        self._cultivo_actual = nuevo_cultivo
        registrar_evento(self._historial_eventos, "Actualizacion", f"Cultivo actualizado de '{anterior}' a '{nuevo_cultivo}'.")
        print(f"OK: Cultivo de la parcela {self.id_parcela} cambiado a '{nuevo_cultivo}'.")

    def activar(self, motivo: str):
        """activar(motivo) -> cambia estado; registra en historial."""
        if self._estado != 'activa':
            self._estado = 'activa'
            registrar_evento(self._historial_eventos, "Cambio Estado", f"Parcela activada. Motivo: {motivo}")
            print(f"OK: Parcela {self.id_parcela} activada. Motivo: {motivo}")
            # Regla de negocio: Si se activa, el riego debería poder habilitarse desde la subclase
            return True
        print(f"INFO: Parcela {self.id_parcela} ya estaba activa.")
        return False

    def desactivar(self, motivo: str):
        """desactivar(motivo) -> cambia estado; registra en historial."""
        if self._estado != 'inactiva':
            self._estado = 'inactiva'
            registrar_evento(self._historial_eventos, "Cambio Estado", f"Parcela desactivada. Motivo: {motivo}")
            print(f"OK: Parcela {self.id_parcela} desactivada. Motivo: {motivo}")
            # Regla de negocio: Si la parcela pasa a inactiva, el riego queda automáticamente inhabilitado (lo maneja la subclase)
            return True
        print(f"INFO: Parcela {self.id_parcela} ya estaba inactiva.")
        return False

    def rectificar_superficie(self, nueva_superficie: float, motivo: str):
        """rectificar_superficie(nueva_superficie, motivo) -> solo > 0; registra valor previo/nuevo."""
        if nueva_superficie <= 0:
            print("ERROR: La nueva superficie debe ser mayor que cero.")
            return

        anterior = self._superficie_ha
        self._superficie_ha = round(nueva_superficie, 2)
        registrar_evento(self._historial_eventos, "Rectificacion Superficie", f"Superficie ajustada de {anterior} ha a {self._superficie_ha} ha. Motivo: {motivo}")
        print(f"OK: Superficie de {self.id_parcela} rectificada a {self._superficie_ha} ha.")