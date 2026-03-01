"""
Punto de entrada principal.
Genera las 4 figuras análogas a la Fig. 5 de Denton & Pestes (2021).

Uso:
    python main.py

Output:
    figuras/figura5_outer_mantle.png
    figuras/figura5_lower_mantle.png
    figuras/figura5_outer_core.png
    figuras/figura5_inner_core.png
    figuras/figura5_todas_capas.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from src.parametros   import Dm2_21
from src.materia      import calcular_A_CC
from src.probabilidades import calcular_probabilidades

# ── Carpeta de salida ────────────────────────────────────────────────
FIGURAS_DIR = "figuras"
os.makedirs(FIGURAS_DIR, exist_ok=True)

# ── 4 "Tierras" homogéneas — densidades promedio PREM ───────────────
CAPAS = [
    # (nombre_corto,   nombre_largo,     rho [g/cm³],  Ye,    color_fondo)
    ("outer_mantle",  "Outer Mantle",    3.5,          0.49,  "#b7e4a0"),
    ("lower_mantle",  "Lower Mantle",    5.0,          0.49,  "#fde68a"),
    ("outer_core",    "Outer Core",     11.0,          0.47,  "#fca5a5"),
    ("inner_core",    "Inner Core",     13.0,          0.47,  "#A9D1EB"),
]

# ── Barrido angular ──────────────────────────────────────────────────
cos_tz = np.linspace(-1.0, -0.001, 3000)
TICKS_X    = [-1.0, -0.8, -0.6, -0.4, -0.2, 0.0]
TICKS_DEG  = ["180°","143°","127°","114°","102°","90°"]


def _decorar_ax(ax, nombre_largo, rho, Ye):
    """Aplica título, ejes, leyenda y grilla a un subplot."""
    A_CC  = calcular_A_CC(rho, Ye)
    ratio = A_CC / Dm2_21

    ax.set_title(
        f"{nombre_largo}   |   ρ = {rho} g/cm³,  "
        f"Ye = {Ye},   A_CC/Δm² = {ratio:.2f}",
        fontsize=9.5
    )
    ax.legend(loc="lower right", fontsize=9, framealpha=0.85)
    ax.set_xlim(-1.0, 0.0)
    ax.set_ylim(-0.02, 1.05)
    ax.set_xticks(TICKS_X)
    ax.set_xticklabels([str(t) for t in TICKS_X], fontsize=9)
    ax.set_xlabel(r"$\cos\,\theta_z$", fontsize=10)
    ax.set_ylabel(r"$P_{\alpha\beta}$", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.35)

    # Eje superior en grados
    ax2 = ax.twiny()
    ax2.set_xlim(-1.0, 0.0)
    ax2.set_xticks(TICKS_X)
    ax2.set_xticklabels(TICKS_DEG, fontsize=8)
    ax2.set_xlabel(r"$\theta_z$", fontsize=9)


def graficar_capa_individual(nombre_corto, nombre_largo, rho, Ye, bg):
    """Genera y guarda la figura individual de una sola capa."""
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.suptitle(
        r"$E_\nu = 250$ MeV  |  2 sabores + efecto de materia  |  NuFIT 6.1 NO",
        fontsize=10
    )

    P_ee, P_emu = calcular_probabilidades(cos_tz, rho, Ye)

    ax.axvspan(-1.0, 0.0, alpha=0.30, color=bg, zorder=0)
    ax.plot(cos_tz, P_ee,  color="royalblue",  lw=2.0,
            label=r"$P(\nu_e \to \nu_e)$")
    ax.plot(cos_tz, P_emu, color="darkorange", lw=2.0,
            label=r"$P(\nu_e \to \nu_\mu)$")

    _decorar_ax(ax, nombre_largo, rho, Ye)

    ruta = os.path.join(FIGURAS_DIR, f"figura5_{nombre_corto}.png")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✅  Guardada → {ruta}")


def graficar_todas_capas():
    """Genera y guarda la figura 2×2 con las 4 capas juntas."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(
        r"Oscilaciones de neutrinos — 2 sabores, densidad constante"
        "\n"
        r"$E_\nu = 250$ MeV  |  NuFIT 6.1, Ordenamiento Normal",
        fontsize=12, fontweight="bold"
    )

    for idx, (_, nombre_largo, rho, Ye, bg) in enumerate(CAPAS):
        ax = axes[idx // 2][idx % 2]

        P_ee, P_emu = calcular_probabilidades(cos_tz, rho, Ye)

        ax.axvspan(-1.0, 0.0, alpha=0.30, color=bg, zorder=0)
        ax.plot(cos_tz, P_ee,  color="royalblue",  lw=2.0,
                label=r"$P(\nu_e \to \nu_e)$")
        ax.plot(cos_tz, P_emu, color="darkorange", lw=2.0,
                label=r"$P(\nu_e \to \nu_\mu)$")

        _decorar_ax(ax, nombre_largo, rho, Ye)

    plt.tight_layout(rect=[0, 0, 1, 0.95], h_pad=3.5, w_pad=2.5)

    ruta = os.path.join(FIGURAS_DIR, "figura5_todas_capas.png")
    plt.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✅  Guardada → {ruta}")

# ══════════════════════════════════════════════════════════════════════
# TESTS — verificación física del modelo
# Ejecutar: python main.py  (los tests corren al final automáticamente)
# ══════════════════════════════════════════════════════════════════════

def run_tests():
    import numpy as np
    from src.parametros      import Dm2_21, theta12, E_eV, E_GeV, R_TIERRA_KM, CAPAS
    from src.materia         import calcular_A_CC, parametros_efectivos   # ← corregido
    from src.geometria       import distancia_km
    from src.probabilidades  import calcular_probabilidades

    errores = []

    # ── TEST 1: Unitariedad ───────────────────────────────────────────
    cos_tz = np.linspace(-1.0, -0.001, 1000)
    for capa in CAPAS:
        P_emu, P_ee = calcular_probabilidades(cos_tz, capa["rho"], capa["Ye"])
        suma = P_ee + P_emu
        if not np.allclose(suma, 1.0, atol=1e-10):
            errores.append(f"TEST 1 FALLO [{capa['nombre']}]: max error={np.max(np.abs(suma-1)):.2e}")
        else:
            print(f"  TEST 1 OK  [{capa['nombre']}]: P_ee + P_emu = 1 ✓")

    # ── TEST 2: Límite vacío ──────────────────────────────────────────
    A_test        = calcular_A_CC(rho_gcm3=0.0, Ye=0.0)
    Dm2_vac, sin2_vac = parametros_efectivos(A_test)   # ← corregido
    sin2_esperado = np.sin(2 * theta12)
    if not np.isclose(Dm2_vac, Dm2_21, rtol=1e-6):
        errores.append(f"TEST 2 FALLO: Δm²_M(vacío) = {Dm2_vac:.4e} != {Dm2_21:.4e}")
    elif not np.isclose(sin2_vac, sin2_esperado, rtol=1e-6):
        errores.append(f"TEST 2 FALLO: sin2θ_M(vacío) = {sin2_vac:.6f} != {sin2_esperado:.6f}")
    else:
        print(f"  TEST 2 OK  [vacío]: Δm²_M → Δm²₂₁, sin2θ_M → sin2θ₁₂ ✓")

    # ── TEST 3: Geometría θz=90° ──────────────────────────────────────
    x = distancia_km(np.array([0.0]))
    if not np.isclose(x[0], 0.0, atol=1e-6):
        errores.append(f"TEST 3 FALLO: x(cos=0) = {x[0]:.4f} km != 0")
    else:
        print(f"  TEST 3 OK  [θz=90°]: x = 0 km ✓")

    # ── TEST 4: Geometría θz=180° ─────────────────────────────────────
    x        = distancia_km(np.array([-1.0]))
    esperado = 2.0 * R_TIERRA_KM
    if not np.isclose(x[0], esperado, rtol=1e-6):
        errores.append(f"TEST 4 FALLO: x(cos=-1) = {x[0]:.2f} km != {esperado:.2f} km")
    else:
        print(f"  TEST 4 OK  [θz=180°]: x = 2·R⊕ = {esperado:.1f} km ✓")

    # ── TEST 5: Resonancia MSW ────────────────────────────────────────
    cos2t         = np.cos(2 * theta12)
    A_res         = Dm2_21 * cos2t
    _, sin2tM_res = parametros_efectivos(A_res)        # ← corregido
    if not np.isclose(sin2tM_res, 1.0, atol=1e-6):
        errores.append(f"TEST 5 FALLO: sin2θ_M(resonancia) = {sin2tM_res:.6f} != 1")
    else:
        print(f"  TEST 5 OK  [resonancia MSW]: sin²(2θ_M) = 1 ✓")

    # ── TEST 6: Rango físico ──────────────────────────────────────────
    cos_tz = np.linspace(-1.0, -0.001, 5000)
    for capa in CAPAS:
        P_emu, P_ee = calcular_probabilidades(cos_tz, capa["rho"], capa["Ye"])
        if np.any(P_ee < -1e-10) or np.any(P_ee > 1+1e-10):
            errores.append(f"TEST 6 FALLO [{capa['nombre']}]: P_ee fuera de [0,1]")
        elif np.any(P_emu < -1e-10) or np.any(P_emu > 1+1e-10):
            errores.append(f"TEST 6 FALLO [{capa['nombre']}]: P_emu fuera de [0,1]")
        else:
            print(f"  TEST 6 OK  [{capa['nombre']}]: 0 ≤ P_ee, P_emu ≤ 1 ✓")

    # ── Resumen ───────────────────────────────────────────────────────
    print()
    if errores:
        print(f"  ❌ {len(errores)} test(s) fallaron:")
        for e in errores:
            print(f"     {e}")
    else:
        print("  ✅ Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    print("\n Generando figuras en carpeta figuras/ ...\n")

    # Una figura por capa
    for nombre_corto, nombre_largo, rho, Ye, bg in CAPAS:
        graficar_capa_individual(nombre_corto, nombre_largo, rho, Ye, bg)

    # Figura 2×2 con todas las capas
    graficar_todas_capas()

    print("\n Listo. Archivos generados:")
    for f in sorted(os.listdir(FIGURAS_DIR)):
        if f.endswith(".png"):
            print(f"   figuras/{f}")

    # ── Tests ─────────────────────────────────────────────────────────
    print("\n" + "═"*60)
    print("  VERIFICACIÓN FÍSICA — 6 TESTS")
    print("═"*60)
    run_tests()