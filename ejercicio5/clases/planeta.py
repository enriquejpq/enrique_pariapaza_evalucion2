from datetime import datetime
import math
from typing import Any
from ejercicio5.clases.cuerpo_celeste import CuerpoCeleste

# Constantes para el cálculo de volumen
PI = math.pi
VOLUMEN_COEFICIENTE = 4/3 * PI

# Modelo 2 — Planeta (Extiende CuerpoCeleste)
class Planeta(CuerpoCeleste):
    """Extiende CuerpoCeleste con radio, distancia al sol y cálculo de densidad."""
    def __init__(self, nombre: str, masa_kg: float, radio_km: float, distancia_sol_km: float):
        # 1. Llamada al constructor de la clase base
        super().__init__(nombre, masa_kg)
        
        # 2. Validaciones adicionales de Planeta
        if radio_km <= 0:
            raise ValueError("El radio debe ser un valor positivo (radio_km > 0).")
        if distancia_sol_km <= 0:
            raise ValueError("La distancia al sol debe ser un valor positivo (distancia_sol_km > 0).")

        # Atributos específicos
        self._radio_km = radio_km
        self._distancia_sol_km = distancia_sol_km

    # Propiedades para acceder a los nuevos atributos (evita modificación directa)
    @property
    def radio_km(self):
        return self._radio_km

    @property
    def distancia_sol_km(self):
        return self._distancia_sol_km

    # Operaciones

    def actualizar_radio(self, nuevo_radio: float):
        """Actualiza el radio, valida > 0 y registra en historial."""
        if nuevo_radio <= 0:
            raise ValueError("El nuevo radio debe ser un valor positivo (radio_km > 0).")
        
        if nuevo_radio != self._radio_km:
            self._registrar_evento("radio_km", self._radio_km, nuevo_radio)
            self._radio_km = nuevo_radio

    def actualizar_distancia_sol(self, nueva_distancia: float):
        """Actualiza la distancia al sol, valida > 0 y registra en historial."""
        if nueva_distancia <= 0:
            raise ValueError("La nueva distancia al sol debe ser un valor positivo.")
        
        if nueva_distancia != self._distancia_sol_km:
            self._registrar_evento("distancia_sol_km", self._distancia_sol_km, nueva_distancia)
            self._distancia_sol_km = nueva_distancia

    def calcular_densidad(self) -> float:
        """Calcula la densidad aproximada (masa / volumen). Densidad en kg/km³."""
        # Volumen (km³) ≈ 4/3 * π * radio³
        volumen_km3 = VOLUMEN_COEFICIENTE * (self._radio_km ** 3)
        
        # La masa es heredada (_masa_kg)
        densidad_kg_por_km3 = self._masa_kg / volumen_km3
        
        return densidad_kg_por_km3

    def comparar_distancia(self, otro_planeta):
        """Indica cuál planeta está más cerca del sol."""
        # Regla de negocio: Comparaciones solo entre objetos Planeta.
        if not isinstance(otro_planeta, Planeta):
            return "Error: La comparación solo es válida entre objetos del tipo Planeta."
        
        distancia_propia = self._distancia_sol_km
        distancia_otro = otro_planeta.distancia_sol_km

        if distancia_propia < distancia_otro:
            return f"{self._nombre} está más cerca del sol que {otro_planeta._nombre}."
        elif distancia_propia > distancia_otro:
            return f"{otro_planeta._nombre} está más cerca del sol que {self._nombre}."
        else:
            return f"Ambos planetas ({self._nombre} y {otro_planeta._nombre}) están a la misma distancia del sol."

    def consultar_ficha(self):
        """Extiende la ficha de CuerpoCeleste con los datos de Planeta."""
        ficha_base = super().consultar_ficha()
        
        # Insertar atributos de Planeta
        ficha_base["Radio (km)"] = f"{self._radio_km:,}"
        ficha_base["Distancia Sol (km)"] = f"{self._distancia_sol_km:,}"
        try:
            ficha_base["Densidad (kg/km³)"] = f"{self.calcular_densidad():.4e}"
        except Exception:
             ficha_base["Densidad (kg/km³)"] = "Error de cálculo"

        return ficha_base
