import pandas as pd
from shiny import module, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as px
from data_container import load_pit_data, load_scouted_data

pd.set_option("display.max_columns", None)

pit_df = load_pit_data().copy()
pit_df["Team Number"] = (
    pd.to_numeric(pit_df["Team Number"], errors="coerce")
    .dropna()
    .astype(int)
    .astype(str)
)

match_df = load_scouted_data().copy()
match_df["Team Number"] = (
    pd.to_numeric(match_df["Team Number"], errors="coerce")
    .dropna()
    .astype(int)
    .astype(str)
)


@module.ui
def pit_overview_tab_ui():
    teams = sorted(pit_df["Team Number"].unique().tolist(), key=lambda x: int(x))

    return ui.page_fluid(
        ui.input_select(
            "team_select",
            "Select Team:",
            choices=teams,
            selected=teams[0] if teams else None,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Intake"),
                ui.output_text("intake_value"),
            ),
            ui.card(
                ui.card_header("Climbing Levels"),
                ui.output_text("climb_value"),
            ),
            col_widths=[6, 6],
        ),
        ui.input_select(
            "y_axis_select",
            "Metric:",
            choices=["Endgame scored points", "Total fuel", "Average fuel"],
            selected="Total fuel",
        ),
        ui.card(output_widget("team_trend_graph")),
    )


@module.server
def pit_overview_tab_server(input, output, session):

    def get_team_row(team_str: str):
        rows = pit_df[pit_df["Team Number"] == str(team_str)]
        return None if rows.empty else rows.iloc[0]

    @render.text
    def intake_value():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        val = row.get("Intake", "")
        val = "" if pd.isna(val) else str(val).strip()
        return val if val else "N/A"

    @render.text
    def climb_value():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        auto = row.get("Climbing Level (Auto)", None)
        endg = row.get("Climbing Level (Endgame)", None)
        auto = "N/A" if pd.isna(auto) else str(auto).strip()
        endg = "N/A" if pd.isna(endg) else str(endg).strip()
        return f"Auto: {auto} | Endgame: {endg}"

    @render_widget
    def team_trend_graph():
        team = str(input.team_select())
        y_axis = str(input.y_axis_select())

        team_df = match_df[match_df["Team Number"] == team].copy()

        if team_df.empty:
            fig = px.scatter(title=f"No match data for Team {team}")
            return fig

        team_df["Match Number"] = pd.to_numeric(team_df["Match Number"], errors="coerce")
        team_df = team_df.dropna(subset=["Match Number"]).sort_values("Match Number")

        team_df["Auto Fuel"] = pd.to_numeric(team_df.get("Auto Fuel", 0), errors="coerce").fillna(0)
        team_df["Teleop Fuel"] = pd.to_numeric(team_df.get("Teleop Fuel", 0), errors="coerce").fillna(0)

        def convert_endgame(level):
            if pd.isna(level):
                return 0
            s = str(level).upper().strip()
            return {"L1": 10, "L2": 20, "L3": 30}.get(s, 0)

        team_df["Endgame scored points"] = team_df["Endgame Climbing Level"].apply(convert_endgame)
        team_df["Total fuel"] = team_df["Auto Fuel"] + team_df["Teleop Fuel"]
        team_df["Average fuel"] = team_df["Total fuel"].expanding().mean()

        fig = px.scatter(team_df, x="Match Number", y=y_axis,
                         title=f"Team {team}: {y_axis} by Match")
        fig.update_traces(mode="markers+lines")
        fig.update_layout(xaxis_title="Match", yaxis_title=y_axis, showlegend=False)
        return fig