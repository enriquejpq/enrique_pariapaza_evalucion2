from datetime import datetime
import math
from ejercicio2.clases.publicacion import Publicacion
# --- Función de utilidad de auditoría (local para este ejemplo) ---
def registrar_evento(historial: list, campo: str, anterior: Any, nuevo: Any):
    """Registra un cambio de valor en el historial de eventos."""
    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "campo_modificado": campo,
        "valor_anterior": anterior,
        "valor_nuevo": nuevo
    })

class Libro(Publicacion):
    """Modelo 2 — Libro
    Extiende Publicacion para añadir control de progreso de lectura.
    """

    def __init__(self, id_publicacion: str, titulo: str, anio: int, paginas_totales: int):
        if paginas_totales <= 0:
            raise ValueError("ERROR: El número total de páginas debe ser positivo.")

        super().__init__(id_publicacion, titulo, anio)
        
        # Atributos adicionales protegidos
        self._paginas_totales = paginas_totales
        self._paginas_leidas = 0
        self._eventos_lectura = []
        
        registrar_evento(self.historial_eventos, "Inicializacion Libro", "N/A", f"Páginas totales: {paginas_totales}")

    # Propiedades de solo lectura
    @property
    def paginas_totales(self):
        return self._paginas_totales

    @property
    def paginas_leidas(self):
        return self._paginas_leidas
    
    @property
    def eventos_lectura(self):
        return list(self._eventos_lectura)

    # --- Operaciones ---

    def leer(self, paginas: int):
        """leer(paginas) -> incrementa paginas_leidas; valida límites."""
        if paginas <= 0:
            print("ERROR: La cantidad de páginas a leer debe ser positiva.")
            return

        paginas_restantes = self._paginas_totales - self._paginas_leidas
        if paginas > paginas_restantes:
            print(f"RECHAZO: No se pueden leer {paginas} páginas. Solo quedan {paginas_restantes} páginas restantes.")
            return
        
        acumulado_antes = self._paginas_leidas
        self._paginas_leidas += paginas
        acumulado_despues = self._paginas_leidas

        self._eventos_lectura.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "paginas_leidas": paginas,
            "acumulado": acumulado_despues
        })
        print(f"OK: Leídas {paginas} páginas. Acumulado: {acumulado_despues}/{self.paginas_totales}.")

    def consultar_progreso(self) -> float:
        """consultar_progreso() -> devuelve % leído redondeado."""
        if self._paginas_totales == 0:
            return 0.0
        progreso = (self._paginas_leidas / self._paginas_totales) * 100
        # Devuelve el porcentaje redondeado a 2 decimales
        return round(progreso, 2)
