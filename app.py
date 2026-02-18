from shiny import App, ui
import pandas as pd
import numpy as np
import plotly.express as px
from shiny import reactive, render, module
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from data_container import load_pit_data, load_scouted_data


app_ui = ui.page_navbar(
    ui.nav_panel("A", "Page A content"),
    ui.nav_panel("B", "Page B content"),
    ui.nav_panel("C", "Page C content"),
    title="App with navbar",
)


def server(input, output, session):
    pass


app = App(app_ui, server)
