import os

from shinywidgets import output_widget, render_widget
from shiny import module, ui
from data_container import load_scouted_data, load_pit_data, get_Teams_in_Match
import pandas as pd
import plotly.express as px

from general_match_things import df

pd.set_option('display.max_columns', None)

# from data_container import scouted_data
scouted_data = load_scouted_data()


@module.ui
def overview_tab_ui():
    return ui.page_fluid(
        output_widget("teleop_v_autoend")
    )


@module.server
def overview_tab_server(input, output, server):


    @render_widget
    def teleop_v_autoend():
            teams = get_Teams_in_Match()
            match_data = df.loc[scouted_data["Team Number"].isin(teams)].reset_index()
            numeric_cols = ["Auto Fuel", "Teleop Fuel"]
            for col in numeric_cols:
                if col in match_data.columns:
                    match_data[col] = pd.to_numeric(match_data[col], errors='coerce').fillna(0)
                    match_data["Auto Climbing Status"] = match_data["Auto Climbing Status"].fillna(False)
                if match_data["Auto Climbing Status"].dtype == 'object':
                    match_data["Auto Climbing Status"] = match_data["Auto Climbing Status"].astype(str).str.lower().isin(
                    ['true', '1', 'yes'])
            def convert_endgame_to_teleop(level):
                if pd.isna(level):
                    return 0
                level_str = str(level).upper().strip()
                if level_str == "L1":
                    return 10
                elif level_str == "L2":
                    return 20
                elif level_str == "L3":
                    return 30
                else:
                    return 0


            match_data["Endgame Teleop Points"] = match_data["Endgame Climbing Level"].apply(convert_endgame_to_teleop)
            match_data["Auto Climb Points"] = match_data["Auto Climbing Status"].apply(lambda x: 15 if x else 0)
            match_data["All Auto"] = match_data["Auto Fuel"] + match_data["Auto Climb Points"]
            match_data["All Teleop"] = match_data["Teleop Fuel"] + match_data["Endgame Teleop Points"]
            match_data["All Endgame"] = match_data["Endgame Teleop Points"]
            match_data["Auto and Endgame"] = match_data["All Auto"] + match_data["All Endgame"]

            team_stats = match_data.groupby("Team Number").agg({
                "All Teleop": "mean",
                "Auto and Endgame": "mean",
                "All Auto": "mean",
                "All Endgame": "mean",
                "Endgame Teleop Points": "mean",
                "Auto Climb Points": "mean",
                "Auto Climbing Status": "mean",
            }).reset_index()
            fig = px.scatter(
                team_stats,
                x="All Teleop",
                y="Auto and Endgame",
                title="Teleop vs. Auto + Endgame",
                hover_data={
                "Team Number": True,
                "All Teleop": ":.1f",
                "Auto and Endgame": ":.1f",
                "All Auto": ":.1f",
                "All Endgame": ":.1f",
                "Endgame Teleop Points": ":.1f",
                "Auto Climb Points": ":.1f",
                "Auto Climbing Status": ":.2%",
                }
            )
            fig.update_traces(
                hovertemplate=(
                    "<b>Team %{customdata[0]}</b><br>"
                    "All Teleop: %{x:.1f}<br>"
                    "Auto and Endgame: %{y:.1f}<br>"
                    "All Auto: %{customdata[1]:.1f}<br>"
                    "All Endgame: %{customdata[2]:.1f}<br>"
                    "Endgame Teleop Points: %{customdata[3]:.1f}<br>"
                    "Auto Climb Points: %{customdata[4]:.1f}<br>"
                    "Auto Climbing Status: %{customdata[5]:.2%}<extra></extra>"
                ),
            customdata=team_stats[["Team Number", "All Auto", "All Endgame",
                       "Endgame Teleop Points", "Auto Climb Points",
                       "Auto Climbing Status"]].values
            )

            fig.update_layout(
                xaxis_title="Average Teleop Score",
                yaxis_title="Average (Auto + Endgame) Score",
                hovermode="closest",
                showlegend=False
            )
            return fig

   # @render_widget
    # def auto_climbing_frequency():
       # auto_climbing_status_df = scouted_data.groupby("Team Number")["Auto Climbing Status"].value_counts().unstack(
        #    fill_value=0).reset_index()
       # auto_climbing_status_df["Climb Freq"] = auto_climbing_status_df[True] / (
        #            auto_climbing_status_df[True] + auto_climbing_status_df[False])
       # auto_climbing_status_df["No Climb Freq"] = auto_climbing_status_df[False] / (
        #            auto_climbing_status_df[True] + auto_climbing_status_df[False])
       # fig = px.bar(auto_climbing_status_df, x="Team Number", y=["Climb Freq", "No Climb Freq"],
                     #title="Auto Climbing Frequency")
       # return fig

  #  @render_widget
  #  def six_teams_average_auto_fuel():
      #  get_Teams_in_Match()
     #   teams = get_Teams_in_Match()
     #   match_data = scouted_data.loc[scouted_data["Team Number"].isin(teams)]
     #   avg_6_teams = match_data.groupby("Team Number").mean(numeric_only=True)
   #     fig = px.bar(avg_6_teams, y="Auto Fuel", title="Fuel in Hub (Auto) per Robot")
     #   return fig

 #   @render_widget
   # def six_teams_average_teleop_fuel():
    #    get_Teams_in_Match()
      #  teams = get_Teams_in_Match()
      #  match_data = scouted_data.loc[scouted_data["Team Number"].isin(teams)]
      #  avg_6_teams = match_data.groupby("Team Number").mean(numeric_only=True)
      #  fig = px.bar(avg_6_teams, y="Teleop Fuel", title="Fuel in Hub (Teleop) per Robot")
      #  return fig


