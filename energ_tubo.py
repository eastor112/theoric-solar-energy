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
  d_int,
  d_ext,
  s_sep,
  l_tubo
):
  # CALCULOS PUNTUALES INSTANTÁNEOS
  # ===============================
  gon = m.extraterrestrial_radiation(n)
  ang_delta = m.declination_angle(n)
  ang_omega_s = m.sunset_hour_angle(latitud_local, ang_delta)
  hora_aparec_sol = m.sunrise(ang_omega_s)
  hora_puesta_sol = m.sunset(ang_omega_s)

  # CALCULOS ANGULARES HORARIOS (manteniendo desde "hora_aparec_sol" hasta "hora_puesta_sol")
  # ==========================
  hora_sol = np.zeros(nn)
  hora_std = np.zeros(nn)
  ang_omega = np.zeros(nn)
  ang_theta = np.zeros(nn)
  ang_theta_z = np.zeros(nn)

  for i in range(nn):
    hora_sol[i] = hora_aparec_sol + (hora_puesta_sol - hora_aparec_sol) / nn * (i - 1)
    hora_std[i] = m.standard_time(n, hora_sol[i], longitud_local)
    ang_omega[i] = m.hour_angle(hora_sol[i])
    ang_theta[i] = m.incidence_angle(ang_delta, latitud_local, inclinacion, azimuth, ang_omega[i])
    ang_theta_z[i] = m.zenith_angle(ang_delta, latitud_local, azimuth, ang_omega[i])

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================
  Go_m = np.zeros(nn)

  for i in range(nn):
      Go_m[i] = m.extraterrestrial_horizontal_radiation(gon, ang_theta[i])

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================
  tau_beam = np.zeros(nn)
  g_beam_n = np.zeros(nn)
  tau_dif = np.zeros(nn)
  g_oo = np.zeros(nn)
  g_difus = np.zeros(nn)

  for i in range(nn):
    tau_beam[i] = m.sky_transmissivity(ang_theta_z[i], altitud_local)
    g_beam_n[i] = m.beam_radiation(gon, tau_beam[i])
    tau_dif[i] = m.diffuse_transmissivity(tau_beam[i])
    g_oo[i] = m.extraterrestrial_horizontal_radiation(gon, ang_theta_z[i])
    g_difus[i] = m.diffuse_radiation_horizontal(g_oo[i], tau_dif[i])

  F_forma = m.diffuse_radiation_shape_function(d_int, d_ext, s_sep)

  # CALCULO DE LAS POTENCIAS HORARIAS QUE INCIDEN SOBRE UN TUBO AL VACIO [W] (Tang, 2009)
  # =========================================================================
  nx = np.zeros(nn)
  ny = np.zeros(nn)
  nz = np.zeros(nn)
  nnx = np.zeros(nn)
  nny = np.zeros(nn)
  nnz = np.zeros(nn)
  angulo_omega = np.zeros(nn)
  ang_theta_t = np.zeros(nn)
  func_accep = np.zeros(nn)
  potencia_haz_1t = np.zeros(nn)
  g_difus_beta = np.zeros(nn)
  potencia_difus_1t = np.zeros(nn)

  for i in range(nn):
    nx[i], ny[i], nz[i] = m.sun_position(ang_delta, latitud_local, ang_omega[i])
    nnx[i], nny[i], nnz[i] = m.sun_position_prima(nx[i], ny[i], nz[i], inclinacion, azimuth)
    ang_theta_t[i] = np.degrees(math.acos(math.sqrt(nnx[i]**2 + nny[i]**2)))
    func_accep[i] = m.acceptance_function(d_int, d_ext, s_sep, angulo_omega[i])
    potencia_haz_1t[i] = m.direct_radiant_power(g_beam_n[i], d_int, l_tubo, ang_theta_t[i], func_accep[i])
    g_difus_beta[i] = m.diffuse_radiation_inclined_surface(g_difus[i], inclinacion)
    potencia_difus_1t[i] = m.diffuse_radiant_power(g_difus_beta[i], d_int, l_tubo, F_forma)

  potencia_total_1t = potencia_haz_1t + potencia_difus_1t

  return np.trapz(hora_std, potencia_total_1t) / 1000
