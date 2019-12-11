from Player import Player
from easygui import *

if boolbox("Would you like to play singleplayer or multiplayer?", "Age of Empires - Game Setup", ["Singleplayer", "Multiplayer"]):
    choice = indexbox("Choose your level of starting resources.", title="Age of Empires - Game Setup", choices=["Low", "Standard", "High"])
    if choice == 0:
        resources = {"Food": 150, "Wood": 50, "Stone": 50, "Gold": 25}
    elif choice == 1:
        resources = {"Food": 300, "Wood": 100, "Stone": 100, "Gold": 50}
    elif choice == 2:
        resources = {"Food": 600, "Wood": 200, "Stone": 200, "Gold": 100}
    else:
        print("Error: Choice selected does not exist...")
    player_1 = Player("Blue", resources)
    player_2 = Player("Red", resources)

    print player_1.get_team()
    print player_1.get_resources()
else:
    pass