import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match, load_match_numbers

df = load_scouted_data()
match_numbers = load_match_numbers()


@module.ui
def general_match_ui():
    return ui.page_fluid(
        ui.layout_sidebar(
            ui.sidebar(
                ui.output_ui("match_list_combobox"),
            ),
            ui.navset_tab(
                ui.nav_panel("Teleop",
                             ui.card(output_widget("teleop_fuel_in_hub")),
                             ui.card(output_widget("teleop_fuel_passed_total")),
                             ui.card(output_widget("teleop_fuel_passed_avg")),

                             ),
            ),
            ui.navset_tab(
                ui.nav_panel("Endgame",
                             ui.card(output_widget("avg_climb_endgame")),)
            )
        )
    )


@module.server
def general_match_server(input, output, session):
    def get_teams_in_match():
        match_number = str(input.match_select())
        return df.loc[df["Team Number"].isin(get_Teams_in_Match(match_number))]

    @render.ui
    def match_list_combobox():
        return ui.input_select(
            "match_select",
            "Match Number:",
            choices=match_numbers
        )

    @render_widget
    def teleop_fuel_in_hub():
        new_df = get_teams_in_match()
        avg_team = new_df.groupby("Team Number").mean(numeric_only=True)
        custom_colors = ["#194f55", "#54808e", "#243454"]
        fig = px.bar(avg_team, y="Teleop Fuel", title="Fuel in Hub (Teleop) per Robot",
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

    @render_widget
    def avg_climb_endgame():
        teams = get_Teams_in_Match()
        match_data = df.loc[df["Team Number"].isin(teams)].reset_index()

        def convert_endgame_to_teleop(level):
            if pd.isna(level):
                return 0
            level_str = str(level).upper().strip()
            if level_str == "L1":
                return 10
            elif level_str == "L2":
                return 20
            elif level_str == "L3":
                return 30
            else:
                return 0

        match_data["Endgame Points"] = match_data["Endgame Climbing Level"].apply(convert_endgame_to_teleop)
        fig = px.bar(x="Team Number", y="Endgame Points", title="Average Endgame Climb Points per Team")
        return fig

#app = App(general_match_ui("match"), lambda input, output, session: general_match_server("match", input, output, session))
