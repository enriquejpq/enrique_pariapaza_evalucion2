from datetime import datetime
from typing import Any

# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, tipo: str, detalle: str, usuario: str = "Sistema"):
    """Registra un evento con fecha, tipo, detalle y usuario."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario,
        "tipo_evento": tipo,
        "detalle": detalle
    })

class Vehiculo:
    """Modelo A — Vehículo
    Gestión de vehículos en el parque de estacionamiento.
    """
    
    def __init__(self, id_vehiculo: str, patente: str, peso_kg: float, usuario: str, estado: str = 'habilitado'):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser positivo.")
        if not patente:
            raise ValueError("La patente no puede estar vacía.")

        self._id_vehiculo = id_vehiculo
        self._patente = patente
        self._peso_kg = peso_kg
        self._estado = estado
        self._historial_eventos = []
        self._usuario_creacion = usuario
        self._conteo_cambios_estado = 0
        self._fecha_ultimo_pesaje = datetime.now()

        registrar_evento(self._historial_eventos, "Creacion", f"Vehículo creado. Peso inicial: {peso_kg} kg.", usuario)

    # Propiedades de solo lectura
    @property
    def id_vehiculo(self):
        return self._id_vehiculo
    
    @property
    def patente(self):
        return self._patente
    
    @property
    def peso_kg(self):
        return self._peso_kg
        
    @property
    def estado(self):
        return self._estado
    
    @property
    def historial_eventos(self):
        return list(self._historial_eventos)
    
    @property
    def conteo_cambios_estado(self):
        return self._conteo_cambios_estado
        
    @property
    def fecha_ultimo_pesaje(self):
        return self._fecha_ultimo_pesaje.strftime("%Y-%m-%d %H:%M:%S")

    # --- Operaciones ---

    def actualizar_peso(self, nuevo_peso_kg: float, usuario: str = "Sistema"):
        """actualizar_peso(nuevo_peso_kg) -> valida > 0; registra en historial."""
        if self._estado == 'inhabilitado':
            print(f"RECHAZO: No se puede actualizar el peso. Vehículo {self.patente} inhabilitado.")
            return

        if nuevo_peso_kg <= 0:
            print("ERROR: El nuevo peso debe ser mayor que cero.")
            return
        
        anterior = self._peso_kg
        self._peso_kg = nuevo_peso_kg
        self._fecha_ultimo_pesaje = datetime.now()
        registrar_evento(self._historial_eventos, "Actualizacion Peso", f"Peso ajustado de {anterior} kg a {nuevo_peso_kg} kg.", usuario)
        print(f"OK: Peso del vehículo {self.patente} actualizado a {nuevo_peso_kg} kg.")

    def habilitar(self, motivo: str, usuario: str = "Sistema"):
        """habilitar(motivo) -> cambia estado; registra en historial."""
        if self._estado != 'habilitado':
            self._estado = 'habilitado'
            self._conteo_cambios_estado += 1
            registrar_evento(self._historial_eventos, "Cambio Estado", f"Vehículo habilitado. Motivo: {motivo}", usuario)
            print(f"OK: Vehículo {self.patente} habilitado. Motivo: {motivo}")
            return True
        print(f"INFO: Vehículo {self.patente} ya estaba habilitado.")
        return False

    def inhabilitar(self, motivo: str, usuario: str = "Sistema"):
        """inhabilitar(motivo) -> cambia estado; registra en historial."""
        if self._estado != 'inhabilitado':
            self._estado = 'inhabilitado'
            self._conteo_cambios_estado += 1
            registrar_evento(self._historial_eventos, "Cambio Estado", f"Vehículo inhabilitado. Motivo: {motivo}", usuario)
            print(f"OK: Vehículo {self.patente} inhabilitado. Motivo: {motivo}")
            return True
        print(f"INFO: Vehículo {self.patente} ya estaba inhabilitado.")
        return False

    def consultar_ficha(self):
        """consultar_ficha() -> devuelve datos actuales y últimas marcas de auditoría."""
        ficha = f"--- Ficha de Vehículo {self.patente} ---\n"
        ficha += f"ID: {self.id_vehiculo} | Estado: {self.estado}\n"
        ficha += f"Peso (kg): {self.peso_kg} | Último Pesaje: {self.fecha_ultimo_pesaje}\n"
        ficha += f"Contador de Cambios de Estado: {self.conteo_cambios_estado}\n"
        
        # Mostrar los 3 últimos eventos
        eventos = self.historial_eventos[-3:]
        ficha += "\nÚltimos Eventos de Auditoría:\n"
        if eventos:
            for e in eventos:
                ficha += f"[{e['fecha']}][{e['usuario']}][{e['tipo_evento']}]: {e['detalle']}\n"
        else:
            ficha += "No hay eventos registrados (solo creación).\n"
        return ficha