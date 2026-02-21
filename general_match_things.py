import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_scouted_data, load_pit_data

df = load_scouted_data()

match_schedule = df.groupby("Match Number")["Team Number"].apply(list).to_dict()

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
            )
        )
    )

@module.server
def general_match_server(input, output, session):

    def get_teams_in_match():
        match_name = str(input.match_select())
        all_teams = match_schedule[match_name]
        new_df = df.loc[df["Team Number"].isin(all_teams)]
        #print(f"Match: {match_name}, Teams: {all_teams}, Rows returned: {len(new_df)}")
        return new_df

    @render.ui
    def match_list_combobox():
        match_numbers = list(match_schedule.keys())
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


#app = App(general_match_ui("match"), lambda input, output, session: general_match_server("match", input, output, session))