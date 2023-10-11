# steam_api.py
from steam.webapi import WebAPI
from PIL import ImageTk, Image
import urllib.request
import io


class SteamAPI:
    def __init__(self, api_key: str):
        self.api = WebAPI(key=api_key)
        self.image_list = []
        self.name_list = []
        self.playtime_2weeks_list = []
        self.playtime_forever_list = []

    def get_recently_played_games(self, steamid: int) -> dict:
        return self.api.IPlayerService.GetRecentlyPlayedGames(steamid=steamid, count=50, format="json")

    def get_player_summaries(self, steamid: int) -> dict:
        return self.api.ISteamUser.GetPlayerSummaries(steamids=steamid, format="json")

    def fetch_avatar(self, summaries: dict):
        avatar_url = summaries["response"]["players"][0]["avatar"]
        try:
            with urllib.request.urlopen(avatar_url, timeout=10) as image_data:
                image_file = io.BytesIO(image_data.read())
            img = ImageTk.PhotoImage(Image.open(image_file))
            return img
        except Exception as e:
            print("Error fetching avatar:", e)

    def fetch_username(self, summaries: dict):
        return summaries["response"]["players"][0]["personaname"]

    def fetch_user_status(self, summaries: dict):
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
            case 5:
                return "Looking to trade"
            case 6:
                return "Looking to play"
            case default:
                return ""

    def fetch_icons(self, games: dict, iteration: int):
        app_id = games["response"]["games"][iteration]["appid"]
        icon_hash = games["response"]["games"][iteration]["img_icon_url"]
        icon_url_formatted = "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(
            appid=app_id, hash=icon_hash)
        try:
            with urllib.request.urlopen(icon_url_formatted, timeout=10) as image_data:
                image_file = io.BytesIO(image_data.read())
            # Create and store ImageTk objects in the list
            img = ImageTk.PhotoImage(Image.open(image_file))
            self.image_list.append(img)
        except Exception as e:
            print("Error fetching icon:", e)
            # Append a placeholder or handle the error accordingly
            self.image_list.append(None)

    def fetch_names(self, games: dict, iteration: int):
        game_name = games["response"]["games"][iteration]["name"]
        self.name_list.append(game_name)

    def fetch_playtime_2weeks(self, games: dict, iteration: int):
        playtime_2weeks = "%4dh %02dmin" % (
            divmod(games["response"]["games"][iteration]["playtime_2weeks"], 60))
        self.playtime_2weeks_list.append(playtime_2weeks)

    def fetch_playtime_forever(self, games: dict, iteration: int):
        playtime_forever = "%4dh %02dmin" % (
            divmod(games["response"]["games"][iteration]["playtime_forever"], 60))
        self.playtime_forever_list.append(playtime_forever)
