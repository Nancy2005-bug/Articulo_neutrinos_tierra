"""
Constantes físicas y parámetros de oscilación.
Fuente: NuFIT 6.1 (2025), Ordenamiento Normal.
"""
import numpy as np

# ------ Tierra -------------------------------------------------------
R_TIERRA_KM = 6371.0          # radio terrestre [km]

# ------ Energía del neutrino -----------------------------------------
E_GeV = 0.250                  # 250 MeV (igual que Fig. 5 del paper)
E_eV  = E_GeV * 1e9           # [eV]

# ------ Parámetros de oscilación (NuFIT 6.1, NO) --------------------
# Usamos parámetros SOLARES (Δm²₂₁, θ₁₂) porque a 250 MeV
# la longitud de oscilación solar cabe ~1 vez en la Tierra.
Dm2_21  = 7.537e-5             # eV²,  Δm²₂₁
theta12 = np.radians(33.76)    # θ₁₂  [rad]

# ------ Constante de Fermi -------------------------------------------
# √2 G_F ≈ 7.63×10⁻¹⁴ eV·cm³/Nₐ
sqrt2_GF = 7.63e-14            # eV·cm³ / Nₐ