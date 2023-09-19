import numpy as np
from energ_tubo import get_pipe_energy

# DATOS GEOESPACIALES
# ===================

longitud_local = -79.0286  # Longitud (Trujillo).
latitud_local = -8.11167   # Latitud Local (Trujillo), phi [deg].
altitud_local = 33         # Altitud local (Trujillo) [m]


# DATOS DISPOSICION DEL COLECTOR
# ==============================
inclinacion = 0             # Angulo de inclinacion del colector, beta [deg].
azimuth = 180               # Angulo de azimuth del colector, gamma [deg] (180 mira al norte).


# DATOS DEL TUBO AL VACIO (CONFIGURACION GEOMÉTRICA)
# ===========================================

D_int = 0.048   # Diametro interno del tubo al vacio [m]
D_ext = 0.058   # Diametro externo del tubo al vacio [m]
L_tubo = 1.80   # Longitud efectivo del tubo al vacio expuesto al sol [m]
S_sep = 0.116   # Distancia de separacion entre centro de tubos [m]


# CONFIGURACION DE LA MATRIZ HORARIA
# ==================================

nn = 121        # Division de puntos que abarca todo el dia

print("RESULTADOS DE ENERGIA DIARIA APROVECHADA EN 1 TUBO AL VACIO")
print("============================================================\n")

Energia_Diaria = np.zeros(365)

for n in range(1, 366):
    Dia = n

    Energia_Total_1T = get_pipe_energy(
      n,
      latitud_local,
      inclinacion,
      azimuth,
      longitud_local,
      nn,
      altitud_local,
      D_int,
      D_ext,
      S_sep,
      L_tubo
    )
    Energia_Diaria[n - 1] = Energia_Total_1T

for n in range(1, 365):
    if np.isinf(Energia_Diaria[n]) or np.isnan(Energia_Diaria[n]):
        Energia_Diaria[n] = (Energia_Diaria[n - 1] + Energia_Diaria[n + 1]) / 2

Dia_col = np.arange(1, 366).reshape(-1, 1)  # Vector que estima el dia
Energia_Diaria_col = Energia_Diaria.reshape(-1, 1)

Energia_Anual = np.sum(Energia_Diaria)  # Valor total de energia anual aprovechada en esa condición

import matplotlib.pyplot as plt

plt.figure(1)
plt.plot(Dia_col, Energia_Diaria_col)
plt.title("Energia Diaria Disponible en 1 Tubo al Vacio [kW-h]")
plt.xlabel("Dia")
plt.ylabel("Energia [kW-h]")
plt.show()

print("Energia Anual Aprovechada en 1 Tubo al Vacio:", Energia_Anual, "kW-h")
