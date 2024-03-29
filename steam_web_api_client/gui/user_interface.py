"""Setup general window of client"""

import os
import tkinter as tk
import webbrowser
from tkinter import ttk

from steam_web_api_client.core.data_handler import DataHandler
from steam_web_api_client.core.steam_api import SteamAPI


class UserInterface:
    """Create and manage the main user interface.

    Attributes:
        root = Tkinter root window
        api_key = A tkinter string holding the value of the steam api key
        steam_id = A tkinter string holding the value of the steam_id of an user
        data_path = A string containing the path of the data.json file
        icon_path = A string containing the path of the window icon
    """

    def __init__(self):
        # Initialize main window and variables
        self.root = tk.Tk()
        self.root.title("Steam Web API")
        self.api_key = tk.StringVar()
        self.steam_id = tk.StringVar()
        self.api_key.trace_add("write", lambda *args: self.limit_entry())
        self.steam_id.trace_add("write", lambda *args: self.limit_entry())
        self.data_path = os.path.join("steam_web_api_client", "data", "data.json")
        icon_path = os.path.join("steam_web_api_client", "assets", "icon.png")
        self.current_id = tk.StringVar()
        self.current_user = tk.StringVar()

        # Window Config
        self.root.resizable(True, True)
        self.root.configure(background="white")
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        self.root.iconphoto(True, tk.PhotoImage(file=icon_path))

        # Read from data\data.json
        self.data_handler = DataHandler(data_path=self.data_path)
        api_key = self.data_handler.read_data()
        self.api_key.set(api_key)

        # Widgets
        label1 = tk.Label(
            self.root,
            text="Web API Key",
            background="white",
            font=("Helvetica", 9, "bold"),
        )
        label2 = tk.Label(
            self.root,
            text="Steam ID",
            background="white",
            font=("Helvetica", 9, "bold"),
        )
        link1 = tk.Label(
            self.root,
            text="(https://steamcommunity.com/dev/apikey)",
            background="white",
            foreground="blue",
            cursor="hand2",
        )
        link1.bind(
            "<Button-1>",
            lambda event: self.open_browser("https://steamcommunity.com/dev/apikey"),
        )
        link2 = tk.Label(
            self.root,
            text="(https://steamid.io/)",
            background="white",
            foreground="blue",
            cursor="hand2",
        )
        link2.bind("<Button-1>", lambda event: self.open_browser("https://steamid.io/"))
        entry1 = ttk.Entry(
            self.root, textvariable=self.api_key, width=40, justify="center"
        )
        entry2 = ttk.Entry(
            self.root, textvariable=self.steam_id, width=40, justify="center"
        )
        label3 = tk.Label(self.root, textvariable=self.current_user, background="white")
        combo = ttk.Combobox(
            self.root, values=self.data_handler.id_list, textvariable=self.current_id
        )
        combo["state"] = "readonly"
        combo.bind("<<ComboboxSelected>>", lambda event: self.combobox_changed())
        button1 = ttk.Button(
            self.root,
            text="Enter",
            command=lambda: [self.root.withdraw(), self.open_response_window()],
        )

        # Grid Placement
        label1.grid(row=0, column=0, padx=20, pady=(10, 0))
        label2.grid(row=0, column=1, padx=20, pady=(10, 0))
        link1.grid(row=1, column=0, padx=20, pady=(0, 10))
        link2.grid(row=1, column=1, padx=20, pady=(0, 10))
        entry1.grid(row=2, column=0, padx=20, pady=5, sticky="NSEW")
        entry2.grid(row=2, column=1, padx=20, pady=5, sticky="NSEW")
        label3.grid(row=3, column=0, padx=20, pady=5)
        combo.grid(row=3, column=1, padx=20, pady=5)
        button1.grid(
            row=4, column=0, columnspan=3, padx=20, pady=(25, 5), sticky="NSEW"
        )

    def limit_entry(self):
        """Limit maximum characters in entries."""
        api_value = self.api_key.get()
        id_value = self.steam_id.get()
        if len(api_value) > 32:
            self.api_key.set(api_value[:32])
        if len(id_value) > 17:
            self.steam_id.set(id_value[:17])

    def open_browser(self, url: str) -> None:
        """Opens a new tab in browser and follows link.

        Args:
            url (str): A string holding the value of a link
        """
        webbrowser.open_new(url)

    def combobox_changed(self):
        """Handle the steam ID in combobox changed event."""
        if self.current_id.get() is not None:
            self.steam_id.set(self.current_id.get())
            self.current_user.set(
                self.data_handler.get_username_by_id(self.current_id.get())
            )

    def open_response_window(self) -> None:
        """Opens a window containing the response of the API."""
        ResponseWindow(
            self.root,
            api_key=self.api_key,
            steam_id=self.steam_id,
            data_handler=self.data_handler,
        )


