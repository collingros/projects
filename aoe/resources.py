from easygui import *  # for gui


def add_resources(player, type_, amount):  # adds
    amount = int(amount)
    type_ = str(type_)
    resources[player][type_] += amount
    return


def subtract_resources(player, type_, amount):
    amount = int(amount)
    type_ = str(type_)
    if resources[player][type_] >= amount:
        resources[player][type_] -= amount
    else:
        print("Not enough " + type_ + "!")
    return


def buy(player, object):
    return


def resource_setup(choice, playerlist, resource_dict):
    if choice == 0:
        for i in range(0, len(playerlist)):
            resource_dict[playerlist[i]] = {"Food": 150, "Wood": 50, "Stone": 25, "Gold": 50}
    elif choice == 1:
        for i in range(0, len(playerlist)):
            resource_dict[playerlist[i]] = {"Food": 300, "Wood": 100, "Stone": 100, "Gold": 50}
    elif choice == 2:
        for i in range(0, len(playerlist)):
            resource_dict[playerlist[i]] = {"Food": 500, "Wood": 200, "Stone": 125, "Gold": 100}
    print("exiting resource_setup with resources: ", resource_dict)
    return


# Main
# 2 players. player1 on blue player2 on red
# ask if player2 is an ai
players = []
resources = dict()
objects = dict()

if boolbox("Is Player 2 an AI?", "Age of Empires - Game Setup", ["Yes", "No"]):
    singleplayer = True  # to be implemented - (if singleplayer)
    players.append("player1")
    players.append("player2")
else:
    singleplayer = False  # to be implemented - (if multiplayer)
starting_resource_choice = indexbox("Choose the amount of starting resources.", title="Age of Empires - Game Setup",
                                    choices=["Low", "Standard", "High"])  # 0 for low 1 for standard 2 for high
resource_setup(starting_resource_choice, players, resources)
resource_choice = indexbox("Choose what you want to do.", title="Age of Empires - TESTING",
                           choices=["Buy", "Sell"])  # testing buying / selling resources 0 for buy 1 for sell
if resource_choice == 0:
    resource_choice = indexbox(
        "You have " + str(resources[players[0]]["Gold"]) + " gold. Choose the resource you want to buy.",
        title="Age of Empires - TESTING", choices=["Food", "Wood", "Stone"])  # 0 food 1 wood 2 stone 3 gold

else:
    pass

print(resources)

'''
nump = input("Enter how many players will be playing this game: ")
resources = dict()
team = dict()
objects = {}

def addResources(player, type_, amount):
    amount = int(amount)
    type_ = str(type_)
    resources[player][type_] += amount
def subtractResources(player, type_, amount):
    amount = int(amount)
    type_ = str(type_)
    if resources[player][type_] >= amount:
        resources[player][type_] -= amount
    else:
        print("Not enough " + type_ + "!")
def buy(player, object):
    return

for i in range(0, int(nump)):
    playername = input("Enter player " + str(i + 1) + "\'s name: ")
    teamname = input("Enter player " + str(i + 1) + "\'s team: ")
    team[playername] = teamname
    ans = input("Choose your grade of starting resources: \n\t[l]ow\n\t[s]tandard\n\t[h]igh")
    if ans == "l":
        resources[playername] = {"Food": 150, "Wood": 50, "Stone": 25, "Gold": 50}
    elif ans == "s":
        resources[playername] = {"Food": 300, "Wood": 100, "Stone": 100, "Gold": 50}
    elif ans == "h":
        resources[playername] = {"Food": 500, "Wood": 200, "Stone": 125, "Gold": 100}

print("pre-resources: ", resources)
addResources("Collin", "Food", 50)
print("newresources: ", resources)
subtractResources("Collin", "Food", 51221)
print("new2resources: ", resources)
'''








