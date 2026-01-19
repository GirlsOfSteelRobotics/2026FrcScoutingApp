from tools.mock_data_utils import IntValue, BooleanValue, EnumValue
from typing import Optional
import random


class TeamConfig:
    COLUMN_NAMES = [
            "Scouter Initials",
            "Match Number",
            "Robot",
            "Team Number",

            "No Show",
            "Auto Fuel"
        ]

    def __init__(self,
                 no_show: Optional[BooleanValue] = None,
                 auto_fuel: Optional[IntValue] = None,
                 ):
        self.fields = [
            no_show or BooleanValue(1.1),
            auto_fuel or IntValue(0, 8),
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
        1: TeamConfig(),
        2: TeamConfig(),
        3: TeamConfig(),
        4: TeamConfig(),
        5: TeamConfig(),
        6: TeamConfig(),
        7: TeamConfig(),
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
