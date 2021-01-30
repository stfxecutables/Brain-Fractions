from pathlib import Path

import numpy as np
import pandas as pd

from src.read_files import read_aseg, read_rhwgpct, read_rhaparc, read_wmparc, read_lhwgpct, read_lhaparc


def get_wm(data_dir: Path) -> pd.DataFrame:
    """
    function to get white matter measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing white matter measurements, see DATA_COLUMNS in src/read_files for column names
    """
    wmparc = read_wmparc(data_dir)
    aseg = read_aseg(data_dir)
    wm_measurements = wmparc.append(aseg, ignore_index=True)

    # the file meta/white matter roi contains the regions of interest for white matter measurements
    wm_roi = np.loadtxt(Path("meta/white matter roi"), dtype=str)

    wm_measurements = wm_measurements[wm_measurements["Region name"].isin(wm_roi)].reset_index(drop=True)

    return wm_measurements


def get_gm(data_dir: Path) -> pd.DataFrame:
    """
    function to get grey matter measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing grey matter measurements, see DATA_COLUMNS in src/read_files for column names
    """
    lhaparc = read_lhaparc(data_dir)
    rhaparc = read_rhaparc(data_dir)
    lhwgpct = read_lhwgpct(data_dir)
    rhwgpct = read_rhwgpct(data_dir)
    aseg = read_aseg(data_dir)
    gm_measurements = lhaparc.append((lhwgpct, rhaparc, rhwgpct, aseg), ignore_index=True)

    # the file meta/grey matter roi contains the regions of interest for grey matter measurements
    gm_roi = np.loadtxt(Path("meta/grey matter roi"), dtype=str)

    gm_measurements = gm_measurements[gm_measurements["Region name"].isin(gm_roi)].reset_index(drop=True)

    return gm_measurements


def get_contrast(data_dir: Path) -> pd.DataFrame:
    """
    function to calculate contrast measurements by dividing white matter measurements by corresponding grey matter
    measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing contrast ratios, see DATA_COLUMNS in src/read_files for column names
    """
    wm_measurements = get_wm(data_dir)
    gm_measurements = get_gm(data_dir)

    ratios = pd.DataFrame(columns=wm_measurements.columns)

    for i, this_wm in wm_measurements.iterrows():
        region_name = this_wm["Region name"]
        type = this_wm["Measurement type"]
        hemisphere = this_wm["Hemisphere"]
        matter = this_wm["Matter"]

        # Not all measurements have the same name, so we need to handle some case by case
        if region_name == "Left-Cerebellum-White-Matter":
            corresponding_region = "Left-Cerebellum-Cortex"
        elif region_name == "lhCerebralWhiteMatter":
            corresponding_region = "lhCortex"
        elif region_name == "Right-Cerebellum-White-Matter":
            corresponding_region = "Right-Cerebellum-Cortex"
        elif region_name == "rhCerebralWhiteMatter":
            corresponding_region = "rhCortex"
        elif region_name == "CerebralWhiteMatter":
            corresponding_region = "Cortex"
        else:
            corresponding_region = region_name

        # Find corresponding measurement
        this_gm = gm_measurements[(gm_measurements["Region name"] == corresponding_region) &\
                  (gm_measurements["Measurement type"] == type) & \
                  (gm_measurements["Hemisphere"] == hemisphere)]

        value = float(this_wm["Value"]) / float(this_gm["Value"].values[0])

        ratios = ratios.append(
            {
                "Region name": region_name + " / " + corresponding_region,
                "Measurement type": type + " / " + type,
                "Matter": matter + " / " + this_gm["Matter"].values[0],
                "Hemisphere": hemisphere,
                "Value": value
            }, ignore_index=True
        )

    return ratios
