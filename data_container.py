import pathlib
import pandas as pd


script_directory = pathlib.Path(__file__).resolve().parent

EVENT_CODE = "mock_data"

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/scouted_data.csv')
    scouted_data[['Team Number', 'Match Number']] = scouted_data[['Team Number', 'Match Number']].astype("string")

    return scouted_data

def load_pit_data():
    pit_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/pit_data.csv')
    pit_data['Team Number'] = pit_data['Team Number'].astype("string")

    return pit_data

def get_Teams_in_Match():
    Teams_in_Match = ["9668", "7072", "4504", "1708", "4467", "3504"]

    return (Teams_in_Match)
