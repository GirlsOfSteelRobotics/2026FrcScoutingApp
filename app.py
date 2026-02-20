from shiny import App, ui

from overview_tab import overview_tab_server, overview_tab_ui

app_ui = ui.page_navbar(
    ui.nav_panel("Overview", overview_tab_ui("overview")),
    # ui.nav_panel("Matches", "matches"),
    title="2026FRCScoutingApp",
)


def server(input, output, session):
    pass
    overview_tab_server("overview")
    # general_match_server("matches")


app = App(app_ui, server)
