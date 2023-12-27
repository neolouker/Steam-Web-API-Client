"""Fetch and save information from Steam Web API"""
import urllib.request
import urllib.error
import io
import datetime
import requests
from steam.webapi import WebAPI
from PIL import ImageTk, Image


class SteamAPI:
    """Save, process and return information from Steam Web API

    Attributes:
        api_key = A string holding the value of the steam api key
        api = An object using the api_key to access the API
        image_list = A list holding icons returned from the API
        name_list = A list holding game titles returned from the API
        playtime_2weeks_list = A list holding playtime in last 2 weeks values returned from the API
        playtime_forever_list = A list holding overall playtime values returned from the API
    """

    def __init__(self, api_key: str):
        self.api = WebAPI(key=api_key)
        self.avatar_list = []
        self.image_list = []
        self.name_list = []
        self.playtime_2weeks_list = []
        self.playtime_forever_list = []

    def get_recently_played_games(self, steamid: int) -> dict:
        """Fetch and return recently played games from API

        Args:
            steamid (int): steam ID of user to fetch information

        Returns:
            dict: data containing the fetched information
        """
        try:
            response = self.api.call(
                "IPlayerService.GetRecentlyPlayedGames", steamid=steamid, count=50, format="json")
            return response

        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            print(f"HTTPError: {http_err}")
            print("No access to this data! This profile is private!")
            return None

    def get_player_summaries(self, steamid: int) -> dict:
        """Fetch and return summary of an user from API

        Args:
            steamid (int): steam ID of user to fetch information

        Returns:
            dict: data containing the fetched information
        """
        try:
            response = self.api.call(
                "ISteamUser.GetPlayerSummaries", steamids=steamid, format="json")
            return response

        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            print(f"HTTPError: {http_err}")
            print("No access to this data! This profile is private!")
            return None

    def fetch_avatar(self, summaries: dict) -> None:
        """Filter and process the avatar of an user

        Args:
            summaries (dict): data containing the fetched information about user

        Returns:
            ImageTk.PhotoImage: processed image of user avatar
        """
        avatar_url = summaries["response"]["players"][0]["avatar"]
        try:
            with urllib.request.urlopen(avatar_url, timeout=10) as image_data:
                image_file = io.BytesIO(image_data.read())
            img = ImageTk.PhotoImage(Image.open(image_file))
            self.avatar_list.append(img)
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print("Error fetching avatar:", e)
            self.avatar_list.append(None)

    def fetch_username(self, summaries: dict) -> str:
        """Filter and return username of user

        Args:
            summaries (dict): data containing the fetched information about user

        Returns:
            str: username
        """
        return summaries["response"]["players"][0]["personaname"]

    def fetch_user_status(self, summaries: dict) -> str:
        """Filter, process and return status of user

        Args:
            summaries (dict): data containing the fetched information about user

        Returns:
            str: status of user
        """
        state = summaries["response"]["players"][0]["personastate"]
        match state:
            case 0:
                return "Offline"
            case 1:
                return "Online"
            case 2:
                return "Busy"
            case 3:
                return "AFK"
            case 4:
                return "Snooze"
            case _:
                return ""

    def fetch_last_logoff(self, summaries: dict) -> str:
        """Filter, process and return the time the user last logged off

        Args:
            summaries (dict): data containing the fetched information about user

        Returns:
            str: time the user last logged off
        """
        last_logoff = summaries["response"]["players"][0]["lastlogoff"]
        time = datetime.datetime.fromtimestamp(last_logoff)
        time_formatted = time.strftime("%d.%m.%Y %H:%M")
        return time_formatted

    def fetch_icons(self, games: dict, iteration: int) -> None:
        """Fetch, process and save the game icons

        Args:
            games (dict): data containing the fetched information about games
            iteration (int): current iteration in loop over amount of games
        """
        app_id = games["response"]["games"][iteration]["appid"]
        icon_hash = games["response"]["games"][iteration]["img_icon_url"]
        icon_url = (f"http://media.steampowered.com/steamcommunity/"
                    f"public/images/apps/{app_id}/{icon_hash}.jpg")
        try:
            with urllib.request.urlopen(icon_url, timeout=10) as image_data:
                image_file = io.BytesIO(image_data.read())
            # Create and store ImageTk objects in the list
            img = ImageTk.PhotoImage(Image.open(image_file))
            self.image_list.append(img)
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print("Error fetching icon:", e)
            # Append a placeholder or handle the error accordingly
            self.image_list.append(None)

    def fetch_names(self, games: dict, iteration: int):
        """Fetch and save game titles

        Args:
            games (dict): data containing the fetched information about games
            iteration (int): current iteration in loop over amount of games
        """
        game_name = games["response"]["games"][iteration]["name"]
        self.name_list.append(game_name)

    def fetch_playtime_2weeks(self, games: dict, iteration: int):
        """Fetch and save the played time in last two weeks per game

        Args:
            games (dict): data containing the fetched information about games
            iteration (int): current iteration in loop over amount of games
        """
        playtime_2weeks = (
            f"{divmod(games['response']['games'][iteration]['playtime_2weeks'], 60)[0]:4}h "
            f"{divmod(games['response']['games'][iteration]['playtime_2weeks'], 60)[1]:02}min"
        )

        self.playtime_2weeks_list.append(playtime_2weeks)

    def fetch_playtime_forever(self, games: dict, iteration: int):
        """Fetch and save the overall played time per game

        Args:
            games (dict): data containing the fetched information about games
            iteration (int): current iteration in loop over amount of games
        """
        playtime_forever = (
            f"{divmod(games['response']['games'][iteration]['playtime_forever'], 60)[0]:4}h "
            f"{divmod(games['response']['games'][iteration]['playtime_forever'], 60)[1]:02}min"
        )

        self.playtime_forever_list.append(playtime_forever)
