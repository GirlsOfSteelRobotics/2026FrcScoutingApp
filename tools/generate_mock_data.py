from tools.mock_data_utils import IntValue, BooleanValue, EnumValue
from typing import Optional
import random


class TeamConfig:
    COLUMN_NAMES = [
            "Scouter Initials",
            "Match Number",
            #"Robot",
            "Team Number",

            "No Show",

            "Auto Fuel",
            "Auto Climbing Status",
            #"Auto Human Player Score",

            "Teleop Fuel",
            #"Teleop Human Player Score",
            "Teleop Fuel Passed",
            "Endgame Climbing Level"
        ]

    def __init__(self,
                 no_show: Optional[BooleanValue] = None,
                 auto_fuel: Optional[IntValue] = None,
                 auto_climb_status: Optional[BooleanValue] = None,
                # auto_hp_score: Optional[IntValue] = None,
                 teleop_fuel: Optional[IntValue] = None,
                 teleop_fuel_passed: Optional[IntValue] = None,
                # teleop_hp_score: Optional[IntValue] = None,
                 eg_level: Optional[EnumValue] = None


                 ):
        self.fields = [
            no_show or BooleanValue(.10),
            auto_fuel or IntValue(0, 16),
            auto_climb_status or BooleanValue(.5),
            #auto_hp_score or IntValue(0, 16),
            teleop_fuel or IntValue(0, 200),
            teleop_fuel_passed or IntValue(0,200),
            #teleop_hp_score or IntValue(0, 48),
            eg_level or EnumValue(["None", "L1", "L2", "L3"], [25, 25, 25, 25])
            #test data

            #endgame_position or EnumValue(["N", "P"], [50, 50])
        ]

    def generate_data(self):
        data = []

        for field in self.fields:
            data.append(field.get_value())

        return data



def main():
    random.seed(3504)

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

    rows = []
    rows.append(TeamConfig.COLUMN_NAMES)

    num_matches = 10
    for match_i in range(num_matches):
        match_teams = random.sample(team_numbers, 6)

        for team_i in range(6):
            rows.append(["abc", match_i + 1, match_teams[team_i], *team_configs[match_teams[team_i]].generate_data()])

    with open("data/mock_data/scouted_data.csv", 'w') as f:
        for row in rows:
            f.write(",".join(str(x) for x in row))
            f.write("\n")


if __name__ == "__main__":
    # python3 -m tools.generate_mock_data
    main()

