import pandas as pd
import datetime
import yaml
from yaml import CLoader as Loader

DATA_DIR = "processed_files/"
MAX_NUM_COLS = 100

DORIS_file_names = [
    "DORIS_beacons_Sentinel-3A.yaml",
    "DORIS_beacons_Sentinel-3B.yaml",
    "DORIS_beacons_Sentinel-6A.yaml",
    "DORIS_beacons_Jason-1.yaml",
    "DORIS_beacons_Jason-2.yaml",
    "DORIS_beacons_Jason-3.yaml",
    "DORIS_beacons_SARAL.yaml",
    "DORIS_beacons_CryoSat-2.yaml",
    "DORIS_beacons_Haiyang-2A.yaml",
]

TLE_file_names = [
    "Sentinel-3A.tle",
    "Sentinel-3B.tle",
    "Sentinel-6A.tle",
    "Jason-1.tle",
    "Jason-2.tle",
    "Jason-3.tle",
    "SARAL.tle",
    "CryoSat-2.tle",
    "Haiyang-2A.tle",
]

satellite_names = [
    "Sentinel-3A",
    "Sentinel-3B",
    "Sentinel-6A",
    "Jason-1",
    "Jason-2",
    "Jason-3",
    "SARAL",
    "CryoSat-2",
    "Haiyang-2A",
]

for i in range(len(DORIS_file_names)):
    f = open(DATA_DIR + DORIS_file_names[i], 'r')
    DORIS_yaml = yaml.load(f, Loader=Loader)
    print("read YAML")
    df_DORIS = pd.json_normalize(DORIS_yaml)
    print(df_DORIS)