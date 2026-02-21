import pathlib
from metadata import CURRENT_EVENT

from utils.statbotics_utils import (
    download_statbotics_matches,
    download_statbotics_event_teams,
)

from utils.tba_utils import download_tba_event_matches, download_tba_event_teams


def download_external_data(event):
    """
    Downloads the external data (TBA) for a specific event
    :param event: The event key
    """
    script_directory = pathlib.Path(__file__).resolve().parent
    data_directory = script_directory / "data" / event
    data_directory.mkdir(parents=True, exist_ok=True)

    # Download TBA data
    download_tba_event_matches(event, data_directory / "tba_matches.json")
    download_tba_event_teams(event, data_directory / "tba_teams.json")

    # Download Statbotics data
    download_statbotics_matches(event, data_directory / "statbotics_matches.json")
    download_statbotics_event_teams(event, data_directory / "statbotics_teams.json")


if __name__ == "__main__":
    download_external_data(CURRENT_EVENT)