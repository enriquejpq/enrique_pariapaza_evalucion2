import datetime
from typing import Dict, Any, List

def generar_registro(tipo_accion: str, descripcion_breve: str, valor_ant: Any = None, valor_nue: Any = None, campo_mod: str = None) -> Dict[str, Any]:
    """
    Crea una entrada estandarizada para el historial de eventos de cualquier objeto.
    """
    # Manejo de valores numéricos grandes (como en Ejercicio 5) para un mejor registro
    if isinstance(valor_ant, (int, float)) and valor_ant > 1e10:
        valor_ant_str = f"{valor_ant:.2e}"
    else:
        valor_ant_str = str(valor_ant) if valor_ant is not None else None

    if isinstance(valor_nue, (int, float)) and valor_nue > 1e10:
        valor_nue_str = f"{valor_nue:.2e}"
    else:
        valor_nue_str = str(valor_nue) if valor_nue is not None else None

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "tipo_accion": tipo_accion,
        "campo_modificado": campo_mod,
        "detalles_operacion": descripcion_breve,
        "valor_anterior": valor_ant_str,
        "valor_nuevo": valor_nue_str
    }