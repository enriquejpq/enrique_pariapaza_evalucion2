import uuid
from datetime import datetime
import math
from ejercicio1.clases.parcela import Parcela

# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, tipo: str, detalle: str):
    """Registra un evento con fecha y detalle en el historial."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "detalle": detalle
    })

class ParcelaRiego(Parcela):
    """Modelo 2 — Parcela con Riego
    Extiende Parcela para incluir gestión de litros y riego automatizado.
    """

    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str,
                 litros_disponibles: float = 0.0, tasa_riego_l_ha: float = 1000.0,
                 umbral_min_litros: float = 0.0):
        
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        
        if tasa_riego_l_ha <= 0:
            raise ValueError("La tasa de riego por hectárea debe ser positiva.")

        # Atributos adicionales protegidos
        self._litros_disponibles = litros_disponibles
        self._tasa_riego_l_ha = tasa_riego_l_ha
        self._umbral_min_litros = umbral_min_litros
        self._estado_riego = 'habilitado' if self.estado == 'activa' else 'inhabilitado'
        self._eventos_riego = []

        registrar_evento(self.historial_eventos, "Inicializacion Riego", f"Riego inicializado. Tasa: {self._tasa_riego_l_ha} L/ha, Umbral: {self._umbral_min_litros} L.")

    # Sobrescribir método de Parcela para aplicar regla de negocio de inhabilitación
    def desactivar(self, motivo: str):
        """Desactiva la parcela y automáticamente el riego."""
        # Llama al método del padre para cambiar el estado de la parcela
        if super().desactivar(motivo): 
            # Regla de negocio: Si la parcela pasa a inactiva, el riego queda automáticamente inhabilitado.
            if self._estado_riego == 'habilitado':
                self._estado_riego = 'inhabilitado'
                registrar_evento(self.historial_eventos, "Riego Automatico", f"Riego inhabilitado automáticamente por desactivación de parcela.")
                print(f"INFO: Riego inhabilitado automáticamente en {self.id_parcela}.")

    # Propiedades de solo lectura para datos adicionales
    @property
    def litros_disponibles(self):
        return round(self._litros_disponibles, 2)

    @property
    def tasa_riego_l_ha(self):
        return self._tasa_riego_l_ha

    @property
    def umbral_min_litros(self):
        return self._umbral_min_litros
    
    @property
    def estado_riego(self):
        return self._estado_riego
    
    @property
    def eventos_riego(self):
        return list(self._eventos_riego)

    # --- Operaciones Adicionales ---

    def configurar_tasa(self, l_ha: float):
        """configurar_tasa(l_ha) -> > 0."""
        if l_ha <= 0:
            print("ERROR: La tasa de riego debe ser mayor a cero L/ha.")
            return
        
        anterior = self._tasa_riego_l_ha
        self._tasa_riego_l_ha = l_ha
        registrar_evento(self.historial_eventos, "Configuracion", f"Tasa de riego modificada de {anterior} L/ha a {l_ha} L/ha.")
        print(f"OK: Tasa de riego configurada a {l_ha} L/ha.")

    def configurar_umbral(self, litros: float):
        """configurar_umbral(litros) -> ≥ 0."""
        if litros < 0:
            print("ERROR: El umbral mínimo de litros no puede ser negativo.")
            return
        
        anterior = self._umbral_min_litros
        self._umbral_min_litros = litros
        registrar_evento(self.historial_eventos, "Configuracion", f"Umbral mínimo ajustado de {anterior} L a {litros} L.")
        print(f"OK: Umbral mínimo configurado a {litros} L.")

    def habilitar_riego(self):
        """habilitar_riego()"""
        if self.estado == 'inactiva':
            print("ERROR: No se puede habilitar el riego, la parcela está inactiva.")
            return

        if self._estado_riego != 'habilitado':
            self._estado_riego = 'habilitado'
            registrar_evento(self.historial_eventos, "Cambio Estado Riego", "Riego habilitado manualmente.")
            print("OK: Riego habilitado.")
        else:
            print("INFO: El riego ya estaba habilitado.")

    def inhabilitar_riego(self):
        """inhabilitar_riego()"""
        if self._estado_riego != 'inhabilitado':
            self._estado_riego = 'inhabilitado'
            registrar_evento(self.historial_eventos, "Cambio Estado Riego", "Riego inhabilitado manualmente.")
            print("OK: Riego inhabilitado.")
        else:
            print("INFO: El riego ya estaba inhabilitado.")

    def cargar_agua(self, litros: float):
        """cargar_agua(litros) -> suma si litros > 0; registra evento de carga."""
        if litros <= 0:
            print("ERROR: La cantidad a cargar debe ser positiva.")
            return

        saldo_antes = self._litros_disponibles
        self._litros_disponibles += litros
        saldo_despues = self._litros_disponibles

        self._eventos_riego.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "litros_solicitados": litros,
            "litros_aplicados": litros, # En una carga, se aplica todo
            "saldo_antes": saldo_antes,
            "saldo_despues": saldo_despues,
            "modo": "Carga"
        })
        print(f"OK: Carga de {litros} L realizada. Nuevo saldo: {saldo_despues:.2f} L.")

    def regar_automatico(self, modo: str):
        """regar_automatico(modo) -> realiza el riego según el modo (estricto o parcial)."""
        
        # --- Reglas de Prohibición ---
        if self.estado == 'inactiva':
            print(f"RECHAZO: Riego no permitido. Parcela {self.id_parcela} está inactiva.")
            return
        if self._estado_riego == 'inhabilitado':
            print("RECHAZO: Riego no permitido. El sistema de riego está inhabilitado.")
            return
        if self._tasa_riego_l_ha <= 0:
            print("RECHAZO: Riego no permitido. Tasa de riego no configurada (> 0).")
            return
        
        # --- Cálculo de Demanda ---
        demanda = self.superficie_ha * self._tasa_riego_l_ha
        saldo_antes = self._litros_disponibles
        litros_a_aplicar = 0.0

        if modo == 'estricto':
            # En estricto: aplica solo si litros_disponibles - demanda >= umbral_min_litros
            saldo_proyectado = saldo_antes - demanda
            if saldo_proyectado >= self._umbral_min_litros:
                litros_a_aplicar = demanda
                print(f"OK (Estricto): Demanda de {demanda:.2f} L aplicada completamente.")
            else:
                print(f"RECHAZO (Estricto): Saldo proyectado ({saldo_proyectado:.2f} L) es menor que el umbral mínimo ({self._umbral_min_litros:.2f} L).")
                registrar_evento(self.historial_eventos, "Riego Fallido", f"Modo estricto rechazado. Demanda: {demanda:.2f} L. Saldo antes: {saldo_antes:.2f} L.")
                return

        elif modo == 'parcial':
            # En parcial: aplica la mayor cantidad posible manteniendo saldo_final >= umbral_min_litros.
            
            # Cantidad máxima que se puede aplicar sin pasar el umbral
            max_aplicable = saldo_antes - self._umbral_min_litros
            
            if max_aplicable <= 0:
                print(f"RECHAZO (Parcial): Saldo actual ({saldo_antes:.2f} L) es insuficiente o igual al umbral ({self._umbral_min_litros:.2f} L).")
                registrar_evento(self.historial_eventos, "Riego Fallido", f"Modo parcial rechazado. Saldo insuficiente para aplicar agua manteniendo umbral.")
                return

            # Aplicamos el mínimo entre la demanda total y lo máximo que podemos aplicar
            litros_a_aplicar = min(demanda, max_aplicable)

            if litros_a_aplicar < demanda:
                print(f"INFO (Parcial): Solo se aplicará una cantidad parcial de {litros_a_aplicar:.2f} L (Demanda: {demanda:.2f} L) para mantener el umbral.")
            else:
                print(f"OK (Parcial): Demanda completa de {demanda:.2f} L aplicada.")
        
        else:
            print("ERROR: Modo de riego no reconocido. Use 'estricto' o 'parcial'.")
            return

        # --- Ejecución y Registro de Descuento ---
        if litros_a_aplicar > 0:
            self._litros_disponibles -= litros_a_aplicar
            saldo_despues = self._litros_disponibles
            
            # El saldo nunca puede quedar negativo (ya validado por max_aplicable en parcial)
            if saldo_despues < 0:
                 saldo_despues = 0 # Falla de lógica, pero forzamos el no negativo

            self._eventos_riego.append({
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "litros_solicitados": demanda,
                "litros_aplicados": round(litros_a_aplicar, 2),
                "saldo_antes": round(saldo_antes, 2),
                "saldo_despues": round(saldo_despues, 2),
                "modo": modo
            })
            print(f"INFO: Saldo final de agua: {saldo_despues:.2f} L. Evento registrado en eventos_riego.")
