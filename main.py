import sys
from pathlib import Path
from typing import List

from src.asymmetry_ratios import get_asymmetry
from src.contrast_ratios import get_contrast


def save_ratios(options: List[str], input_dir: Path, output_dir: Path, filename: str) -> None:
    """
    function to save ratios to given destination directory. The name of the ratio files will have the same name as
    the data folder and will have either "_asymmetry" or "_contrast" appended depending on the ratio type
    :param options: List containing either "asymmetry", "contrast" or both (default)
    :param input_dir: path to FreeSurfer output folder for MRI
    :param output_dir: directory where the files are to be written to
    :param filename: string containing the file name (name of the data folder)
    :return: None
    """
    for option in options:
        if option == "asymmetry":
            a_ratios = get_asymmetry(input_dir)
            a_ratios.to_csv(output_dir.joinpath(filename + "_asymmetry.csv"), index=False)
        if option == "contrast":
            c_ratios = get_contrast(input_dir)
            c_ratios.to_csv(output_dir.joinpath(filename + "_contrast.csv"), index=False)
            pass


if __name__ == '__main__':
    assert len(sys.argv) >= 3, "Program needs input and output directories. See usage for more info"
    data_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])

    file_name = str(data_dir.as_posix()).split("/")[-1]
    if len(sys.argv) == 4:
        save_ratios([sys.argv[3]], data_dir, out_dir, file_name)
    elif len(sys.argv) == 3:
        save_ratios(["contrast", "asymmetry"], data_dir, out_dir, file_name)

    print("Program completed successfully!")

