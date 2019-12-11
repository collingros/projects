import sys
import sdl2
import sdl2.ext
#from sdl2 import *

WINDOW_X = 640
WINDOW_Y = 480
WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLACK = sdl2.ext.Color(0, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
PINK = sdl2.ext.Color(255, 105, 180)

BACKGROUND_COLOR = WHITE

sdl2.ext.init()


window = sdl2.ext.Window("Python Project", size=(WINDOW_X, WINDOW_Y))
window.show()
renderer = sdl2.ext.Renderer(window)

class Player(object):
    def __init__(self, money, resources):
        self.money = money
        self.resources = resources


class Tree(object):
    def __init__(self):
        self.wood = 100
        self.position = [0, 0]
        self.type = "tree" #thinking of iterating through the unit dict to find just trees,
        # compared to bushes or villagers to render them as green squares

    def render(self):
        if self.wood > 0:
            renderer.fill((self.position[0], self.position[1], 5, 5), GREEN)


class Bush(object):
    def __init__(self):
        self.food = 100
        self.position = [0, 0]
        self.type = "bush" #thinking of iterating through the unit dict to find just trees,
        # compared to bushes or villagers to render them as green squares

    def render(self):
        if self.food > 0:
            renderer.fill((self.position[0], self.position[1], 5, 5), PINK)


class Villager(object):
    def __init__(self):
        self.health = 100
        self.position = [0, 0]
        self.type = "villager"

    def build(self, obj):
        pass



class Swordsman(object):
    pass


#map needs to be a class in order to store data in itself (currently the pos of trees and bushes..)
class Map(object):
    def __init__(self, units = dict()): #units is a dictionary of coordinates of every units' position and their type
        self.units = units
        self.generated = False

    def render(self):
        for unit_name, unit in self.units.items():
            if unit.type == "tree" or unit.type == "bush":
                unit.render()

    def generate(self):
        tree_count = 0
        bush_count = 0
        for x in range (0, WINDOW_X):
            if x < ((WINDOW_X // 2) - 50) or x > ((WINDOW_X // 2) + 50): # to generate trees on the sides, leaving space in the middle
                for y in range (0, WINDOW_Y):
                    if y < ((WINDOW_Y // 2) - 50) or y > ((WINDOW_Y // 2) + 50):
                        if y % 10 == 0 and x % 10 == 0:
                            tree = Tree()
                            tree.position = [x, y]
                            tree_count += 1
                            self.units["tree" + str(tree_count)] = tree
            else:
                for y in range (0, WINDOW_Y):
                    if y > ((WINDOW_Y // 2) - 50) and y < ((WINDOW_Y // 2) + 50):
                        if y % 10 == 0 and x % 10 == 0:
                            bush = Bush()
                            bush.position = [x, y]
                            bush_count += 1
                            self.units["bush" + str(bush_count)] = bush
        self.generated = True

class Button(object):
    def __init__(self, pos_x, pos_y, color, width_x=100, width_y=30):
        self.width_x = width_x
        self.width_y = width_y
        self.pos_x = pos_x - width_x // 2
        self.pos_y = pos_y - width_y // 2
        self.color = color
        self.default_color = True
        # self.rendeRED = False i was thinking of maybe adding this to make it disappear,
        # but that's probably stupid and you can do it another way

    def render(self):
        renderer.fill((self.pos_x, self.pos_y, self.width_x, self.width_y), self.color)
        # self.rendeRED = True

    def message(self, message=""):
        pass

    def destroy(self):
        renderer.fill((self.pos_x, self.pos_y, self.width_x, self.width_y), (0, 0, 0))

def menu_event(event):
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
        if event.button.button == sdl2.SDL_BUTTON_LEFT:
            mouse_x = event.button.x
            mouse_y = event.button.y
            if (mouse_x >= start_button.pos_x and mouse_x <= start_button.pos_x + start_button.width_x) and (
                    mouse_y >= start_button.pos_y and mouse_y <= start_button.pos_y + start_button.width_y):
                if start_button.default_color:
                    start_button.color = RED
                    start_button.default_color = False


    elif event.type == sdl2.SDL_MOUSEBUTTONUP:
        start_button.destroy()
        return True
    return False

def game_event(event, map):
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
        #print(event.button.x)
        #print(event.button.y)
        if map.units[event.button.x, event.button.y].type == "villager":
            print("selected villager!")


mouse_x = None
mouse_y = None

game_state = "menu"
menu = True
game = False
ending = False
map = None

game_running = True
last_step = 0

start_button = Button(320, 240, WHITE)
default_button_color = True
while game_running:
    if sdl2.SDL_GetTicks() - last_step >= 0:
        if ending:
            pass
        elif game:
            #menu = False
            if not map:
                map = Map()
                map.generate()
                map.render()
            else:
                map.render()
                pass
        elif menu:
            start_button.render()

        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                game_running = False
                break
            if game and map:
                ending = game_event(event, map)
            elif menu:
                game = menu_event(event)
        renderer.present()  # updates renderer, this is critical to ensure your changes actually change
        window.refresh()  # updates window
        last_step = sdl2.SDL_GetTicks()