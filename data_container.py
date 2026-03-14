import pathlib
import pandas as pd
import numpy as np
import pathlib
import json


script_directory = pathlib.Path(__file__).resolve().parent

df = pd.read_csv("data/2026nyro/match_scouting.csv")

EVENT_CODE = "2026nyro"

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{"2026nyro"}/match_scouting.csv')
    print(scouted_data["team_key"])
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
    scouted_data[["Team Number", "Match Number"]] = scouted_data[["Team Number", "Match Number"]].astype("string")


    def convert_endgame_to_points(level):
        if pd.isna(level):
            return 0
        level_str = str(level).upper().strip()
        return {"L1": 10, "L2": 20, "L3": 30}.get(level_str, 0)

    if scouted_data["Auto Climbing Status"].dtype == 'object':
        scouted_data["Auto Climbing Status"] = scouted_data["Auto Climbing Status"].astype(str).str.lower().isin(
            ['true', '1', 'yes'])
    scouted_data["Auto Climb Points"] = scouted_data["Auto Climbing Status"].apply(lambda x: 15 if x else 0)

    scouted_data["Endgame Teleop Points"] = scouted_data["Endgame Climbing Level"].apply(convert_endgame_to_points)
    scouted_data["Auto Climb Points"] = scouted_data["Auto Climbing Status"].apply(lambda x: 15 if x else 0)
    scouted_data["All Auto"] = scouted_data["Auto Fuel"] + scouted_data["Auto Climb Points"]
    scouted_data["All Teleop"] = scouted_data["Teleop Fuel"] + scouted_data["Endgame Teleop Points"]
    scouted_data["All Endgame"] = scouted_data["Endgame Teleop Points"]
    scouted_data["Auto and Endgame"] = scouted_data["All Auto"] + scouted_data["All Endgame"]
    scouted_data["Total Fuel"] = scouted_data["Auto Fuel"] + scouted_data["Teleop Fuel"]
    scouted_data["Endgame Fuel"] = scouted_data["Endgame Teleop Points"]
    scouted_data["Total Climb Points"] = scouted_data["Auto Climb Points"] + scouted_data["Endgame Teleop Points"]

    return scouted_data

def load_pit_data():
    pit_data = pd.read_csv(script_directory / f'data/{"2026nyro"}/pit_scouting.csv')
    pit_data['Team Number'] = pit_data['Team Number'].astype("string")

    return pit_data

def get_Teams_in_Match(match_number):
    with open(script_directory / f'data/{"2026nyro"}/tba_matches.json', 'r') as f:
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
    with open(script_directory / f'data/{"2026nyro"}/tba_matches.json', 'r') as f:
        matches_json = json.load(f)
        match_numbers = sorted(set(str(m["match_number"]) for m in matches_json), key=lambda x: int(x))
    return match_numbers

if __name__ == "__main__":
    pit = load_pit_data()
    scouted = load_scouted_data()
    print("Pit teams:", sorted(pit["Team Number"].unique().tolist()))
    print("Scouted teams:", sorted(scouted["Team Number"].unique().tolist()))

def load_statbotics_matches(match_number):
    with open(script_directory / f'data/{"2026nyro"}/statbotics_matches.json', 'r') as f:
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
