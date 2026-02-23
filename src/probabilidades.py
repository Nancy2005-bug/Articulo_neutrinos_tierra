"""
Probabilidades de oscilación a 2 sabores con efecto de materia.
Ecuaciones (6) y (7) del PDF de instrucciones.
"""
import numpy as np
from src.parametros import E_GeV
from src.materia import calcular_A_CC, parametros_efectivos
from src.geometria import distancia_km


def calcular_probabilidades(
    cos_tz: np.ndarray,
    rho_gcm3: float,
    Ye: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula P(νe→νe) y P(νe→νμ) en función del ángulo cenital.

    Factor de conversión de unidades:
      Δm²[eV²] · x[km] / E[GeV]  ×  1.267  →  adimensional

    Parámetros
    ----------
    cos_tz   : array de cos θz (valores en [-1, 0])
    rho_gcm3 : densidad de la "Tierra" [g/cm³]
    Ye       : fracción de electrones

    Retorna
    -------
    (P_ee, P_emu) : arrays de probabilidades ∈ [0, 1]
    """
    A_CC       = calcular_A_CC(rho_gcm3, Ye)
    Dm2_M, s2M = parametros_efectivos(A_CC)
    x_km       = distancia_km(cos_tz)

    # Argumento del seno²  (factor 1.267 incluye conversión de unidades)
    phase = 1.267 * Dm2_M * x_km / E_GeV

    P_emu = s2M**2 * np.sin(phase)**2   # Ec. (6)
    P_ee  = 1.0 - P_emu                  # Ec. (7)
    return P_ee, P_emu