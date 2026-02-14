import pathlib
from metadata import CURRENT_EVENT
from utils.tba_utils import download_tba_event_matches

def download_external_data(event):
    """
    Downloads the external data (TBA) for a specific event
    :param event: The event key
    """
    script_directory = pathlib.Path(__file__).resolve().parent
    data_directory = script_directory / "data" / event
    data_directory.mkdir(parents=True, exist_ok=True)

    #
    download_tba_event_matches(event, data_directory / "tba_matches.json")


if __name__ == "__main__":
    download_external_data(CURRENT_EVENT)