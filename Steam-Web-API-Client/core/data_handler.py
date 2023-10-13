"""File Handling for saving input values between executions."""

import json


class DataHandler:
    """Reading and writing to json file

    Attributes:
        data_path: A string containing the path of a json file
        api_key: A string holding the value of the steam api key
        steam_id: A string holding the value of the steam_id of an user
        input_data: A dictionary declaring the structure of the json file
    """

    def __init__(self, data_path: str, api_key: str, steam_id: str):
        self.data_path = data_path
        self.api_key = api_key
        self.steam_id = steam_id
        self.input_data = {"api_key": "", "steam_id": ""}

    def read_data(self) -> list:
        """Reads api_key and steam_id from data.json

        Returns:
            list: value of api_key and steam_id
        """
        try:
            with open(file=self.data_path, mode="r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
                self.api_key = loaded_data["api_key"]
                self.steam_id = loaded_data["steam_id"]
            print(f"Loaded data from {self.data_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.api_key = ""
            self.steam_id = ""
            print(f"Couldn't read data from {self.data_path}")
        return [self.api_key, self.steam_id]

    def write_data(self) -> None:
        """Writes api_key and steam_id to data.json"""
        self.input_data["api_key"] = self.api_key
        self.input_data["steam_id"] = self.steam_id
        with open(file=self.data_path, mode="w", encoding="utf-8") as json_file:
            json.dump(self.input_data, json_file)
