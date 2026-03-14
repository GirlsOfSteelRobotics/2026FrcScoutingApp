import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match, load_match_numbers, \
    load_statbotics_matches

df = load_scouted_data()
match_numbers = load_match_numbers()
all_teams = sorted(df["Team Number"].unique().tolist())

@module.ui
def general_match_ui():
    return ui.page_fluid(
        ui.layout_sidebar(
            ui.sidebar(
                ui.input_radio_buttons(
                    "selection_mode",
                    "Select By:",
                    choices=["Match Number", "Pick 6 Teams"],
                    selected="Match Number"
                ),
                ui.output_ui("match_list_combobox"),
            ),

                ui.navset_tab(
                #OVERALL
                    ui.nav_panel("Overall",
                                 ui.layout_column_wrap(
                                     ui.card(
                                         ui.output_ui("red_statbotics_prediction")
                                     ),
                                     ui.card(
                                         ui.output_ui("blue_statbotics_prediction")
                                     )
                                 ),
                                 ui.layout_column_wrap(
                                     ui.card(ui.output_ui("rp_energized"), height="490px"),
                                     ui.card(ui.output_ui("rp_supercharged"), height="490px"),
                                     ui.card(ui.output_ui("rp_climbing"), height="490px"),
                                     width=1 / 3,
                                 ),
                                 ),
                #AUTO
                    ui.nav_panel("Auto",
                                 ui.card(output_widget("auto_fuel_in_hub")),
                                        ui.card(output_widget("auto_climbing_frequency")),
                                 ),
                #TELEOP
                    ui.nav_panel("Teleop",
                                 ui.card(output_widget("teleop_fuel_in_hub")),
                                 ui.card(output_widget("teleop_fuel_passed_total")),
                                 ui.card(output_widget("teleop_fuel_passed_avg")),
                                 ),
                #ENDGAME
                ui.nav_panel("Endgame",
                ui.card(output_widget("endgame_positions_by_instance")),
                    ui.card(output_widget("endgame_positions_by_points")),
                    ui.card(output_widget("total_climbing_points")),
                    ui.card(output_widget("avg_climbing_points")),
                             )
            )
        )
    )

@module.server
def general_match_server(input, output, session):

    def get_teams_in_match():
        if input.selection_mode() == "Match Number":
            match_number = str(input.match_select())
            teams = get_Teams_in_Match(match_number)
        else:
            teams = [
                str(input.team1()), str(input.team2()), str(input.team3()),
                str(input.team4()), str(input.team5()), str(input.team6()),
            ]
        return df.loc[df["Team Number"].isin(teams)]

    def blue_df():
        if input.selection_mode() == "Match Number":
            match_number = str(input.match_select())
            teams = get_Teams_in_Match(match_number)[:3]  # blue is first 3 in your get_Teams_in_Match
        else:
            teams = [str(input.team1()), str(input.team2()), str(input.team3())]
        return df.loc[df["Team Number"].isin(teams)]

    def red_df():
        if input.selection_mode() == "Match Number":
            match_number = str(input.match_select())
            teams = get_Teams_in_Match(match_number)[3:]  # red is last 3
        else:
            teams = [str(input.team4()), str(input.team5()), str(input.team6())]
        return df.loc[df["Team Number"].isin(teams)]

    @render.ui
    def match_list_combobox():
        if input.selection_mode() == "Match Number":
            return ui.input_select(
                "match_select",
                "Match Number:",
                choices=match_numbers
            )
        else:
            return ui.div(
                ui.input_select("team1", "Team 1:", choices=all_teams),
                ui.input_select("team2", "Team 2:", choices=all_teams),
                ui.input_select("team3", "Team 3:", choices=all_teams),
                ui.input_select("team4", "Team 4:", choices=all_teams),
                ui.input_select("team5", "Team 5:", choices=all_teams),
                ui.input_select("team6", "Team 6:", choices=all_teams),
            )

