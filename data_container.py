import pathlib
import pandas as pd
import numpy as np
import pathlib
import json


script_directory = pathlib.Path(__file__).resolve().parent

EVENT_CODE = "mock_data"

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/scouted_data.csv')
    scouted_data[['Team Number', 'Match Number']] = scouted_data[['Team Number', 'Match Number']].astype("string")

    return scouted_data

def load_pit_data():
    pit_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/pit_data.csv')
    pit_data['Team Number'] = pit_data['Team Number'].astype("string")

    return pit_data

def get_Teams_in_Match(match_number):
    with open(script_directory / f'data/{EVENT_CODE}/tba_matches.json', 'r') as f:
        matches_json = json.load(f)
        for match in matches_json:
            if str(match["match_number"]) == str(match_number):
                teams = []
                for team_key in match["alliances"]["blue"]["team_keys"]:
                    teams.append(team_key.replace("frc", ""))
                for team_key in match["alliances"]["red"]["team_keys"]:
                    teams.append(team_key.replace("frc", ""))
                return teams
    return []

def load_match_numbers():
    with open(script_directory / f'data/{EVENT_CODE}/tba_matches.json', 'r') as f:
        matches_json = json.load(f)
        match_numbers = sorted(set(str(m["match_number"]) for m in matches_json), key=lambda x: int(x))
    return match_numbers