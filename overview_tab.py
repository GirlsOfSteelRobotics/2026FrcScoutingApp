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

        def convert_endgame_to_points(level):
            if pd.isna(level):
                return 0
            level_str = str(level).upper().strip()
            return {"L1": 10, "L2": 20, "L3": 30}.get(level_str, 0)

        new_df["Endgame Teleop Points"] = new_df["Endgame Climbing Level"].apply(convert_endgame_to_points)
        new_df["Auto Climb Points"] = new_df["Auto Climbing Status"].apply(lambda x: 15 if x else 0)
        new_df["All Auto"] = new_df["Auto Fuel"] + new_df["Auto Climb Points"]
        new_df["All Teleop"] = new_df["Teleop Fuel"] + new_df["Endgame Teleop Points"]
        new_df["All Endgame"] = new_df["Endgame Teleop Points"]
        new_df["Auto and Endgame"] = new_df["All Auto"] + new_df["All Endgame"]
        new_df["Total Fuel"] = new_df["Auto Fuel"] + new_df["Teleop Fuel"]
        new_df["Endgame Fuel"] = new_df["Endgame Teleop Points"]

        team_stats = new_df.groupby("Team Number").agg({
            "All Teleop": "mean",
            "Auto and Endgame": "mean",
            "All Auto": "mean",
            "All Endgame": "mean",
            "Endgame Teleop Points": "mean",
            "Auto Climb Points": "mean",
            "Auto Climbing Status": "mean",
            "Auto Fuel": "mean",
            "Teleop Fuel": "mean",
            "Endgame Fuel": "mean",
            "Total Fuel": "mean",
        }).reset_index()

        y_axis = str(input.y_axis_select())

        fig = px.scatter(
            team_stats,
            x = "All Teleop",
            y = y_axis,
            title=f"Teleop vs. {y_axis} (Team Averages)",
        )
        fig.update_traces(
            hovertemplate=(
                "<b>Team %{customdata[0]}</b><br>"
                "All Teleop: %{x:.1f}<br>"
                f"{y_axis}: %{{y:.1f}}<br>"
                "<extra></extra>"
            ),
            customdata=team_stats[["Team Number"]].values
        )
        fig.update_layout(
            xaxis_title="Average Teleop Score",
            yaxis_title= y_axis,
            hovermode="closest",
            showlegend=False
        )
        return fig

    @render_widget
    def statbotics_prediction(input, output, session):
        return