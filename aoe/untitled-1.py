nump = input("Enter how many players will be playing this game: ")
resources = dict()
team = dict()
objects = {}

def addResources(player, type, amount):
    amount = int(amount)
    type = str(type)
    resources[player][type] += amount
def subtractResources(player, type, amount):
    amount = int(amount)
    type = str(type)
    if resources[player][type] >= amount:
        resources[player][type] -= amount
    else:
        print("Not enough " + type + "!")
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









