import math
import numpy as np
import model as m

def get_pipe_energy(
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
):
  # CALCULOS PUNTUALES INSTANTÁNEOS
  # ===============================
  Gon = m.extraterrestrial_radiation(n)
  ang_delta = m.declination_angle(n)
  ang_omega_s = m.sunset_hour_angle(latitud_local, ang_delta)
  hora_aparec_sol = m.sunrise(ang_omega_s)
  hora_puesta_sol = m.sunset(ang_omega_s)

  # CALCULOS ANGULARES HORARIOS (manteniendo desde "hora_aparec_sol" hasta "hora_puesta_sol")
  # ==========================
  HoraSol = np.zeros(nn)
  HoraStd = np.zeros(nn)
  AngOmega = np.zeros(nn)
  AngTheta = np.zeros(nn)
  AngThetaZ = np.zeros(nn)

  for i in range(nn):
      HoraSol[i] = hora_aparec_sol + (hora_puesta_sol - hora_aparec_sol) / nn * (i - 1)
      HoraStd[i] = m.standard_time(n, HoraSol[i], longitud_local)
      AngOmega[i] = m.hour_angle(HoraSol[i])
      AngTheta[i] = m.incidence_angle(ang_delta, latitud_local, inclinacion, azimuth, AngOmega[i])
      AngThetaZ[i] = m.zenith_angle(ang_delta, latitud_local, azimuth, AngOmega[i])

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================
  Go_m = np.zeros(nn)

  for i in range(nn):
      Go_m[i] = m.extraterrestrial_horizontal_radiation(Gon, AngTheta[i])

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================
  TAU_BEAM = np.zeros(nn)
  G_BEAMn = np.zeros(nn)
  TAU_DIF = np.zeros(nn)
  G_OO = np.zeros(nn)
  G_DIFUS = np.zeros(nn)

  for i in range(nn):
      TAU_BEAM[i] = m.sky_transmissivity(AngThetaZ[i], altitud_local)
      G_BEAMn[i] = m.beam_radiation(Gon, TAU_BEAM[i])
      TAU_DIF[i] = m.diffuse_transmissivity(TAU_BEAM[i])
      G_OO[i] = m.extraterrestrial_horizontal_radiation(Gon, AngThetaZ[i])
      G_DIFUS[i] = m.diffuse_radiation_horizontal(G_OO[i], TAU_DIF[i])

  F_forma = m.diffuse_radiation_shape_function(D_int, D_ext, S_sep)

  # CALCULO DE LAS POTENCIAS HORARIAS QUE INCIDEN SOBRE UN TUBO AL VACIO [W] (Tang, 2009)
  # =========================================================================
  Nx = np.zeros(nn)
  Ny = np.zeros(nn)
  Nz = np.zeros(nn)
  NNx = np.zeros(nn)
  NNy = np.zeros(nn)
  NNz = np.zeros(nn)
  ANGULO_OMEGA = np.zeros(nn)
  AngThetaT = np.zeros(nn)
  FUNC_ACCEP = np.zeros(nn)
  POTENCIA_HAZ_1T = np.zeros(nn)
  G_DIFUS_BETA = np.zeros(nn)
  POTENCIA_DIFUS_1T = np.zeros(nn)

  for i in range(nn):
      Nx[i], Ny[i], Nz[i] = m.sun_position(ang_delta, latitud_local, AngOmega[i])
      NNx[i], NNy[i], NNz[i] = m.sun_position_prima(Nx[i], Ny[i], Nz[i], inclinacion, azimuth)
      AngThetaT[i] = np.degrees(math.acos(math.sqrt(NNx[i]**2 + NNy[i]**2)))
      FUNC_ACCEP[i] = m.acceptance_function(D_int, D_ext, S_sep, ANGULO_OMEGA[i])
      POTENCIA_HAZ_1T[i] = m.direct_radiant_power(G_BEAMn[i], D_int, L_tubo, AngThetaT[i], FUNC_ACCEP[i])
      G_DIFUS_BETA[i] = m.diffuse_radiation_inclined_surface(G_DIFUS[i], inclinacion)
      POTENCIA_DIFUS_1T[i] = m.diffuse_radiant_power(G_DIFUS_BETA[i], D_int, L_tubo, F_forma)

  POTENCIA_TOTAL_1T = POTENCIA_HAZ_1T + POTENCIA_DIFUS_1T

  Energia_Total_1T = np.trapz(HoraStd, POTENCIA_TOTAL_1T) / 1000

  return Energia_Total_1T