# OVERALL STATS
    @render.ui
    def red_statbotics_prediction():
        match_num = int(input.match_select())
        statbotics_matches = load_statbotics_matches(match_num)
        print(statbotics_matches)
        return ui.value_box(
                title="Prediction RED",
                value=str(statbotics_matches["pred_red_score"])
            )

    @render.ui
    def blue_statbotics_prediction():
        match_num = int(input.match_select())
        statbotics_matches = load_statbotics_matches(match_num)
        print(statbotics_matches)
        return ui.value_box(
            title="Prediction BLUE",
            value=str(statbotics_matches["pred_blue_score"])
        )

    @render_widget
    def avg_fuel():
        new_df = get_teams_in_match()
        avg_team = new_df.groupby("Team Number").mean(numeric_only=True).reset_index()

        # Calculate total fuel
        avg_team["Total Fuel"] = avg_team["Auto Fuel"] + avg_team["Teleop Fuel"]

        # Sort by total fuel for better visualization
        avg_team = avg_team.sort_values("Total Fuel", ascending=True)

        # Create horizontal bar chart
        fig = px.bar(
            avg_team,
            x="Team Number",  # Teams on x-axis
            y="Total Fuel",  # Values on y-axis
            title="Average Fuel by Team (Sorted)",
            labels={"Total Fuel": "Average Fuel Score", "Team Number": "Team Number"},
            orientation='v',  # Horizontal bars
            text="Total Fuel"  # Show values
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(height=500)

        return fig

    @render.ui
    def rp_climbing():
        red = red_df().copy()
        blue = blue_df().copy()

        def calc_climbing_points(alliance_df):
            alliance_df["Auto Climbing Status"] = alliance_df["Auto Climbing Status"].fillna(False)
            return alliance_df.groupby("Team Number")["Total Climb Points"].mean().sum()

        red_climb = calc_climbing_points(red)
        blue_climb = calc_climbing_points(blue)

        def climb_status(total):
            status = "Traversal RP Likely" if total >= 50 else "Traversal RP Unlikely"
            return f"{total:.0f} pts - {status}"

        return ui.div(
            ui.value_box(title="RED Climbing RP Prediction", value=climb_status(red_climb), height="200px", showcase=None),
            ui.value_box(title="BLUE Climbing RP Prediction", value=climb_status(blue_climb), height="200px", showcase=None),
        )

    @render.ui
    def rp_energized():
        red = red_df().copy()
        blue = blue_df().copy()

        red_avg_fuel = (red["Auto Fuel"] + red["Teleop Fuel"]).mean() * 3
        blue_avg_fuel = (blue["Auto Fuel"] + blue["Teleop Fuel"]).mean() * 3

        def energized_status(avg):
            status = "Energized RP Likely" if avg >= 100 else "Energized RP Unlikely"
            return f"{avg:.0f} fuel - {status}"

        return ui.div(
            ui.value_box(title="RED Energized RP Prediction", value=energized_status(red_avg_fuel), height="200px", showcase=None),
            ui.value_box(title="BLUE Energized RP Prediction", value=energized_status(blue_avg_fuel), height="200px", showcase=None),
        )

    @render.ui
    def rp_supercharged():
        red = red_df().copy()
        blue = blue_df().copy()

        red_avg_fuel = (red["Auto Fuel"] + red["Teleop Fuel"]).mean() * 3
        blue_avg_fuel = (blue["Auto Fuel"] + blue["Teleop Fuel"]).mean() * 3

        def supercharged_status(avg):
            status = "Supercharged RP Likely" if avg >= 360 else "Supercharged RP Unlikely"
            return f"{avg:.0f} fuel - {status}"

        return ui.div(
            ui.value_box(title="RED Supercharged RP Prediction", value=supercharged_status(red_avg_fuel),
                         height="200px", showcase=None),
            ui.value_box(title="BLUE Supercharged RP Prediction", value=supercharged_status(blue_avg_fuel),
                         height="200px", showcase=None),
        )

# AUTO GRAPHS
    @render_widget
    def auto_fuel_in_hub():
        new_df = get_teams_in_match()
        avg_team = new_df.groupby("Team Number").mean(numeric_only=True)
        custom_colors = ["#CBB9A4", "#E6DAC8", "8A6C5F"]
        fig = px.bar(avg_team, y="Auto Fuel", title="Fuel in Hub (Auto) per Robot",
                     color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def auto_climbing_frequency():
        new_df = get_teams_in_match()
        auto_climbing_status_df = new_df.groupby("Team Number")["Auto Climbing Status"].value_counts().unstack(
            fill_value=0).reset_index()
        auto_climbing_status_df["Climb Freq"] = auto_climbing_status_df[True] / (
                auto_climbing_status_df[True] + auto_climbing_status_df[False])
        auto_climbing_status_df["No Climb Freq"] = auto_climbing_status_df[False] / (
                auto_climbing_status_df[True] + auto_climbing_status_df[False])
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(auto_climbing_status_df, x="Team Number", y=["Climb Freq", "No Climb Freq"],
                     title="Auto Climbing Frequency", color_discrete_sequence=custom_colors)
        return fig



#TELEOP GRAPHS
    @render_widget
    def teleop_fuel_in_hub():
        new_df = get_teams_in_match()
        avg_team = new_df.groupby("Team Number").mean(numeric_only=True)
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(avg_team, y="Teleop Fuel", title="Average Fuel in Hub (Teleop) per Robot",
                     color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def teleop_fuel_passed_total():
        new_df = get_teams_in_match()
        total_df = new_df.groupby("Team Number")["Teleop Fuel Passed"].sum().reset_index()
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(total_df, x="Team Number", y="Teleop Fuel Passed",
                     title="Total Teleop Fuel Passed",
                     color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def teleop_fuel_passed_avg():
        new_df = get_teams_in_match()
        avg_df = new_df.groupby("Team Number")["Teleop Fuel Passed"].mean().reset_index()
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(avg_df, x="Team Number", y="Teleop Fuel Passed",
                     title="Average Teleop Fuel Passed",
                     color_discrete_sequence=custom_colors)
        return fig



#ENDGAME GRAPHS
    @render_widget
    def endgame_positions_by_instance():
        new_df = get_teams_in_match()
        endgame_df = new_df.groupby("Team Number")["Endgame Climbing Level"].value_counts().unstack(
            fill_value=0).reset_index()
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(endgame_df, x="Team Number", y=["L1", "L2", "L3"],
                     title="Endgame Positions by Instance", color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def endgame_positions_by_points():
        new_df = get_teams_in_match()
        endgame_df = new_df.groupby("Team Number")["Endgame Climbing Level"].value_counts().unstack(
            fill_value=0).reset_index()
        endgame_df["L1 Points"] = endgame_df["L1"] * 10
        endgame_df["L2 Points"] = endgame_df["L2"] * 20
        endgame_df["L3 Points"] = endgame_df["L3"] * 30
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(endgame_df, x="Team Number", y=["L1 Points", "L2 Points", "L3 Points"],
                     title="Endgame Positions by Points", color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def total_climbing_points():
        new_df = get_teams_in_match().copy()
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(new_df, x="Team Number", y="Total Climb Points",
                     title="Auto + Endgame Climbing Points", color_discrete_sequence=custom_colors)
        return fig

    @render_widget
    def avg_climbing_points():
        new_df = get_teams_in_match().copy()
        avg_df = new_df.groupby("Team Number").mean(numeric_only=True).reset_index()
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(avg_df, x="Team Number", y="Total Climb Points",
                     title="Avg Auto + Endgame Climbing Points", color_discrete_sequence=custom_colors)
        return fig

# app = App(general_match_ui("match"), lambda input, output, session: general_match_server("match", input, output, session))
