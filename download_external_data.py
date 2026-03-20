import pathlib
from metadata import SCOUT_RADIOZ_ORG, CURRENT_EVENT

from utils.statbotics_utils import (
    download_statbotics_matches,
    download_statbotics_event_teams,
)


from utils.tba_utils import download_tba_event_matches, download_tba_event_teams
from utils.scout_radioz_utils import (
        download_scout_radioz_match_scouting,
        download_scout_radioz_pit_scouting,
    )

def download_external_data(event):
    """
    Downloads the external data (TBA) for a specific event
    :param event: The event key
    """
    script_directory = pathlib.Path(__file__).resolve().parent
    data_directory = script_directory / "data" / event
    data_directory.mkdir(parents=True, exist_ok=True)

    #Download ScoutRadioz data
    download_scout_radioz_match_scouting(
        SCOUT_RADIOZ_ORG, event, data_directory / "scouted_data.csv")
    download_scout_radioz_pit_scouting(
        SCOUT_RADIOZ_ORG, event, data_directory / "pit_data.csv")

    # Download TBA data
    download_tba_event_matches(event, data_directory / "tba_matches.json")
    download_tba_event_teams(event, data_directory / "tba_teams.json")

    # Download Statbotics data
    download_statbotics_matches(event, data_directory / "statbotics_matches.json")
    download_statbotics_event_teams(event, data_directory / "statbotics_teams.json")


if __name__ == "__main__":
        # python3 -m download_external_data
        download_external_data("2026paca")