import os
from shinywidgets import output_widget, render_widget
from shiny import module, ui
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match
import pandas as pd
import plotly.express as px
import numpy as np

pd.set_option('display.max_columns', None)

# from data_container import scouted_data
df = load_scouted_data()


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        ui.input_select(
            "y_axis_select",
            "Y Axis:",
            choices = ["Auto Fuel", "Teleop Fuel", "Endgame Fuel", "Total Fuel"]
        ),
        ui.input_radio_buttons(
            "selection_mode",
            "Select By:",
            choices=["Team Number", "Stat"],
            selected="Team Number",
        ),
        #ui.card(output_widget("auto_climbing_frequency")),
        ui.card(output_widget("teleop_vs_auto_endgame")),
    )


@module.server
def overview_tab_server(input, output, session):

    @render_widget
    def teleop_vs_auto_endgame():
        new_df = df.copy()

        numeric_cols = ["Auto Fuel", "Auto Human Player Score", "Teleop Fuel", "Teleop Human Player Score"]
        for col in numeric_cols:
            if col in new_df.columns:
                new_df[col] = pd.to_numeric(new_df[col], errors='coerce').fillna(0)

        new_df["Auto Climbing Status"] = new_df["Auto Climbing Status"].fillna(False)
        if new_df["Auto Climbing Status"].dtype == 'object':
            new_df["Auto Climbing Status"] = new_df["Auto Climbing Status"].astype(str).str.lower().isin(
                ['true', '1', 'yes'])

        team_stats = (new_df.groupby("Team Number").mean(numeric_only=True)).reset_index()

        y_axis = str(input.y_axis_select())

        if input.selection_mode() == "Team Number":
            sorted_df = team_stats.sort_values(by='Team Number', key=lambda x: x.astype(int))
        else:
            sorted_df = team_stats.sort_values(by=y_axis, ascending=False)

        fig = px.bar(
            sorted_df,
            x = sorted_df["Team Number"],
            y = y_axis,
            title=f"{y_axis} (Averages) by Team",
            color_discrete_sequence=["#BFAEDC"]
        )
        fig.update_traces(
            hovertemplate=(
                "<b>Team %{x}</b><br>"
                f"{y_axis}: %{{y:.1f}}<br>"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            xaxis_title="Team Number",
            yaxis_title= y_axis,
            hovermode="closest",
            showlegend=False
        )
        return fig