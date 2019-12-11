# Collin Gros
#
# tron game in python
#
# TODO:
# completely rewrite everything
# be efficient
# debug
# networking:
#       multiplayer
#       ready up buttons
#       menu
#       customization
#
# DIRECTIONS:
#    LEFT: 4
#    RIGHT: 6
#    UP: 8
#    DOWN: 2
#
# COLORS:
#    GREEN: {"x":0, "y":WIN_H/2}
#    RED: {"x":WIN_X-PLAYER_WIDTH, "y":WIN_H/2}
#
import os
import sdl2.ext


# do i need these global variables
# could move them to screen
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)


class Screen:
    def __init(self, WIN_X, WIN_Y)
        sdl2.ext.init()

        self.window = sdl2.ext.Window("PYTRON", size=(WIN_X, WIN_Y))
        self.renderer = sdl2.ext.Renderer(window)


class Player:
    def __init__(self, color, x, y, dir, size, speed):
        self.color = color
        self.speed = speed

        self.x = x
        self.y = y

        self.size = size
        self.wall = []

        self.dir = dir


    def move(self, dir):
        self.dir = dir

        speed = self.speed
        x = self.x
        y = self.y

        in_bounds = check_bounds(self, dir)
        if in_bounds:
            if dir == 4:
            # LEFT
                x -= speed
            elif dir == 6:
            # RIGHT
                x += speed
            elif dir == 8:
            # UP
                y -= speed
            elif dir == 2:
            # DOWN
                y += speed


    def render(self, renderer):
        color = self.color
        size = self.size

        x = self.x
        y = self.y
        w = x + size
        h = y + size

        renderer.fill((x, y, w, h), color)


def init_sdl():
    sdl2.ext.init()

    return renderer, window


def init_players(size, speed):
    players = []
    size = 10
    speed = 2

    green = Player(GREEN, 0, WIN_Y/2, 6, size, speed)
    red = Player(RED, WIN_X-size, WIN_Y/2, 4, size, speed)

    players.append(green)
    players.append(red)

    return players


def in_bounds(player, dir):
    speed = player.speed
    size = player.size
    x = player.x
    y = player.y

    if dir == 4:
        if x - speed < 0:
            return False
    elif dir == 6:
        if x + speed > WIN_X - size:
            return False
    elif dir == 8:
        if y - speed < 0:
            return False
    elif dir == 2:
        if y + speed > WIN_Y - size:
            return False

    return True


def render(renderer, players):
    # clear screen, then redraw
    renderer.clear(GRAY)
    pass


def analyze_event(events):
    # quit when sdl2.SDL_QUIT is the event.type
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            exit()
    pass


def


def update_end_vars(vars, events, players):
    if player.has_collided(players):
        vars[0] = True
    if analyze_event(events) == "usr_quit":
        vars[1] = True


screen = Screen(640, 480)

players = init_players(10, 2)

fatality = False
sdl_quit = False

# order matters
# 0: fatality, 1: sdl_quit
end_vars = [fatality, sdl_quit]

while not any(end_vars):
    events = sdl2.ext.get_events()

    update_end_vars(end_vars, events, players)

    analyze_event(events)

    render(renderer, players)
#window.show()












