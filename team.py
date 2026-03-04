import os
from shinywidgets import output_widget, render_widget
from shiny import module, ui
from data_container import load_pit_data
import pandas as pd
import plotly.express as px

pd.set_option("display.max_columns", None)

pit_df = load_pit_data()


@module.ui
def pit_overview_tab_ui():
    return ui.page_fluid(
        ui.layout_columns(
            ui.card(output_widget("intake_card")),
            ui.card(output_widget("climb_levels_card")),
            col_widths=[6, 6],
        )
    )


@module.server
def pit_overview_tab_server(input, output, session):

    @render_widget
    def intake_card():
        # counts of intake values
        counts = (
            pit_df["Intake"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .reset_index()
        )
        counts.columns = ["Intake", "Teams"]

        fig = px.bar(counts, x="Intake", y="Teams", title="Intake")
        fig.update_layout(showlegend=False)
        return fig

    @render_widget
    def climb_levels_card():
        # counts of climb levels (auto + endgame) shown side-by-side
        auto_counts = (
            pit_df["Climbing Level (Auto)"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )
        auto_counts.columns = ["Level", "Teams"]
        auto_counts["Phase"] = "Auto"

        end_counts = (
            pit_df["Climbing Level (Endgame)"]
            .dropna()
            .value_counts()
            .sort_index()
            .reset_index()
        )
        end_counts.columns = ["Level", "Teams"]
        end_counts["Phase"] = "Endgame"

        plot_df = pd.concat([auto_counts, end_counts], ignore_index=True)

        fig = px.bar(
            plot_df,
            x="Level",
            y="Teams",
            color="Phase",
            barmode="group",
            title="Climbing Levels",
        )
        return fig

