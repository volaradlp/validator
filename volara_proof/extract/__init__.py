import zipfile
import json
from volara_proof.models.user_data import UserData
from volara_proof.buffers.tweets import Tweets


def extract_user_data(zip_file_path: str) -> UserData | None:
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        file_names = zip_ref.namelist()
        if "user_data.json" in file_names:
            with zip_ref.open("user_data.json", "r") as file:
                return UserData(**json.load(file))
        else:
            return None


def extract_data(zip_file_path: str):
    """
    Extracts the data from the zip file
    :param zip_file_path: Path to the zip file
    :return: Object containing a quality score and whether the file is valid

    Throws
        If extract contraints are not respected
    """
    required_files = ["tweets.data"]

    # Load data from zip file and validate that it contains the required files
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            file_names = zip_ref.namelist()
            if not all(file in file_names for file in required_files):
                raise ValueError(
                    f"Zip file does not contain all required files: {required_files}"
                )

            with zip_ref.open("tweets.data", "r") as file:
                file_bytes = file.read()
                return Tweets.GetRootAs(file_bytes)
    except zipfile.BadZipFile:
        with open(zip_file_path, "rb") as f:
            file_bytes = f.read().strip(b"\x00")
            return Tweets.GetRootAs(file_bytes)
