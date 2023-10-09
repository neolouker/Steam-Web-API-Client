# user_interface.py
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from core.steam_api import SteamAPI
from core.data_handler import DataHandler
import urllib.request
import io
import webbrowser


class UserInterface:
    def __init__(self):
        # Root Window
        self.root = tk.Tk()
        self.root.title("Steam Web API")
        # Stretch and Resize
        self.root.resizable(True, True)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        # Variables
        self.api_key = tk.StringVar()
        self.steam_id = tk.StringVar()
        self.data_path = "Steam-Web-API-Client\data\data.json"
        # Read from data\data.json
        self.data_handler = DataHandler(
            data_path=self.data_path, api_key=self.api_key, steam_id=self.steam_id)
        self.api_key.set(self.data_handler.read_data()[0])
        self.steam_id.set(self.data_handler.read_data()[1])
        # Widgets
        self.label1 = tk.Label(self.root, text="Web API Key")
        self.label2 = tk.Label(self.root, text="Steam ID")
        self.link1 = tk.Label(
            self.root, text="(https://steamcommunity.com/dev/apikey)", foreground="blue", cursor="hand2")
        self.link1.bind(
            "<Button-1>", lambda event: self.open_browser("https://steamcommunity.com/dev/apikey"))
        self.link2 = tk.Label(self.root, text="(https://steamid.io/)",
                              foreground="blue", cursor="hand2")
        self.link2.bind(
            "<Button-1>", lambda event: self.open_browser("https://steamid.io/"))
        self.entry1 = ttk.Entry(
            self.root, textvariable=self.api_key, width=40, justify="center")
        self.entry2 = ttk.Entry(
            self.root, textvariable=self.steam_id, width=40, justify="center")
        self.button1 = ttk.Button(self.root, text="Enter", command=lambda: [
            self.root.withdraw(), self.open_response_window()])
        # Grid Placement
        self.label1.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.label2.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.link1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.link2.grid(row=1, column=1, padx=20, pady=(0, 10))
        self.entry1.grid(row=2, column=0, padx=20, pady=5, sticky="NSEW")
        self.entry2.grid(row=2, column=1, padx=20, pady=5, sticky="NSEW")
        self.button1.grid(row=3, column=0, columnspan=3,
                          padx=20, pady=(25, 5), sticky="NSEW")

    def open_browser(self, url):
        webbrowser.open_new(url)

    def open_response_window(self):
        response_window = ResponseWindow(
            self.root, api_key=self.api_key, steam_id=self.steam_id, data_path=self.data_path)


class ResponseWindow:
    def __init__(self, root, api_key: tk.StringVar, steam_id: tk.StringVar, data_path):
        # Window Instance
        self.root = root
        self.api_key = api_key
        self.steam_id = steam_id
        self.data_path = data_path
        self.response = tk.Toplevel(self.root)
        self.response.title("Steam Web API")
        self.response.resizable(True, True)
        # Information Storage
        self.image_list = []
        self.name_list = []
        self.playtime_2weeks_list = []
        self.playtime_forever_list = []
        # Data Handler
        self.data_handler = DataHandler(
            data_path=self.data_path, api_key=self.api_key.get(), steam_id=self.steam_id.get())
        # Save Input Data in data\data.json
        self.data_handler.write_data()
        # Steam Web API
        steam_api = SteamAPI(api_key=self.api_key.get())
        output = steam_api.get_recently_played_games(
            steamid=self.steam_id.get())
        amount_games = output["response"]["total_count"]

        # Iteration
        for i in range(amount_games):
            # Source Information
            self.fetch_icons(response=output, iter=i)
            self.fetch_names(response=output, iter=i)
            self.fetch_playtime_2weeks(response=output, iter=i)
            self.fetch_playtime_forever(response=output, iter=i)
            # Widgets
            title_head = tk.Label(self.response, text=("Title"))
            playtime_2weeks_head = tk.Label(
                self.response, text="Last 2 Weeks")
            playtime_forever_head = tk.Label(
                self.response, text="Overall")
            separator = ttk.Separator(self.response, orient="horizontal")
            icon = tk.Label(self.response, image=self.image_list[i])
            title = tk.Label(self.response, text=self.name_list[i])
            playtime_2weeks = tk.Label(
                self.response, text=self.playtime_2weeks_list[i])
            playtime_forever = tk.Label(
                self.response, text=self.playtime_forever_list[i])
            # Grid Placement
            row_begin = i + 2
            title_head.grid(row=0, column=1, padx=10)
            playtime_2weeks_head.grid(row=0, column=2, padx=10)
            playtime_forever_head.grid(row=0, column=3, padx=10)
            separator.grid(row=1, column=0, columnspan=4, sticky="EW")
            icon.grid(row=row_begin, column=0, padx=10, pady=10)
            title.grid(row=row_begin, column=1, padx=40, pady=10)
            playtime_2weeks.grid(row=row_begin, column=2, padx=10, pady=10)
            playtime_forever.grid(row=row_begin, column=3, padx=10, pady=10)

        # When the response window is closed, destroy the main window
        self.response.protocol("WM_DELETE_WINDOW", self.on_response_close)

    def fetch_icons(self, response: dict, iter: int):
        app_id = response["response"]["games"][iter]["appid"]
        icon_hash = response["response"]["games"][iter]["img_icon_url"]
        icon_url_formatted = "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(
            appid=app_id, hash=icon_hash)
        with urllib.request.urlopen(icon_url_formatted, timeout=5) as image_data:
            image_file = io.BytesIO(image_data.read())
        # Create and store ImageTk objects in the list
        img = ImageTk.PhotoImage(Image.open(image_file))
        self.image_list.append(img)

    def fetch_names(self, response: dict, iter: int):
        game_name = response["response"]["games"][iter]["name"]
        self.name_list.append(game_name)

    def fetch_playtime_2weeks(self, response: dict, iter: int):
        playtime_2weeks = "%4dh %02dmin" % (
            divmod(response["response"]["games"][iter]["playtime_2weeks"], 60))
        self.playtime_2weeks_list.append(playtime_2weeks)

    def fetch_playtime_forever(self, response: dict, iter: int):
        playtime_forever = "%4dh %02dmin" % (
            divmod(response["response"]["games"][iter]["playtime_forever"], 60))
        self.playtime_forever_list.append(playtime_forever)

    def on_response_close(self):
        self.root.destroy()
