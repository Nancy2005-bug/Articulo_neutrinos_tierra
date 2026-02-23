# Oscilaciones de Neutrinos en la Tierra
### Adaptación didáctica de la Figura 5 — Denton & Pestes (2021)

> **Contexto académico:** Primer parcial — Física de Neutrinos.
> **Grupo 3:** Nancy Camacho Santo y Karol Ivonne Castro Hernández.  
> **Artículo base:** P. B. Denton and R. Pestes, [*"Neutrino oscillations through the Earth's core"*](https://doi.org/10.1103/PhysRevD.104.113007), Phys. Rev. D 104 (2021) 113007.
---

## ¿Qué hace este proyecto?

Este código reproduce una adaptación didáctica de la Figura 5 del artículo de Denton & Pestes (2021), que muestra las probabilidades de oscilación de neutrinos atmosféricos propagándose a través de la Tierra.

La adaptación simplifica el modelo original (3 sabores, PREM completo) a:

- **2 sabores** ($\nu_{w}$, $\nu_{\mu}$) con efecto de materia a densidad constante.
- **4 "Tierras" homogéneas**, cada una con la densidad promedio de una capa del modelo PREM:


  | Capa | ρ (g/cm³) | Ye |
  |---|---|---|
  | Outer Mantle | 3.5 | 0.49 |
  | Lower Mantle | 5.0 | 0.49 |
  | Outer Core | 11.0 | 0.47 |
  | Inner Core | 13.0 | 0.47 |

Para cada "Tierra" se calculan y grafican:
- La probabilidad de supervivencia $P(\nu_{e}\rightarrow \nu_{e})$.
- La probabilidad de transición $P(\nu_{e}\rightarrow \nu_{\mu})$.

en función del ángulo cenital $\theta_{z} \in [90\degree, 180\degree]$ (neutrino llegando desde abajo).

---

## Física del modelo

### Parámetros de oscilación
Tomados de [NuFIT 6.1 (2025)](http://www.nu-fit.org/?q=node/309), Ordenamiento Normal:

| Parámetro | Valor |
|---|---|
| $\Delta m_{21}^2$ | $7.537 \times 10^{-5} eV^2$ |
| $\theta_{12}$ | $33.76\degree$ |
| $E_{\nu}$ | 250 MeV |

Se usan los parámetros solares ($\Delta m_{21}^2$, $\theta_{12}$) porque a 250 MeV la longitud de oscilación ($\sim 8230$ km) es comparable al diámetro de la Tierra.

### Ecuaciones implementadas

El potencial de materia para $\nu_{e}$ es:

$$
A_{CC}=2E_{\nu} \sqrt{2} G_{F} N_{e}(x) \quad [eV^2]
$$

Los parámetros efectivos en materia (densidad constante):

$$
\Delta m_{M}^2(x)=\sqrt{(\Delta m^2 \cos{2\theta} - A_{CC}(x))^2+(\Delta m^2\sin{2\theta})^2}
$$

$$
\sin{2\theta_{M}}(x)=\frac{\Delta m^2 \sin{2\theta}}{\Delta m_{M}^2(x)}
$$

Las probabilidades de oscilación:

$$
P_{\nu_{e}\to \nu_{\mu}}=\sin^2{2\theta_{M}}\sin^2{\left(\frac{1.267 \Delta m^2_{M} x}{E_{\nu}}\right)}
$$

$$
P(\nu_{e} \to \nu_{e})=1-P(\nu_{e} \to \nu_{\mu})
$$

donde $x(\theta_{z})=2R\oplus |\cos{\theta_{z}}|$ ($x=2R\oplus$ diámetro completo)


---

## Instalación y uso

### Requisitos
- Python 3.10 o superior
- Git
- Visual Studio Code (recomendado)

### Dependecias

>numpy>=1.24
matplotlib>=3.7

### 1. Clonar el repositorio.

```bash
git clone https://github.com/Nancy2005-bug/Articulo_neutrino_tierra.git
cd Articulo_neutrino_tierra
```

### 2. Crear el entorno virtual.

**Opción A:** desde VSCode:

>Ctrl + Shift + P → Python: Create Environment → Venv → selecciona Python 3.10+

**Opción B:** desde terminal:

>Windows (PowerShell) Ctrl + ñ
python -m venv .venv
.venv\Scripts\Activate.ps1

### 3. Instalar dependencias.

```bash
pip install -r requirements.txt
```

### 4. Ejecutar

```bash
python main.py
```

### 5. Ver resultados.

Las figuras se guardan automáticamente en `figuras/`:

---

## Figuras generadas

| Figura                   | Descripción                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| figura5_outer_mantle.png | Oscilaciones en Tierra con densidad del manto externo (cerca de resonancia MSW) |
| figura5_lower_mantle.png | Oscilaciones en Tierra con densidad del manto inferior (resonancia superada)    |
| figura5_outer_core.png   | Oscilaciones en Tierra con densidad del núcleo externo (materia dominante)      |
| figura5_inner_core.png   | Oscilaciones en Tierra con densidad del núcleo interno (supresión máxima)       |
| figura5_todas_capas.png  | Las 4 capas juntas en una figura 2×2 para comparación                           |

---

## Limitaciones del Modelo

Este modelo es una simplificación didáctica. Las diferencias con la Fig. 5
original del paper son:

1. 2 sabores vs 3 sabores: el paper usa el esquema completo PMNS.

2. Densidad constante vs PREM real: el paper usa densidad variable por capa.

3. Sin resonancia paramétrica: la resonancia estrecha en $\cos{\theta_{z}\approx -0.84}$ que aparece en la Fig. 5 no está presente en este modelo homogéneo.

4. Sin nuSQuIDs: el paper resuelve la ecuación de Schrödinger numéricamente con el paquete nuSQuIDs; aquí se usa la solución analítica exacta para densidad constante.

---

## Fuentes y Referencias

* Artículo principal: Denton & Pestes (2021), [link](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.104.113007)

* Parámetros de oscilación: NuFIT 6.1 (2025), [link](http://www.nu-fit.org/?q=node/309)

* Densidades PREM: Dziewonski & Anderson (1981), Tabla II, [link](http://www.nu-fit.org/?q=node/309)

* Geometría del trayecto: [arXiv:1110.5471](https://arxiv.org/pdf/1110.5471) (Ec. 40) y [arXiv:2207.11257](https://arxiv.org/pdf/2207.11257) (Ec. 17)