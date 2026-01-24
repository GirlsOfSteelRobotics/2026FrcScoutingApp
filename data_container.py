import pathlib
import pandas as pd


script_directory = pathlib.Path(__file__).resolve().parent

EVENT_CODE = "mock_data"

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/scouted_data.csv')
    scouted_data[['Team Number', 'Match Number']] = scouted_data[['Team Number', 'Match Number']].astype("string")

    return scouted_data

def get_Teams_in_Match():
    Teams_in_Match = ["118", "67", "8393", "3504", "254", "1678"]

    return (Teams_in_Match)


