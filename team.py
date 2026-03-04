import pandas as pd
from shiny import module, ui, render
from data_container import load_pit_data

pd.set_option("display.max_columns", None)

pit_df = load_pit_data().copy()

# Normalize Team Number to string so filtering ALWAYS matches dropdown values
pit_df["Team Number"] = (
    pd.to_numeric(pit_df["Team Number"], errors="coerce")
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