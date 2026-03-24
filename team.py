import pandas as pd
from shiny import module, ui, render
from shinywidgets import output_widget, render_widget
import plotly.express as pxgit pu
from data_container import load_pit_data, load_scouted_data

pd.set_option("display.max_columns", None)

pit_df = load_pit_data().copy()
match_df = load_scouted_data().copy()


@module.ui
def pit_overview_tab_ui():
    teams = sorted(
        [x for x in pit_df["Team Number"].unique().tolist() if x is not None and str(x) != '<NA>'],
        key=lambda x: int(x)
    )
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
            ui.card(
                ui.card_header("Go Under Trench?"),
                ui.output_text("under_trench"),
            ),
            ui.card(
                ui.card_header("Go Over Bump?"),
                ui.output_text("over_bump"),
            ),
            ui.card(
                ui.card_header("Climbing Type (In/Out)"),
                ui.output_text("climb_type"),
            ),
            ui.card(
                ui.card_header("Preload Number"),
                ui.output_text("preload_number"),
            ),
            ui.card(
                ui.card_header("Mechanical Quality"),
                ui.output_text("mechanical_quality"),
            ),
            ui.card(
                ui.card_header("Electrical Wiring Quality"),
                ui.output_text("elec_wiring_quality"),
            ),
            ui.card(
                ui.card_header("Drivetrain Quality"),
                ui.output_text("drivetrain_quality"),
            ),
            ui.card(
                ui.card_header("Programming Language"),
                ui.output_text("program_language"),
            ),
            ui.card(
                ui.card_header("Carrying Capacity"),
                ui.output_text("carrying_capacity"),
            ),
            ui.card(
                ui.card_header("__-Piece Auto"),
                ui.output_text("piece_auto"),
            ),
            ui.card(
                ui.card_header("Auto Start Position"),
                ui.output_text("auto_start"),
            ),
            ui.card(
                ui.card_header("Defensive Skill (0-5)"),
                ui.output_text("defensive_skill"),
            ),
            col_widths=[6, 6],
        ),
        ui.input_select(
            "y_axis_select",
            "Metric:",
            choices=["Endgame Scored Points", "Total Fuel", "Average Fuel", "Auto Fuel", "Teleop Fuel"],
            selected="Total Fuel",
        ),
        ui.card(output_widget("team_trend_graph")),
    )


#Pit Scouting Cards
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

    @render.text
    def under_trench():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        trench = row.get("Under Trench?", "N/A")
        if trench == 0:
            return False
        elif trench == 1:
            return True
        else:
            return "N/A"


    @render.text
    def over_bump():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        bump = row.get("Over Bump?", "N/A")
        if bump == 0:
            return False
        elif bump == 1:
            return True
        else:
            return "N/A"

    @render.text
    def climb_type():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        type = row.get ("Climb type", "N/A")
        return type

    @render.text
    def preload_number():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        preload = row.get ("Preload Number", "")
        preload = "" if pd.isna(preload) else str(preload).strip()
        return preload if preload else "N/A"

    @render.text
    def carrying_capacity():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        capacity = row.get ("Carrying Capacity", "")
        capacity = "" if pd.isna(capacity) else str(capacity).strip()
        return capacity if capacity else "N/A"

    @render.text
    def piece_auto():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        piece = row.get ("Piece Auto", "")
        piece = "" if pd.isna(piece) else str(piece).strip()
        return piece if piece else "N/A"

    @render.text
    def auto_start():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        positions = []
        for col, label in [("StartHumanPlayer", "Human Player"), ("StartCenter", "Center"), ("StartDepot", "Depot")]:
            val = row.get(col, 0)
            try:
                if int(float(str(val))) == 1:
                    positions.append(label)
            except:
                pass
        return ", ".join(positions) if positions else "None specified"

    @render.text
    def defensive_skill():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        defense = row.get ("Defense Skill (0-5)", "")
        defense = "" if pd.isna(defense) else str(defense).strip()
        return defense if defense else "N/A"

    @render.text
    def program_language():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        program_language = row.get("Programming Language", "")
        program_language = "" if pd.isna(program_language) else str(program_language).strip()
        return program_language if program_language else "N/A"

    @render.text
    def drivetrain_quality():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        drivetrain_quality = row.get("Drivetrain Quality", "")
        drivetrain_quality = "" if pd.isna(drivetrain_quality) else str(drivetrain_quality).strip()
        return drivetrain_quality



    @render.text
    def elec_wiring_quality():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        elec_wiring_quality = row.get("Electrical Wiring Quality", "")
        elec_wiring_quality = "" if pd.isna(elec_wiring_quality) else str(elec_wiring_quality).strip()
        return elec_wiring_quality if elec_wiring_quality else "N/A"

    @render.text
    def mechanical_quality():
        team = input.team_select()
        row = get_team_row(team)
        if row is None:
            return "N/A"
        mech_quality = row.get ("Mechanical Quality", "")
        mech_quality = "" if pd.isna(mech_quality) else str(mech_quality).strip()
        return mech_quality if mech_quality else "N/A"

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

        team_df["Auto Fuel"] = pd.to_numeric(team_df["Auto Fuel"], errors="coerce").fillna(0)
        team_df["Teleop Fuel"] = pd.to_numeric(team_df["Teleop Fuel"], errors="coerce").fillna(0)

        def convert_endgame(level):
            if pd.isna(level):
                return 0
            return {"L1": 10, "L2": 20, "L3": 30}.get(str(level).upper().strip(), 0)

        team_df["Endgame Scored Points"] = team_df["Endgame Climbing Level"].apply(convert_endgame)
        team_df["Total Fuel"] = team_df["Auto Fuel"] + team_df["Teleop Fuel"]
        team_df["Average Fuel"] = team_df["Total Fuel"].expanding().mean()

        fig = px.scatter(team_df, x="Match Number", y=y_axis,
                         title=f"Team {team}: {y_axis} by Match", color_discrete_sequence=["#BFAEDC"])
        fig.update_traces(mode="markers+lines")
        fig.update_layout(xaxis_title="Match", yaxis_title=y_axis, showlegend=False)
        return fig