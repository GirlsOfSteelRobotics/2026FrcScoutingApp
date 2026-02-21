from tools.mock_data_utils import IntValue, BooleanValue, EnumValue
from typing import Optional
import random
import json


class TeamConfig:
    COLUMN_NAMES = [
            "Scouter Initials",
            "Match Number",
            #"Robot",
            "Team Number",

            "No Show",

            "Auto Fuel",
            "Auto Climbing Status",
            "Auto Human Player Score",

            "Teleop Fuel",
            "Teleop Fuel Passed",
            "Endgame Climbing Level"
        ]

    def __init__(self,
                 no_show: Optional[BooleanValue] = None,
                 auto_fuel: Optional[IntValue] = None,
                 auto_climb_status: Optional[BooleanValue] = None,
                 auto_hp_score: Optional[IntValue] = None,
                 teleop_fuel: Optional[IntValue] = None,
                 teleop_fuel_passed: Optional[IntValue] = None,
                 eg_level: Optional[EnumValue] = None


                 ):
        self.fields = [
            no_show or BooleanValue(.5),
            auto_fuel or IntValue(0, 16),
            auto_climb_status or BooleanValue(.5),
            auto_hp_score or IntValue(0, 16),
            teleop_fuel or IntValue(0, 200),
            teleop_fuel_passed or IntValue(0, 200),
            eg_level or EnumValue(["None", "L1", "L2", "L3"], [25, 25, 25, 25])
            #test data

            #endgame_position or EnumValue(["N", "P"], [50, 50])
        ]

    def generate_data(self):
        data = []

        for field in self.fields:
            data.append(field.get_value())

        return data


def populate_tba_and_statbotics_match(tba_matches, statbotics_matches, match_number, match_teams):
        match_key = f"2025tnkn_qm{match_number}"
        tba_matches.append({
            "alliances": {
                "blue": { "team_keys": [f"frc{x}" for x in match_teams[3:]]},
                "red": { "team_keys": [f"frc{x}" for x in match_teams[0:3]]},
            },
            "key": match_key,
            "match_number": match_number
        })

        statbotics_matches.append({
            "key": match_key,
            "match_number": match_number,
            "alliances": {
                "red": { "team_keys": match_teams[0:3]},
                "blue": { "team_keys": match_teams[3:]},
            }
        })


def populate_from_previous_event():
    teams = set()
    matches = []

    with open("data/2025tnkn/statbotics_matches.json", 'r') as f:
        matches_json = json.load(f)

    for match_json in matches_json:
        match_number = match_json["match_number"]
        red_teams = match_json["alliances"]["red"]["team_keys"]
        blue_teams = match_json["alliances"]["blue"]["team_keys"]
        teams.update(red_teams + blue_teams)

        matches.append([match_number] + red_teams + blue_teams)

    teams = sorted(teams)

    team_configs = {}

    for team in teams:
        team_configs[team] = TeamConfig()

    return team_configs, teams, matches


def populate_randomly():
    team_configs = {
        254: TeamConfig(),
        1678: TeamConfig(),
        4467: TeamConfig(),
        2056: TeamConfig(),
        118: TeamConfig(),
        67: TeamConfig(),
        8393: TeamConfig(),
        3504: TeamConfig(
            auto_fuel=IntValue(min_value=5, max_value=30)
        ),
    }
    team_numbers = list(team_configs.keys())

    matches = []

    for match_i in range(60):
        match_teams = random.sample(team_numbers, 6)

        matches.append([match_i + 1, *match_teams])

    return team_configs, team_numbers, matches


def main():
    random.seed(3504)

    # team_configs, team_numbers, matches = populate_randomly()
    team_configs, team_numbers, matches = populate_from_previous_event()



    tba_teams = [{
        "key": f"frc{team_number}",
        "team_number": team_number
    } for team_number in team_numbers]

    statbotics_teams = [{
        "team": team_number,
    } for team_number in team_numbers]

    scouted_data = []
    scouted_data.append(TeamConfig.COLUMN_NAMES)

    tba_matches = []
    statbotics_matches = []

    num_scouted_matches = 28
    for i, match_data in enumerate(matches):
        match_number = match_data[0]
        teams = match_data[1:]

        populate_tba_and_statbotics_match(tba_matches, statbotics_matches, match_number, teams)

        if i < num_scouted_matches:
            for team in teams:
                scouted_data.append(["abc", match_number, team, *team_configs[team].generate_data()])

    with open("data/mock_data/scouted_data.csv", 'w') as f:
        for row in scouted_data:
            f.write(",".join(str(x) for x in row))
            f.write("\n")

    with open("data/mock_data/tba_teams.json", 'w') as f:
        json.dump(tba_teams, f, indent=4)

    with open("data/mock_data/statbotics_teams.json", 'w') as f:
        json.dump(statbotics_teams, f, indent=4)

    with open("data/mock_data/tba_matches.json", 'w') as f:
        json.dump(tba_matches, f, indent=4)

    with open("data/mock_data/statbotics_matches.json", 'w') as f:
        json.dump(statbotics_matches, f, indent=4)



if __name__ == "__main__":
    # python3 -m tools.generate_mock_data
    main()

