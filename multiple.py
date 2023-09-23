import numpy as np
import matplotlib.pyplot as plt
from energ_tubo import get_pipe_energy

# DATOS GEOESPACIALES
# ===================
longitud_local = -79.0286  # Longitud (Trujillo).
latitud_local = -8.11167   # Latitud Local (Trujillo), phi [deg].
altitud_local = 33         # Altitud local (Trujillo) [m]

# DATOS DISPOSICION DEL COLECTOR
# ==============================
# Especifica arrays de inclinaciones y azimuts
inclinaciones = [0, 20, 25, 30]  # Lista de ángulos de inclinación [deg].
azimuths = [140, 160, 180, 210, 240]  # Lista de ángulos de azimut [deg].

# DATOS DEL TUBO AL VACIO (CONFIGURACION GEOMÉTRICA)
# ===========================================
diametro_interno = 0.048   # Diametro interno del tubo al vacio [m]
diametro_externo = 0.058   # Diametro externo del tubo al vacio [m]
longitud_tubo = 1.80   # Longitud efectivo del tubo al vacio expuesto al sol [m]
separacion_tubos_centros = 0.116   # Distancia de separacion entre centro de tubos [m]

# CONFIGURACION DE LA MATRIZ HORARIA
# ==================================
nn = 24        # Division de puntos que abarca todo el dia

for inclinacion in inclinaciones:
    plt.figure()

    for azimuth in azimuths:
        energia_diaria = np.zeros(365)

        for n in range(1, 366):
            dia = n

            energia_diaria[n - 1] = get_pipe_energy(
                n,
                latitud_local,
                inclinacion,
                azimuth,
                longitud_local,
                nn,
                altitud_local,
                diametro_interno,
                diametro_externo,
                separacion_tubos_centros,
                longitud_tubo
            )

        dia_col = np.arange(1, 366).reshape(-1, 1)
        energia_diaria_col = energia_diaria.reshape(-1, 1)
        energia_anual = np.sum(energia_diaria)
        plt.plot(dia_col, energia_diaria_col, label=f"Azimuth: {azimuth}°")

    plt.title(f"Energia Diaria Disponible para Inclinación: {inclinacion}° [kW-h]")
    plt.xlabel("Dia")
    plt.ylabel("Energia [kW-h]")
    plt.grid()
    plt.ylim(0, 0.9)
    plt.legend()

plt.show()
