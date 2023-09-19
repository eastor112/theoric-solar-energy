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

d_int = 0.048   # Diametro interno del tubo al vacio [m]
d_ext = 0.058   # Diametro externo del tubo al vacio [m]
l_tubo = 1.80   # Longitud efectivo del tubo al vacio expuesto al sol [m]
s_sep = 0.116   # Distancia de separacion entre centro de tubos [m]


# CONFIGURACION DE LA MATRIZ HORARIA
# ==================================

nn = 121        # Division de puntos que abarca todo el dia

print("RESULTADOS DE ENERGIA DIARIA APROVECHADA EN 1 TUBO AL VACIO")
print("============================================================\n")

energia_diaria = np.zeros(365)

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
    d_int,
    d_ext,
    s_sep,
    l_tubo
  )
  energia_diaria[n - 1] = Energia_Total_1T

for n in range(1, 365):
    if np.isinf(energia_diaria[n]) or np.isnan(energia_diaria[n]):
        energia_diaria[n] = (energia_diaria[n - 1] + energia_diaria[n + 1]) / 2

dia_col = np.arange(1, 366).reshape(-1, 1)  # Vector que estima el dia
energia_diaria_col = energia_diaria.reshape(-1, 1)

energia_anual = np.sum(energia_diaria)  # Valor total de energia anual aprovechada en esa condición

import matplotlib.pyplot as plt

plt.figure(1)
plt.plot(dia_col, energia_diaria_col)
plt.title("Energia Diaria Disponible en 1 Tubo al Vacio [kW-h]")
plt.xlabel("Dia")
plt.ylabel("Energia [kW-h]")
plt.show()

print("Energia Anual Aprovechada en 1 Tubo al Vacio:", energia_anual, "kW-h")
