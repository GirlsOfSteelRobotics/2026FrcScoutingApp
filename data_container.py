import pathlib
import pandas as pd
import numpy as np
import json
from metadata import CURRENT_EVENT

EVENT_KEY = CURRENT_EVENT

custom_colors = ["#A07761", "#6C4E3E", "#D6BFA6"]

script_directory = pathlib.Path(__file__).resolve().parent

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{EVENT_KEY}/scouted_data.csv')
    scouted_data.columns = scouted_data.columns.str.strip()

    # Rename if raw column names are present
    if "team_key" in scouted_data.columns:
        scouted_data["team_key"] = scouted_data["team_key"].str[3:]
        scouted_data.rename(columns={
            "team_key": "Team Number",
            "match_number": "Match Number",
            "totalAutofuelscored": "Auto Fuel",
            "totalTeleopfuelscored": "Teleop Fuel",
            "TotalAutofuelPassed": "Auto Fuel Passed",
            "TotalTeleopfuelPassed": "Teleop Fuel Passed",
            "totalfuelscored": "Total Fuel",
            "Totalfuelpassed": "Total Fuel Passed",
            "totalAutoPoints": "Total Auto Points",
            "totalTeleopPoints": "Total Teleop Points",
            "totalEndgamePoints": "Endgame Points",
            "contributedPoints": "Contributed Points",
            "AutoClimb": "Auto Climbing Status",
            "Climb": "Endgame Climbing Level"
        }, inplace=True)

    # Ensure Team Number and Match Number are strings
    scouted_data = scouted_data.dropna(subset=["Team Number", "Match Number"])

    # Force all numeric columns to numbers, replacing anything unparseable with 0
    numeric_cols = [
        "Auto Fuel", "Teleop Fuel", "Auto Fuel Passed", "Teleop Fuel Passed",
        "Total Fuel", "Total Fuel Passed", "Total Auto Points", "Total Teleop Points",
        "Endgame Points", "Contributed Points"
    ]
    for col in numeric_cols:
        if col in scouted_data.columns:
            scouted_data[col] = pd.to_numeric(scouted_data[col], errors='coerce').fillna(0).astype(int)

    # Fix Auto Climbing Status to be a proper boolean
    if "Auto Climbing Status" in scouted_data.columns:
        scouted_data["Auto Climbing Status"] = scouted_data["Auto Climbing Status"].astype(str).str.lower().isin(
            ['true', '1', 'yes']
        )

    # Fix Endgame Climbing Level — convert to points safely
    def convert_endgame_to_points(level):
        if pd.isna(level):
            return 0
        level_str = str(level).upper().strip()
        return {"L1": 10, "L2": 20, "L3": 30}.get(level_str, 0)

    if "Endgame Climbing Level" in scouted_data.columns:
        scouted_data["Endgame Teleop Points"] = scouted_data["Endgame Climbing Level"].apply(convert_endgame_to_points).astype(int)
    else:
        scouted_data["Endgame Teleop Points"] = 0

    scouted_data["Auto Climb Points"] = scouted_data["Auto Climbing Status"].apply(lambda x: 15 if x else 0).astype(int)

    # All derived columns — everything is int at this point so no type errors
    scouted_data["All Auto"] = scouted_data["Auto Fuel"] + scouted_data["Auto Climb Points"]
    scouted_data["All Teleop"] = scouted_data["Teleop Fuel"] + scouted_data["Endgame Teleop Points"]
    scouted_data["All Endgame"] = scouted_data["Endgame Teleop Points"]
    scouted_data["Auto and Endgame"] = scouted_data["All Auto"] + scouted_data["All Endgame"]
    scouted_data["Total Fuel"] = scouted_data["Auto Fuel"] + scouted_data["Teleop Fuel"]
    scouted_data["Endgame Fuel"] = scouted_data["Endgame Teleop Points"]
    scouted_data["Total Climb Points"] = scouted_data["Auto Climb Points"] + scouted_data["Endgame Teleop Points"]

    return scouted_data


def load_pit_data():
    pit_data = pd.read_csv(script_directory / f'data/{EVENT_KEY}/pit_data.csv')
    pit_data.columns = pit_data.columns.str.strip()
    pit_data["team_key"] = pit_data["team_key"].str.replace("frc", "", regex=False)
    pit_data.rename(columns={"team_key": "Team Number"}, inplace=True)
    pit_data['Team Number'] = pit_data['Team Number'].astype("string")
    return pit_data


def get_Teams_in_Match(match_number):
    with open(script_directory / f'data/{EVENT_KEY}/tba_matches.json', 'r') as f:
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
    with open(script_directory / f'data/{EVENT_KEY}/tba_matches.json', 'r') as f:
        matches_json = json.load(f)
        match_numbers = sorted(set(str(m["match_number"]) for m in matches_json), key=lambda x: int(x))
    return match_numbers


def load_statbotics_matches(match_number):
    with open(script_directory / f'data/{EVENT_KEY}/statbotics_matches.json', 'r') as f:
        matches_json = json.load(f)
        for match in matches_json:
            if str(match["match_number"]) == str(match_number):
                red_teams = [str(t) for t in match["alliances"]["red"]["team_keys"]]
                blue_teams = [str(t) for t in match["alliances"]["blue"]["team_keys"]]
                return {
                    "match_number": match["match_number"],
                    "red_teams": red_teams,
                    "blue_teams": blue_teams,
                    "pred_red_score": match.get("pred_red_score"),
                    "pred_blue_score": match.get("pred_blue_score"),
                }
    return None