"""
Geometría del trayecto del neutrino en una Tierra esférica.

Convención: el neutrino llega al detector DESDE ABAJO.
  cos θz ∈ [-1, 0]  →  θz ∈ [90°, 180°]

Fuente: Ec. (40) de arXiv:1110.5471 y Ec. (17) de arXiv:2207.11257.
"""
import numpy as np
from src.parametros import R_TIERRA_KM


def distancia_km(cos_tz: float | np.ndarray) -> np.ndarray:
    """
    Distancia total recorrida dentro de la Tierra esférica homogénea.

      x(θz) = 2 R⊕ |cos θz|   [km]

    Parámetros
    ----------
    cos_tz : cos del ángulo cenital, en [-1, 0]

    Retorna
    -------
    Distancia en km (array del mismo tamaño que cos_tz)
    """
    cos_tz = np.asarray(cos_tz)
    return 2 * R_TIERRA_KM * np.abs(cos_tz)