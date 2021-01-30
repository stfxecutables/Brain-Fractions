import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.read_files import read_aseg, read_rhwgpct, read_rhaparc, read_wmparc, read_lhwgpct, read_lhaparc


def get_lh(data_dir: Path) -> pd.DataFrame:
    """
    function to get left hemisphere measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing left hemisphere measurements, see DATA_COLUMNS in src/read_files for column names
    """
    wmparc = read_wmparc(data_dir)
    aseg = read_aseg(data_dir)
    lhwgpct = read_lhwgpct(data_dir)
    lhaparc = read_lhaparc(data_dir)
    lh_measurements = wmparc.append((aseg, lhwgpct, lhaparc), ignore_index=True)

    # the file meta/lh roi contains the regions of interest for left hemisphere measurements
    lh_roi = np.loadtxt(Path("meta/lh roi"), dtype=str)

    lh_measurements = lh_measurements[
        lh_measurements["Region name"].isin(lh_roi) & (lh_measurements["Hemisphere"] == "Left")
    ].reset_index(drop=True)

    return lh_measurements


def get_rh(data_dir: Path) -> pd.DataFrame:
    """
    function to get right hemisphere measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing right hemisphere measurements, see DATA_COLUMNS in src/read_files for column names
    """
    wmparc = read_wmparc(data_dir)
    aseg = read_aseg(data_dir)
    rhwgpct = read_rhwgpct(data_dir)
    rhaparc = read_rhaparc(data_dir)
    rh_measurements = wmparc.append((aseg, rhwgpct, rhaparc), ignore_index=True)

    # the file meta/rh roi contains the regions of interest for right hemisphere measurements
    rh_roi = np.loadtxt(Path("meta/rh roi"), dtype=str)

    rh_measurements = rh_measurements[
        rh_measurements["Region name"].isin(rh_roi) & (rh_measurements["Hemisphere"] == "Right")
        ].reset_index(drop=True)

    return rh_measurements


def get_asymmetry(data_dir: Path):
    """
    function to calculate asymmetry measurements by dividing left hemisphere measurements by corresponding right
    hemisphere measurements
    :param data_dir: path to FreeSurfer output folder for MRI
    :return: dataframe containing asymmetry ratios, see DATA_COLUMNS in src/read_files for column names
    """
    lh_measurements = get_lh(data_dir)
    rh_measurements = get_rh(data_dir)

    ratios = pd.DataFrame(columns=lh_measurements.columns)

    for i, this_lh in lh_measurements.iterrows():
        region_name = this_lh["Region name"]
        type = this_lh["Measurement type"]
        hemisphere = this_lh["Hemisphere"]
        matter = this_lh["Matter"]

        corresponding_region = region_name

        # Measurements from aseg.stats have a left-right prefix
        if re.search("Left-", region_name):
            corresponding_region = "Right-" + re.split("Left-", region_name)[-1]

        this_rh = rh_measurements[(rh_measurements["Region name"] == corresponding_region) & \
                                  (rh_measurements["Measurement type"] == type) & \
                                  (rh_measurements["Matter"] == matter)]

        value = float(this_lh["Value"]) / float(this_rh["Value"].values[0])

        ratios = ratios.append(
            {
                "Region name": region_name + " / " + corresponding_region,
                "Measurement type": type + " / " + type,
                "Matter": matter,
                "Hemisphere": hemisphere + " / " + this_rh["Hemisphere"].values[0],
                "Value": value
            }, ignore_index=True
        )

    return ratios




