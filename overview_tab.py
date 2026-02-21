import os

from shinywidgets import output_widget, render_widget
from shiny import module, ui
# Hacky way to get to root package
if "notebooks" in os.getcwd():
    os.chdir("..")

from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match
import pandas as pd
import plotly.express as px

pd.set_option('display.max_columns', None)

# from data_container import scouted_data
scouted_data = load_scouted_data()


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        output_widget("auto_climbing_frequency"),
    )


@module.server
def overview_tab_server(input, output, server):

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