import sys
# import sdl2
import sdl2.ext

WINDOW_X = 640
WINDOW_Y = 480
WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLACK = sdl2.ext.Color(0, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
PINK = sdl2.ext.Color(255, 105, 180)
BLUE = sdl2.ext.Color(0, 0, 255)

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

class Car(object):
    def __init__(self, color, pos_x=0, pos_y=0, speed=5, size_x=5, size_y=5):
        self.speed = speed
        self.color = color
        self.position_x = pos_x
        self.position_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def move_left(self):
        if self.position_x - self.speed >= 0:
            self.position_x = self.position_x - self.speed
        else:
            self.position_x = 0

    def move_right(self):
        if self.position_x + self.size_x + self.speed <= WINDOW_X:
            self.position_x = self.position_x + self.speed
        else:
            self.position_x = WINDOW_X - self.size_x

    def move_up(self):
        if self.position_y - self.speed >= 0:
            self.position_y = self.position_y - self.speed
        else:
            self.position_y = 0

    def move_down(self):
        if self.position_y + self.size_y + self.speed <= WINDOW_Y:
            self.position_y = self.position_y + self.speed
        else:
            self.position_y = WINDOW_Y - self.size_y

    def render(self):
        renderer.fill((self.position_x, self.position_y, self.size_x, self.size_y), self.color)

#map needs to be a class in order to store data in itself (currently the pos of trees and bushes..)
class Map(object):
    def __init__(self, units={}): #units is a dictionary of coordinates of every units' position and their type
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
            if x < ((WINDOW_X // 2) - 50): # to generate trees on the sides, leaving space in the middle
                for y in range (0, WINDOW_Y):
                    if y < ((WINDOW_Y // 2) - 50):
                        if y % 10 == 0 and x % 10 == 0:
                            tree = Tree()
                            tree.position = [x, y]
                            tree_count += 1
                            self.units["tree" + str(tree_count)] = tree
                    elif y > ((WINDOW_Y // 2) + 50):
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

def game_event(event, map, players):
    keystates = sdl2.SDL_GetKeyboardState(None)
    if keystates[sdl2.SDL_SCANCODE_W]:
        print("w was pressed")
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
        pass
    elif event.type == sdl2.SDL_KEYDOWN:
        if event.key.keysym.sym == sdl2.SDLK_LEFT:
            players[0].move_left()
        if event.key.keysym.sym == sdl2.SDLK_RIGHT:
            players[0].move_right()
        if event.key.keysym.sym == sdl2.SDLK_UP:
            players[0].move_up()
        if event.key.keysym.sym == sdl2.SDLK_DOWN:
            players[0].move_down()
        if event.key.keysym.sym == sdl2.SDLK_a:
            players[1].move_left()
        if event.key.keysym.sym == sdl2.SDLK_d:
            players[1].move_right()
        if event.key.keysym.sym == sdl2.SDLK_w:
            players[1].move_up()
        if event.key.keysym.sym == sdl2.SDLK_s:
            players[1].move_down()


        #print(event.button.x)
        #print(event.button.y)
        #if map.units[event.button.x, event.button.y].type == "villager":
        #    print("selected villager!")


mouse_x = None
mouse_y = None

game_state = "menu"
menu = True
game = False
ending = False
map = None

game_running = True
last_step = 0
player_1 = Car(BLUE, 0, 0)
player_2 = Car(RED, 0, 10)
players = [player_1, player_2]

start_button = Button(320, 240, BLACK)
default_button_color = True
while game_running:
    if sdl2.SDL_GetTicks() - last_step >= 0:
        renderer.clear(WHITE)
        if ending:
            pass
        elif game:
            #menu = False
            if not map:
                map = Map()
                map.generate()
            map.render()
            for player in players:
                player.render()
        elif menu:
            start_button.render()

        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                game_running = False
                break
            if game and map:
                ending = game_event(event, map, players)
            elif menu:
                game = menu_event(event)
        renderer.present()  # updates renderer, this is critical to ensure your changes actually change
        window.refresh()  # updates window
        last_step = sdl2.SDL_GetTicks()