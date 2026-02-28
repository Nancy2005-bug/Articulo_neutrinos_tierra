"""
Parámetros físicos y densidades PREM.

Densidades: promedio ponderado por volumen de la Tabla II de
Dziewonski & Anderson (1981), PREM.
Ye (= Z/A): Tabla 1 de arXiv:2207.11257.
"""

import numpy as np

# ── Parámetros de oscilación — NuFIT 6.1 (2025), Ordenamiento Normal ──
Dm2   = 7.537e-5      # Δm²₂₁  [eV²]
THETA = np.radians(33.76)   # θ₁₂  [rad]
E_GeV = 0.250         # Energía del neutrino  [GeV]
E_eV  = E_GeV * 1e9   # Energía del neutrino  [eV]

# ── Constante — parametrización numérica de √2 G_F ─────────────────
# √2 G_F ≃ 7.63e-14  eV·cm³ / N_A
# (Instrucciones-Parcial1.pdf, ec. 3)
SQRT2_GF = 7.63e-14   # [eV·cm³ · mol]

# ── Radio de la Tierra ──────────────────────────────────────────────
R_EARTH_KM = 6371.0   # [km]

# ── Datos crudos Tabla II PREM — (radio [km], densidad [g/cm³]) ─────
_PREM_RAW = np.array([
    # Inner Core  (0 – 1221.5 km)
    [0,      13.0885], [100,   13.0863], [200,   13.0798],
    [300,    13.0668], [400,   13.0538], [500,   13.0313],
    [600,    13.0104], [700,   12.9799], [800,   12.9491],
    [900,    12.9096], [1000,  12.8703], [1100,  12.8224],
    [1200,   12.7740], [1221.5,12.7630],
    # Outer Core  (1221.5 – 3480 km)
    [1221.5, 12.1663], [1300,  12.1258], [1400,  12.0692],
    [1500,   12.0099], [1600,  11.9472], [1700,  11.8799],
    [1800,   11.8082], [1900,  11.7340], [2000,  11.6557],
    [2100,   11.5712], [2200,  11.4813], [2300,  11.3904],
    [2400,   11.2897], [2500,  11.1907], [2600,  11.0806],
    [2700,   10.9704], [2800,  10.8473], [2900,  10.7301],
    [3000,   10.5965], [3100,  10.4683], [3200,  10.3293],
    [3300,   10.1813], [3400,  10.0250], [3480,   9.9035],
    # Lower Mantle  (3480 – 5701 km)
    [3480,   5.5665],  [3500,  5.5562],  [3600,  5.5064],
    [3630,   5.4916],  [3700,  5.4507],  [3800,  5.4069],
    [3900,   5.3573],  [4000,  5.3077],  [4100,  5.2577],
    [4200,   5.2071],  [4300,  5.1560],  [4400,  5.1055],
    [4500,   5.0538],  [4600,  5.0023],  [4700,  4.9490],
    [4800,   4.8975],  [4900,  4.8440],  [5000,  4.7912],
    [5100,   4.7372],  [5200,  4.6834],  [5300,  4.6287],
    [5400,   4.5740],  [5500,  4.5183],  [5600,  4.4630],
    [5701,   4.4032],
    # Outer Mantle  (5701 – 6346.6 km)
    [5701,   3.9840],  [5771,  3.9325],  [5871,  3.8750],
    [5971,   3.7338],  [6071,  3.5414],  [6151,  3.3598],
    [6221,   3.3648],  [6291,  3.3747],  [6346.6,3.3808],
])

_r_all   = _PREM_RAW[:, 0]
_rho_all = _PREM_RAW[:, 1]


def _promedio_volumetrico(r_min, r_max):
    """Promedio de densidad ponderado por volumen de capa esférica [g/cm³]."""
    mask = (_r_all >= r_min) & (_r_all <= r_max)
    r    = _r_all[mask].copy()
    rho  = _rho_all[mask].copy()
    if r[0] > r_min:
        r   = np.concatenate([[r_min], r])
        rho = np.concatenate([[np.interp(r_min, _r_all, _rho_all)], rho])
    if r[-1] < r_max:
        r   = np.concatenate([r, [r_max]])
        rho = np.concatenate([rho, [np.interp(r_max, _r_all, _rho_all)]])
    vol     = (4/3) * np.pi * (r[1:]**3 - r[:-1]**3)
    rho_mid = (rho[:-1] + rho[1:]) / 2
    return float(np.sum(rho_mid * vol) / np.sum(vol))


# ── Densidades promedio y Ye por capa (calculados de Tabla II PREM) ─
#    Ye  fuente: Tabla 1 de arXiv:2207.11257

CAPAS = [
    {
        "nombre":  "Outer Mantle",
        "r_min":   5701.0,
        "r_max":   6346.6,
        "rho":     _promedio_volumetrico(5701.0, 6346.6),   # 3.621 g/cm³
        "Ye":      0.49,
        "color":   "#d5f0c0",
    },
    {
        "nombre":  "Lower Mantle",
        "r_min":   3480.0,
        "r_max":   5701.0,
        "rho":     _promedio_volumetrico(3480.0, 5701.0),   # 4.908 g/cm³
        "Ye":      0.49,
        "color":   "#fdeea0",
    },
    {
        "nombre":  "Outer Core",
        "r_min":   1221.5,
        "r_max":   3480.0,
        "rho":     _promedio_volumetrico(1221.5, 3480.0),   # 10.900 g/cm³
        "Ye":      0.47,
        "color":   "#fdc0b8",
    },
    {
        "nombre":  "Inner Core",
        "r_min":   0.0,
        "r_max":   1221.5,
        "rho":     _promedio_volumetrico(0.0, 1221.5),      # 12.893 g/cm³
        "Ye":      0.47,
        "color":   "#d8ccf5",
    },
]

Dm2_21    = Dm2
theta12   = THETA
sqrt2_GF  = SQRT2_GF
R_EARTH   = R_EARTH_KM
R_TIERRA_KM = R_EARTH_KM