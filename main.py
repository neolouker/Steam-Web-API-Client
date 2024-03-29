"""Steam Web API Client

Graphical tool to fetch player information from Steam Web API.

Requires all modules listed in requirements.txt to be installed.
"""

from steam_web_api_client.gui.user_interface import UserInterface


def main():
    """Initializes the user interface."""
    user_interface = UserInterface()
    user_interface.root.mainloop()


if __name__ == "__main__":
    main()
