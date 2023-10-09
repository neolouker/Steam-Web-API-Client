# steam_api.py
from steam.webapi import WebAPI


class SteamAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_recently_played_games(self, steamid: int) -> dict:
        api = WebAPI(key=self.api_key)
        return api.IPlayerService.GetRecentlyPlayedGames(steamid=steamid, count=50, format="json")
