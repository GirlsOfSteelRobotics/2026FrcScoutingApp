from shiny import App, ui
import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_pit_data, load_scouted_data

from overview_tab import overview_tab_server, overview_tab_ui
from general_match_things import general_match_server, general_match_ui
from team import pit_overview_tab_ui, pit_overview_tab_server
app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview_tab_ui("overview")),
    ui.nav_panel("Matches", general_match_ui("matches")),
    ui.nav_panel("Team", pit_overview_tab_ui("team")),
    title="2026FRCScoutingApp",
)


def server(input, output, session):
    pass
    overview_tab_server("overview")
    general_match_server("matches")
    pit_overview_tab_server("team")



app = App(app_ui, server)
