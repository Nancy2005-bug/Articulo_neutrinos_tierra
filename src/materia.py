"""
Efecto de materia a densidad constante — esquema 2 sabores.
Ecuaciones (1)–(5) del PDF de instrucciones.
"""
import numpy as np
from src.parametros import Dm2_21, theta12, sqrt2_GF, E_eV

def calcular_A_CC(rho_gcm3: float, Ye: float) -> float:
    """
    Potencial de materia A_CC = 2 E_ν √2 G_F N_e  [eV²]
    N_e = Ye · ρ · Nₐ  [cm⁻³]   (Nₐ absorbido en sqrt2_GF)

    Parámetros
    ----------
    rho_gcm3 : densidad másica [g/cm³]
    Ye       : fracción de electrones Z/A

    Retorna
    -------
    A_CC en eV²
    """
    return 2 * E_eV * sqrt2_GF * Ye * rho_gcm3


def parametros_efectivos(A_CC: float) -> tuple[float, float]:
    """
    Calcula Δm²_M y sin(2θ_M) en materia de densidad constante.
    Ecuaciones (4) y (5) del PDF de instrucciones.
    Retorna (Dm2_M, sin2thetaM)
    """
    sin2t = np.sin(2 * theta12)
    cos2t = np.cos(2 * theta12)
    
    Dm2_M   = np.sqrt((Dm2_21 * cos2t - A_CC)**2
                      + (Dm2_21 * sin2t)**2)
    sin2t_M = (Dm2_21 * sin2t) / Dm2_M
    return Dm2_M, sin2t_M