import pandas as pd
import os
import re


class CSVError(Exception):
    """Error to be raised if a file is not a CSV"""

    def __init__(self, msg):
        self.msg = msg


def data_information(filepath: str):
    """Return column_names and dtypes of [c|t]sv files.
    :param filepath: absolute or relative path of data

    :return: Dataframe with column_names, column_dtypes
    """
    # split the filepath and get the filename
    _, filename = os.path.split(filepath)
    # regular expression pattern to check if [c|t]sv
    pattern = re.compile(r"[ct]sv")
    # check in filename for pattern if not raise CSVError
    if pattern.search(filename) is None:
        raise CSVError(f"Can't determine if {filename} is a CSV")
    # create dataframe from file with sep depending on type
    if "csv" in filename:
        df = pd.read_csv(filepath)
    elif "tsv" in filename:
        df = pd.read_csv(filepath, sep="\t")

    # create dataframe with column names and dtypes
    result = pd.DataFrame({
        "column_names": df.columns.to_list(),
        "dtypes": df.dtypes
    })

    return result