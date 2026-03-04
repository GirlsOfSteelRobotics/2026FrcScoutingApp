import os
from shinywidgets import output_widget, render_widget
from shiny import module, ui
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match
import pandas as pd
import plotly.express as px
import numpy as np

pd.set_option('display.max_columns', None)

df = load_scouted_data()
match_numbers = load_match_numbers()
all_teams = sorted(df["Team Number"].unique().tolist())


@module.ui
ui.page_navbar(
    "Pit Data",
    ui.card(
        ui

)





