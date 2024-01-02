"""File Handling for saving input values between executions."""

import json
import os


class DataHandler:
    """Read and write to json file.

    Attributes:
        data_path: A string containing the path of a json file
        api_key: A string holding the value of the steam api key
        steam_id: A string holding the value of the steam_id of an user
        input_data: A dictionary declaring the structure of the json file
    """

    def __init__(self, data_path: str, api_key: str = ""):
        self.data_path = data_path
        self.api_key = api_key
        self.id_list = []

    def read_data(self) -> str:
        """Reads api_key and steam_id from data.json.

        Returns:
            str: value of api_key
        """
        try:
            with open(file=self.data_path, mode="r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
                self.api_key = loaded_data["api_key"]
                self.id_list = list(loaded_data["steam_ids"])
            print(f"Loaded data from {self.data_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.api_key = ""
            self.id_list = []
            print(f"Couldn't read data from {self.data_path}")
            directory = os.path.dirname(self.data_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file=self.data_path, mode="w", encoding="utf-8"):
                print(f"Created {self.data_path}")
        return self.api_key

    def save_data(self) -> None:
        """Writes api_key and steam_id to data.json."""
        input_data = {"api_key": "", "steam_ids": self.id_list}
        input_data["api_key"] = self.api_key
        with open(file=self.data_path, mode="w", encoding="utf-8") as json_file:
            json.dump(input_data, json_file)
            print(f"Saved data to {self.data_path}")
