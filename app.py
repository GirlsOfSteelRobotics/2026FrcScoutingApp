from shiny import App, ui

from overview_tab import overview_tab_server, overview_tab_ui
from general_match_things import general_match_server, general_match_ui
app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview_tab_ui("overview")),
    ui.nav_panel("Matches", general_match_ui("matches")),
    title="2026FRCScoutingApp",
)


def server(input, output, session):
    pass
    overview_tab_server("overview")
    general_match_server("matches")


app = App(app_ui, server)
