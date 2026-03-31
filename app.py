from shiny import App, ui
import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shinywidgets import output_widget, render_widget
from data_container import load_pit_data, load_scouted_data

from overview_tab import overview_tab_server, overview_tab_ui
from general_match_things import general_match_server, general_match_ui
from team import pit_overview_tab_ui, pit_overview_tab_server

# Define custom CSS with navbar color
custom_css = """
<style>
body {
    background-color: #FFFFFF;
}

/* Change navbar background color */
.navbar {
    background-color: #f7041a !important;
}

/* Change navbar text color for better contrast (white text on red) */
.navbar-default .navbar-brand {
    color: #ffffff !important;
}

.navbar-default .navbar-nav > li > a {
    color: #ffffff !important;
}

/* Change navbar text hover color */
.navbar-default .navbar-nav > li > a:hover {
    color: #ffcccc !important;
}

/* Change active tab color */
.navbar-default .navbar-nav > .active > a,
.navbar-default .navbar-nav > .active > a:hover,
.navbar-default .navbar-nav > .active > a:focus {
    background-color: #d60316 !important;
    color: #ffffff !important;
}
</style>
"""

app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview_tab_ui("overview")),
    ui.nav_panel("Matches", general_match_ui("matches")),
    ui.nav_panel("Team", pit_overview_tab_ui("team")),
    title="2026FRCScoutingApp",
    header=ui.HTML(custom_css),
)


def server(input, output, session):
    pass
    overview_tab_server("overview")
    general_match_server("matches")
    pit_overview_tab_server("team")


app = App(app_ui, server)