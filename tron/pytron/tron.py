# Collin Gros
# 10-31-18

# Create a "tron" style game. The game has a menu, where the user can choose
# offline, online, settings, and quit.

# in offline:
#   the rules of tron are played in split-screen (on alocal keyboard).
# in online:
#   the rules of tron are played using a server-client connection
# in settings:
#   the user can change various settings that affect the game
# in quit:
#   the game immediately exits


class Game:
# the game, has control over everything
    def __init__():
        self.data = Data()


class Data:
# contains settings from the settings.txt file, as well as all player
# data
    def __init__():
        self.settings = self.load_settings()
        self.players = self.load_players()


    def load_settings(set_file="settings.txt"):
        settings = {}

        with open(set_file, "r") as my_file:
            for line in my_file:
                my_line = line.strip()
                line_substr = my_line.split(":")

                key = line_substr[0]
                val = line_substr[1]
                settings[player][key] = val

        return settings


    def load_players():
        # problem: what if multiple players want different settings?
        # 2d dict needed


class Player:
# represents the square that is drawn on the screen and can be controlled
# seperately by each user playing the game.
# contains its own render functions
# also has a trail
    def __init__():
        pass


class Trail:
# represents the player's extension of themselves as they move across
# the window (their wall, or trail left behind them). will kill any
# player that touches it
    def __init__():
        pass


class Screen:
# represents the window of the game rendering workhorse
    def __init__():
        pass


class Music:
# plays music appropriate to the state of the game
    def __init__():
        pass


class Menu:
# decides what the game does based on user input
    def __init__():
        pass


class Network:
# does all the complicated online multiplayer stuff
    def __init__():
        pass

