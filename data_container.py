import pathlib
import pandas as pd


script_directory = pathlib.Path(__file__).resolve().parent

EVENT_CODE = "mock_data"

def load_scouted_data():
    scouted_data = pd.read_csv(script_directory / f'data/{EVENT_CODE}/scouted_data.csv')

    return scouted_data


