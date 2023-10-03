from steam.webapi import WebAPI

api = WebAPI(key="6A26C9F8553573EE4362267C36D99767")

def get_recently_played_games(ID: int):
    output = api.IPlayerService.GetRecentlyPlayedGames(steamid=ID, count=50, format="json")
    amount_games = output["response"]["total_count"]
    for i in range(amount_games):
        print(output["response"]["games"][i]["name"].ljust(25) + "|".ljust(2), end="")
        print("%4dh %02dmin".ljust(15) % (divmod(output["response"]["games"][i]["playtime_2weeks"], 60)) + "|".ljust(3), end="")
        print("%4dh %02dmin".ljust(15) % (divmod(output["response"]["games"][i]["playtime_forever"], 60)) + "|".ljust(5))

def main():
    get_recently_played_games(ID=76561198353694153)

if __name__ == "__main__":
    main()
