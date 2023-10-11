# user_interface.py
import tkinter as tk
from tkinter import ttk
from core.steam_api import SteamAPI
from core.data_handler import DataHandler
import webbrowser
import os


class UserInterface:
    def __init__(self):
        # Variables
        self.root = tk.Tk()
        self.root.title("Steam Web API")
        self.api_key = tk.StringVar()
        self.steam_id = tk.StringVar()
        self.data_path = os.path.join(
            "Steam-Web-API-Client", "data", "data.json")
        self.icon_path = os.path.join(
            "Steam-Web-API-Client", "assets", "icon.png")

        # Window Config
        self.root.resizable(True, True)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        self.root.iconphoto(True, tk.PhotoImage(file=self.icon_path))

        # Read from data\data.json
        self.data_handler = DataHandler(
            data_path=self.data_path, api_key=self.api_key, steam_id=self.steam_id)
        self.data = self.data_handler.read_data()
        self.api_key.set(self.data[0])
        self.steam_id.set(self.data[1])

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

    def open_browser(self, url: str):
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

        # Create a canvas with the vertical scrollbar
        scrollbar = ttk.Scrollbar(self.response, orient="vertical")
        canvas = tk.Canvas(self.response, yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scrollbar.config(command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas to hold the widgets
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Data Handler
        self.data_handler = DataHandler(
            data_path=self.data_path, api_key=self.api_key.get(), steam_id=self.steam_id.get())

        # Save Input Data in data\data.json
        self.data_handler.write_data()

        # Steam Web API
        self.steam_api = SteamAPI(api_key=self.api_key.get())
        games = self.steam_api.get_recently_played_games(
            steamid=self.steam_id.get())
        summary = self.steam_api.get_player_summaries(
            steamid=self.steam_id.get())
        amount_games = games["response"]["total_count"]

        # User Information
        self.avatar = self.steam_api.fetch_avatar(summaries=summary)
        self.username = self.steam_api.fetch_username(summaries=summary)
        self.user_status = self.steam_api.fetch_user_status(summaries=summary)

        # Static Widgets
        avatar = tk.Label(frame, image=self.avatar)
        username = tk.Label(frame, text=self.username)
        status = tk.Label(frame, text=self.user_status)
        separator1 = ttk.Separator(frame, orient="horizontal")
        title_head = tk.Label(frame, text="Title")
        playtime_2weeks_head = tk.Label(frame, text="Last 2 Weeks")
        playtime_forever_head = tk.Label(frame, text="Overall")
        separator2 = ttk.Separator(frame, orient="horizontal")

        # Grid Placement
        avatar.grid(row=0, column=0, padx=10, pady=15)
        username.grid(row=0, column=1, padx=10, pady=15)
        status.grid(row=0, column=2, padx=10, pady=15)
        separator1.grid(row=1, column=0, columnspan=4, sticky="EW")
        title_head.grid(row=2, column=1, padx=10)
        playtime_2weeks_head.grid(row=2, column=2, padx=10)
        playtime_forever_head.grid(row=2, column=3, padx=10)
        separator2.grid(row=3, column=0, columnspan=4, sticky="EW")

        for i in range(amount_games):

            # Playtime Information
            self.steam_api.fetch_icons(games=games, iteration=i)
            self.steam_api.fetch_names(games=games, iteration=i)
            self.steam_api.fetch_playtime_2weeks(games=games, iteration=i)
            self.steam_api.fetch_playtime_forever(games=games, iteration=i)

            # Dynamic Widgets
            icon = tk.Label(frame, image=self.steam_api.image_list[i])
            title = tk.Label(frame, text=self.steam_api.name_list[i])
            playtime_2weeks = tk.Label(
                frame, text=self.steam_api.playtime_2weeks_list[i])
            playtime_forever = tk.Label(
                frame, text=self.steam_api.playtime_forever_list[i])

            # Grid Placement
            row_begin = i + 4
            icon.grid(row=row_begin, column=0, padx=10, pady=5)
            title.grid(row=row_begin, column=1, padx=40, pady=5)
            playtime_2weeks.grid(row=row_begin, column=2, padx=20, pady=5)
            playtime_forever.grid(row=row_begin, column=3, padx=20, pady=5)

        # Update the scroll region whenever the canvas is updated
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind the canvas scrolling to the scrollbar
        # Automatically adjust the canvas width based on the content
        canvas.bind("<Configure>", lambda e: canvas.config(width=e.width))
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(
            int(-1 * (event.delta / 120)), "units"))

        # Automatically adjust the window size based on the content
        self.response.update_idletasks()
        self.response.geometry(
            f"{frame.winfo_reqwidth()}x{min(frame.winfo_reqheight(), 500)}")

        # When the response window is closed, destroy the main window
        self.response.protocol("WM_DELETE_WINDOW", self.on_response_close)

    def on_response_close(self):
        self.root.destroy()
