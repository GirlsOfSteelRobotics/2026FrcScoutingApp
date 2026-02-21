import os

from shinywidgets import output_widget, render_widget
from shiny import module, ui
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match
import pandas as pd
import plotly.express as px

pd.set_option('display.max_columns', None)

# from data_container import scouted_data
scouted_data = load_scouted_data()


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        output_widget("auto_climbing_frequency"), output_widget("six_teams_average_auto_fuel"), output_widget("six_teams_average_teleop_fuel"),
    )


@module.server
def overview_tab_server(input, output, server):
    def get_Teams_in_Match():
        Teams_in_Match = ["118", "67", "8393", "3504", "254", "1678"]

        return (Teams_in_Match)

    @render_widget
    def auto_climbing_frequency():
        auto_climbing_status_df = scouted_data.groupby("Team Number")["Auto Climbing Status"].value_counts().unstack(
            fill_value=0).reset_index()
        auto_climbing_status_df["Climb Freq"] = auto_climbing_status_df[True] / (
                    auto_climbing_status_df[True] + auto_climbing_status_df[False])
        auto_climbing_status_df["No Climb Freq"] = auto_climbing_status_df[False] / (
                    auto_climbing_status_df[True] + auto_climbing_status_df[False])
        fig = px.bar(auto_climbing_status_df, x="Team Number", y=["Climb Freq", "No Climb Freq"],
                     title="Auto Climbing Frequency")
        return fig

    @render_widget
    def six_teams_average_auto_fuel():
        get_Teams_in_Match()
        teams = get_Teams_in_Match()
        match_data = scouted_data.loc[scouted_data["Team Number"].isin(teams)]
        avg_6_teams = match_data.groupby("Team Number").mean(numeric_only=True)
        fig = px.bar(avg_6_teams, y="Auto Fuel", title="Fuel in Hub (Auto) per Robot")
        return fig

    @render_widget
    def six_teams_average_teleop_fuel():
        get_Teams_in_Match()
        teams = get_Teams_in_Match()
        match_data = scouted_data.loc[scouted_data["Team Number"].isin(teams)]
        avg_6_teams = match_data.groupby("Team Number").mean(numeric_only=True)
        fig = px.bar(avg_6_teams, y="Teleop Fuel", title="Fuel in Hub (Teleop) per Robot")
        return fig


