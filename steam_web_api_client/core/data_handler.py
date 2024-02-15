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
        self.username_list = []
        self.id_list = []
        self.user_data = []

    def read_data(self) -> str:
        """Reads api_key and steam_id from data.json.

        Returns:
            str: value of api_key
        """
        try:
            with open(file=self.data_path, mode="r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
                self.api_key = loaded_data["api_key"]
                self.user_data = loaded_data["user_data"]
                self.id_list = [entry["steam_id"] for entry in self.user_data]
                self.username_list = [entry["username"] for entry in self.user_data]
            print(f"Loaded data from {self.data_path}")
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.api_key = ""
            print(f"Couldn't read data from {self.data_path}")
            directory = os.path.dirname(self.data_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file=self.data_path, mode="w", encoding="utf-8"):
                print(f"Created {self.data_path}")
        return self.api_key

    def save_data(self) -> None:
        """Writes api_key and steam_id to data.json."""
        user_data_list = [
            {"steam_id": steam_id, "username": username}
            for steam_id, username in zip(self.id_list, self.username_list)
        ]
        input_data = {
            "api_key": self.api_key,
            "user_data": user_data_list,
        }
        with open(file=self.data_path, mode="w", encoding="utf-8") as json_file:
            json.dump(input_data, json_file)
            print(f"Saved data to {self.data_path}")

    def get_username_by_id(self, steam_id: str) -> str:
        """Get the username associated with the given steam_id.

        Args:
            steam_id (str): The steam_id to look up.

        Returns:
            str: The corresponding username, or an empty string if not found.
        """
        for entry in self.user_data:
            if entry["steam_id"] == steam_id:
                return entry["username"]
        return ""