class ResponseWindow:
    """Create and manage the response window showing Steam API information.

    Attributes:
        root = root window
        api_key = A tkinter string holding the value of the steam api key
        steam_id = A tkinter string holding the value of the steam_id of an user
        data_handler = An existing object of the DataHandler class
        response = A new toplevel window for response information
    """

    def __init__(
        self, root, api_key: tk.StringVar, steam_id: tk.StringVar, data_handler
    ):
        # Initialize response window and variables
        self.root = root
        self.api_key = api_key
        self.steam_id = steam_id
        self.response = tk.Toplevel(self.root)
        self.response.title("Steam Web API")
        self.response.resizable(False, False)
        self.steam_api = SteamAPI(api_key=self.api_key.get())
        self.row_end = 0
        self.total_time_2weeks = 0

        # Create a canvas with the vertical scrollbar
        scrollbar = ttk.Scrollbar(self.response, orient="vertical")
        canvas = tk.Canvas(
            self.response, yscrollcommand=scrollbar.set, background="white"
        )

        # Create a frame inside the canvas to hold the widgets
        frame = tk.Frame(canvas, background="white")

        # Steam Web API
        games = self.steam_api.get_recently_played_games(steamid=self.steam_id.get())
        summary = self.steam_api.get_player_summaries(steamid=steam_id.get())

        # Error Handling
        if not games["response"] or not summary["response"]:
            self.root.destroy()
            print("[INFO] Response Window has been closed!")
            user_interface = UserInterface()
            user_interface.root.mainloop()
            return

        # Data Handler
        data_handler.api_key = self.api_key.get()
        self.steam_api.fetch_username(summaries=summary)
        data_handler.username_list.append(self.steam_api.username_list[0])
        if self.steam_id.get() not in data_handler.id_list:
            if len(data_handler.id_list) >= 10:
                data_handler.id_list[-1] = self.steam_id.get()
            else:
                data_handler.id_list.append(self.steam_id.get())

            data_handler.save_data()

        amount_games = games["response"]["total_count"]

        # Create and place static widgets
        self.create_static_widgets(summary=summary, frame=frame)

        # Create and place dynamic widgets
        self.total_time_2weeks = self.create_dynamic_widgets(
            amount_games=amount_games, games=games, frame=frame
        )

        separator4 = ttk.Separator(frame, orient="horizontal")
        separator4.grid(row=self.row_end, column=0, columnspan=4, sticky="WE")

        str_total_time_2weeks = (
            f"{divmod(self.total_time_2weeks, 60)[0]:4}h "
            f"{divmod(self.total_time_2weeks, 60)[1]:02}min"
        )

        label4 = tk.Label(
            frame,
            text=str_total_time_2weeks,
            font=("Helvetica", 9, "bold"),
            background="white",
        )
        label4.grid(row=self.row_end + 1, column=2, padx=45, pady=15, sticky="E")

        # Configure canvas
        self.config_canvas(canvas=canvas, scrollbar=scrollbar, frame=frame)

        # Automatically adjust the window size based on the content
        self.response.update_idletasks()
        self.response.geometry(
            f"{frame.winfo_reqwidth()}x{min(frame.winfo_reqheight(), 500)}"
        )

        # When the response window is closed, destroy the main window
        self.response.protocol("WM_DELETE_WINDOW", self.on_response_close)

    def create_static_widgets(self, summary: dict, frame: ttk.Frame) -> None:
        # pylint: disable=too-many-locals
        """Create widgets showing user information.

        Args:
            summary (dict): data containing the fetched information about user
            frame (ttk.Frame): the area to place widgets onto
        """
        # User Information
        self.steam_api.fetch_avatar(summaries=summary)
        user_status_value = self.steam_api.fetch_user_status(summaries=summary)
        last_logoff_value = self.steam_api.fetch_last_logoff(summaries=summary)
        if user_status_value == "Online":
            last_logoff_value = "Now"

        # Static Widgets
        status_head = tk.Label(
            frame, text="Status", font=("Helvetica", 9, "bold"), background="white"
        )
        last_logoff_head = tk.Label(
            frame,
            text="Last Time Seen",
            font=("Helvetica", 9, "bold"),
            background="white",
        )
        separator1 = ttk.Separator(frame, orient="horizontal")
        avatar_head = tk.Label(
            frame, image=self.steam_api.avatar_list[0], background="white"
        )
        username = tk.Label(
            frame, text=self.steam_api.username_list[0], background="white"
        )
        status = tk.Label(frame, text=user_status_value, background="white")
        last_logoff = tk.Label(frame, text=last_logoff_value, background="white")
        separator2 = ttk.Separator(frame, orient="horizontal")
        playtime_2weeks_head = tk.Label(
            frame,
            text="Last 2 Weeks",
            font=("Helvetica", 9, "bold"),
            background="white",
        )
        playtime_forever_head = tk.Label(
            frame, text="Overall", font=("Helvetica", 9, "bold"), background="white"
        )
        separator3 = ttk.Separator(frame, orient="horizontal")

        # Grid Placement
        status_head.grid(row=0, column=2, padx=5, pady=5)
        separator1.grid(row=1, column=0, columnspan=4, sticky="WE")
        avatar_head.grid(row=2, column=0, padx=5, pady=10)
        last_logoff_head.grid(row=0, column=3, padx=25, pady=5)
        username.grid(row=2, column=1, padx=5, pady=10, sticky="W")
        status.grid(row=2, column=2, padx=5, pady=10)
        last_logoff.grid(row=2, column=3, padx=5, pady=10)
        separator2.grid(row=3, column=0, columnspan=4, sticky="WE")
        playtime_2weeks_head.grid(row=4, column=2, padx=25, sticky="WE")
        playtime_forever_head.grid(row=4, column=3, padx=25, sticky="WE")
        separator3.grid(row=5, column=0, columnspan=4, sticky="WE")

    def create_dynamic_widgets(
        self, amount_games: int, games: dict, frame: ttk.Frame
    ) -> int:
        """Create widgets showing game information.

        Args:
            amount_games (int): amount of games returned from API
            games (dict): data containing the fetched information about games
            frame (ttk.Frame): the area to place widgets onto

        Returns:
            int: total played time in 2 weeks
        """

        total_time_2weeks = 0

        if amount_games > 0:
            for i in range(amount_games):
                # Playtime Information
                self.steam_api.fetch_icons(games=games, iteration=i)
                self.steam_api.fetch_names(games=games, iteration=i)
                self.steam_api.fetch_playtime_2weeks(games=games, iteration=i)
                self.steam_api.fetch_playtime_forever(games=games, iteration=i)

                total_time_2weeks += games["response"]["games"][i]["playtime_2weeks"]

                # Dynamic Widgets
                icon = tk.Label(
                    frame, image=self.steam_api.image_list[i], background="white"
                )
                title = tk.Label(
                    frame, text=self.steam_api.name_list[i], background="white"
                )
                playtime_2weeks = tk.Label(
                    frame,
                    text=self.steam_api.playtime_2weeks_list[i],
                    background="white",
                )
                playtime_forever = tk.Label(
                    frame,
                    text=self.steam_api.playtime_forever_list[i],
                    background="white",
                )

                # Grid Placement
                row_begin = i + 6
                icon.grid(row=row_begin, column=0, padx=5, pady=5)
                title.grid(row=row_begin, column=1, padx=(5, 30), pady=5, sticky="W")
                playtime_2weeks.grid(
                    row=row_begin, column=2, padx=45, pady=5, sticky="E"
                )
                playtime_forever.grid(
                    row=row_begin, column=3, padx=45, pady=5, sticky="E"
                )

                self.row_end = row_begin + 1
        else:
            placeholder_label = tk.Label(
                frame,
                text="No Games Found",
                background="white",
                font=("Helvetica", 11),
            )
            placeholder_label.grid(row=6, column=0, columnspan=4, padx=5, pady=20)
            self.row_end = 7

        return total_time_2weeks

    def config_canvas(
        self, canvas: tk.Canvas, scrollbar: tk.Scrollbar, frame: tk.Frame
    ) -> None:
        """Adjust canvas options based on content.

        Args:
            canvas (tk.Canvas): the area where the content frame is in
        """
        scrollbar.pack(side="right", fill="y")
        scrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=(0, 0))

        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Update the scroll region whenever the canvas is updated
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind the canvas scrolling to the scrollbar
        # Automatically adjust the canvas width based on the content
        canvas.bind("<Configure>", lambda e: canvas.config(width=canvas.winfo_width()))
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
        )

    def on_response_close(self) -> None:
        """When closing the response window also close root window."""
        if self.root.winfo_exists():
            self.root.destroy()
