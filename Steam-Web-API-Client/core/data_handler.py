import json


class DataHandler:
    def __init__(self, data_path, api_key, steam_id):
        self.data_path = data_path
        self.api_key = api_key
        self.steam_id = steam_id

    def read_data(self):
        # Read data.json if possible
        try:
            with open(self.data_path, "r") as json_file:
                loaded_data = json.load(json_file)
                self.api_key = loaded_data["api_key"]
                self.steam_id = loaded_data["steam_id"]
            print(f"Loaded data from {self.data_path}.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.api_key = ""
            self.steam_id = ""
            print(f"Couldn't read data from {self.data_path}.")
        return self.api_key, self.steam_id

    def write_data(self):
        self.input_data = {"api_key": "", "steam_id": ""}
        self.input_data["api_key"] = self.api_key
        self.input_data["steam_id"] = self.steam_id
        with open(self.data_path, "w") as json_file:
            json.dump(self.input_data, json_file)
