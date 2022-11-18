import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import yaml
from skyfield.api import load as skyfield_load
from params import TLE_Lifetime_Analysis_Parameters
from util import convert_skyfield_earthSatellites_into_dataframe_of_keplerian_elements, eci_2_ric
import datetime
import astropy.constants



DATE_RANGE = ("2013-02-01", "2013-05-01")
MANOEUVERS_FILE_NAME = "manoeuvres_Jason-2.yaml"
TLE_FILE_NAME = "Jason-2.tle"

params = TLE_Lifetime_Analysis_Parameters()
f = open(params.manoeuver_files_directory + MANOEUVERS_FILE_NAME, "r")
list_of_manoeuvre_datetimes = yaml.safe_load(f)["manoeuvre_timestamps"]

list_of_skyfield_earthSatellites = skyfield_load.tle_file(params.TLE_files_directory + TLE_FILE_NAME, reload=False)
df_TLE_keplerian_elements = convert_skyfield_earthSatellites_into_dataframe_of_keplerian_elements(list_of_skyfield_earthSatellites)
df_TLE_propagated_keplerian_elements = convert_skyfield_earthSatellites_into_dataframe_of_keplerian_elements(list_of_skyfield_earthSatellites, date_offset=1)

mu = 3.986004418e14
mean_SMA_vals = []
orientation = []
for sat in list_of_skyfield_earthSatellites:

    radians_per_second = sat.model.no_kozai / 60
    mean_SMA_vals.append(1e-3 * (
            astropy.constants.GM_earth.value ** (1/3) /
            (radians_per_second) ** (2/3)
    )
                         )

mean_SMA_vals = np.array(mean_SMA_vals)

mean_x_vals = []
mean_RIC_vals = []
print(dir(list_of_skyfield_earthSatellites[0]))
mean_SMA_vals2 = []

for sat in list_of_skyfield_earthSatellites:
    mean_x_vals.append(sat._position_and_velocity_TEME_km(sat.epoch)[0])
    mean_RIC_vals.append(eci_2_ric(sat._position_and_velocity_TEME_km(sat.epoch)[0], sat._position_and_velocity_TEME_km(sat.epoch)[1])[0])
    mean_SMA_vals2.append(sat.model.radiusearthkm * sat.model.am)
    #print(sat._position_and_velocity_t_e_m_e_km(sat.epoch))
    #quit()

propagated_to_mean_diff = [0]
propagated_to_osculating_diff = [0]
propagated_mean_to_mean_s_m_a_diff = [0]
SMA_diff = [0]
for i in range(len(df_TLE_keplerian_elements) - 1):
    propagated_to_mean_diff.append(df_TLE_propagated_keplerian_elements["_u"].iloc[i] - mean_RIC_vals[1 + i][0])
    propagated_to_osculating_diff.append(df_TLE_propagated_keplerian_elements["_u"].iloc[i] - df_TLE_keplerian_elements["_u"].iloc[1+i])
    propagated_mean_to_mean_s_m_a_diff.append(mean_SMA_vals2[i + 1] - df_TLE_propagated_keplerian_elements["mean semi-major axis"].iloc[i])
    SMA_diff.append(mean_SMA_vals[i + 1] - mean_SMA_vals[i])



#print(propagated_mean_to_mean_s_m_a_diff)

df_TLE_keplerian_elements["diff with propagations"] =  propagated_to_osculating_diff
df_TLE_keplerian_elements["propagations diff with mean"] = propagated_to_mean_diff
df_TLE_keplerian_elements["propagations mean diff with mean"] = propagated_mean_to_mean_s_m_a_diff
df_TLE_keplerian_elements["_s_m_a_diff"] = SMA_diff

seriespropagated_to_mean_diff = df_TLE_keplerian_elements["propagations diff with mean"][DATE_RANGE[0]:DATE_RANGE[1]]
seriespropagated_diff = df_TLE_keplerian_elements["diff with propagations"][DATE_RANGE[0]:DATE_RANGE[1]]
#series_propagated_mean_to_mean_s_m_a_diff = df_t_l_e_keplerian_elements["propagations mean diff with mean"][_d_a_t_e_r_a_n_g_e[0]:_d_a_t_e_r_a_n_g_e[1]]
series_propagated_mean_to_mean_s_m_a_diff = df_TLE_keplerian_elements["propagations mean diff with mean"][DATE_RANGE[0]:DATE_RANGE[1]]
series_s_m_a_diff = df_TLE_keplerian_elements["_s_m_a_diff"][DATE_RANGE[0]:DATE_RANGE[1]]

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14}

matplotlib.rc('font', **font)

plt.figure(figsize=(15, 4))
plt.subplots_adjust(bottom=0.15)

plt.plot(
    #seriespropagated_to_mean_diff,
    #seriespropagated_diff,
    #series_propagated_mean_to_mean_s_m_a_diff,
    series_s_m_a_diff,
    c="b",
    marker="s",
    # label="_propagations _diff with _mean",
    markersize=4,
    alpha=0.75,
)

plt.plot(
    #seriespropagated_to_mean_diff,
    #seriespropagated_diff,
    series_propagated_mean_to_mean_s_m_a_diff,
    #series_s_m_a_diff,
    c="g",
    marker="s",
    # label="_propagations _diff with _mean",
    markersize=4,
    alpha=0.75,
)

#plt.xlabel("_time _epochs")
plt.ylabel("_in-track position difference (km)")
plt.xticks(rotation=20)
plt.xlim([datetime.datetime.fromisoformat(DATE_RANGE[0]),
          datetime.datetime.fromisoformat(DATE_RANGE[1])])
plt.tight_layout()
plt.show()