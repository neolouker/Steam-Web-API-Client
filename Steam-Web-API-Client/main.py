from tkinter import *
from tkinter.ttk import *
from steam.webapi import WebAPI
from PIL import ImageTk, Image
import urllib.request
import io
import webbrowser

class UserInterface:
    def __init__(self):
        # Root Window
        self.root = Tk()
        self.root.title("Steam Web API")
        ## Stretch and Resize
        self.root.resizable(True, True)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 1, weight=1)
        ## Variables
        self.api_key = StringVar()
        self.steam_id = StringVar()
        ## Widgets
        self.label1 = Label(self.root, text="Web API Key")
        self.label2 = Label(self.root, text="Steam ID")
        self.link1 = Label(self.root, text="(https://steamcommunity.com/dev/apikey)", foreground="blue", cursor="hand2")
        self.link1.bind("<Button-1>", lambda event: self.callback("https://steamcommunity.com/dev/apikey"))
        self.link2 = Label(self.root, text="(https://steamid.io/)", foreground="blue", cursor="hand2")
        self.link2.bind("<Button-1>", lambda event: self.callback("https://steamid.io/"))
        self.entry1 = Entry(self.root, textvariable=self.api_key, width=40, justify="center")
        self.entry2 = Entry(self.root, textvariable=self.steam_id, width=40, justify="center")
        self.button1 = Button(self.root, text="Enter", command=lambda: [self.root.withdraw(), self.handler(key=self.api_key.get(), id=self.steam_id.get())])
        ## Grid Placement
        self.label1.grid(row=0, column=0, padx=20, pady=2)
        self.label2.grid(row=0, column=1, padx=20, pady=2)
        self.link1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.link2.grid(row=1, column=1, padx=20, pady=(0, 10))
        self.entry1.grid(row=2, column=0, padx=20, pady=5, sticky="NSEW")
        self.entry2.grid(row=2, column=1, padx=20, pady=5, sticky="NSEW")
        self.button1.grid(row=3, column=0, columnspan=3, padx=20, pady=(25, 5), sticky="NSEW")
        # Information Storage
        self.image_list = []
        self.name_list = []
        self.playtime_2weeks_list = []
        self.playtime_forever_list = []

    def fetch_icons(self, response: dict, iter: int):
        app_id = response["response"]["games"][iter]["appid"]
        icon_hash = response["response"]["games"][iter]["img_icon_url"]
        icon_url_formatted = "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(appid=app_id , hash=icon_hash)
        with urllib.request.urlopen(icon_url_formatted, timeout=5) as image_data:
            image_file = io.BytesIO(image_data.read())
        # Create and store ImageTk objects in the list
        img = ImageTk.PhotoImage(Image.open(image_file))
        self.image_list.append(img)
    
    def fetch_names(self, response: dict, iter: int):
        game_name = response["response"]["games"][iter]["name"]
        self.name_list.append(game_name)

    def fetch_playtime_2weeks(self, response: dict, iter: int):
        playtime_2weeks = "%4dh %02dmin" % (divmod(response["response"]["games"][iter]["playtime_2weeks"], 60))
        self.playtime_2weeks_list.append(playtime_2weeks)
    
    def fetch_playtime_forever(self, response: dict, iter: int):
        playtime_forever = "%4dh %02dmin" % (divmod(response["response"]["games"][iter]["playtime_forever"], 60))
        self.playtime_forever_list.append(playtime_forever)

    def handler(self, key: str, id: int):
        # API
        steam = SteamAPI(api_key=key)
        output = steam.get_recently_played_games(steamid=id)
        amount_games = output["response"]["total_count"]
        # Response Window
        self.response = Toplevel()
        self.response.title("Steam Web API Response")
        self.response.resizable(True, True)
        # Iteration
        for i in range(amount_games):
            self.fetch_icons(response=output, iter=i)
            self.fetch_names(response=output, iter=i)
            self.fetch_playtime_2weeks(response=output, iter=i)
            self.fetch_playtime_forever(response=output, iter=i)
            # Create label with current ImageTk icon
            icon = Label(self.response, image=self.image_list[i])
            icon.grid(row=i, column=0, padx=10, pady=10)
            # Create label for game names
            name = Label(self.response, text=self.name_list[i])
            name.grid(row=i, column=1, pady=10)
            # Create label for playtime in last 2 weeks
            playtime_2weeks = Label(self.response, text=self.playtime_2weeks_list[i])
            playtime_2weeks.grid(row=i, column=2, padx=10, pady=10)
            # Create label for overall playtime
            playtime_forever = Label(self.response, text=self.playtime_forever_list[i])
            playtime_forever.grid(row=i, column=3, padx=10, pady=10)

        # When the response window is closed, destroy the main window
        self.response.protocol("WM_DELETE_WINDOW", self.on_response_close)
    
    def callback(self, url):
        webbrowser.open_new(url)

    def on_response_close(self):
        self.root.destroy()


class SteamAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_recently_played_games(self, steamid: int) -> dict:
        api = WebAPI(key=self.api_key)
        return api.IPlayerService.GetRecentlyPlayedGames(steamid=steamid, count=50, format="json")

def main():
    window = UserInterface()
    window.root.mainloop()

if __name__ == "__main__":
    main()
