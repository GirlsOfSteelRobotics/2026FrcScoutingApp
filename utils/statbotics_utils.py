import json
from pathlib import Path
import pandas as pd
from typing import Dict, Any


############################################
# Statbotics Matches
############################################

def download_statbotics_matches(event: str, output_path: Path, quals_only=True):
    """
    :param event: The event key (i.e. 2025casj)
    :param output_path: The path to save the json to
    :param quals_only: If true, only data from qualification matches will be saved
    """
    import statbotics
    sb = statbotics.Statbotics()
    elims = False if quals_only else None
    try:
        data = sb.get_matches(event=event, elims=elims)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
    except UserWarning:
        print("Could not load statbotics match data")


def load_statbotics_matches(filename: Path) -> pd.DataFrame:
    """
    :param filename: The filename to load
    :return: The data in the form of a dataframe
    """
    if not filename.exists():
        print("Statbotics match file does not exist!")
        return pd.DataFrame()
    with open(filename, "r") as f:
        json_data = json.load(f)
    return statbotics_matches_json_to_dataframe(json_data)


def statbotics_matches_json_to_dataframe(json_data: Dict[str, Any]) -> pd.DataFrame:
    """
    :param json_data: The json dictionary
    :return: The data frame
    """
    # There is nothing interesting to precalculate, so we just shove the json into a dataframe
    return pd.json_normalize(json_data)


############################################
# Statbotics Events/Teams
############################################

def download_statbotics_event_teams(event: str, output_path: Path):
    """
    :param event: The event key (i.e. 2025casj)
    :param output_path: The location on disk to save the file
    """
    import requests
    url = f"https://api.statbotics.io/v3/team_events?event={event}"
    response = requests.get(url)
    with open(output_path, "w") as f:
        as_json = response.json()
        json.dump(as_json, f, indent=4)


def load_statbotics_teams(filename: Path):
    """
    :param filename: The path to the cached json file.
    :return: The dataframe representing the json and some helpful precalculated aggregate data
    """
    with open(filename, "r") as f:
        json_data = json.load(f)
    return statbotics_teams_json_to_dataframe(json_data)


def statbotics_teams_json_to_dataframe(json_data: Dict[str, Any]) -> pd.DataFrame:
    """
    :param json_data: The json dictionary
    :return: The data frame
    """
    output = pd.json_normalize(json_data)
    return output