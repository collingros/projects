''' This is my first attempt at a game in SDL2 and Python - the game is like
Tron.'''
import os
import sdl2.ext
# Responsible for gfx and events

dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ["PYSDL2_DLL_PATH"] = dir_path
# Need to set PYSDL2_DLL_PATH to the same directory as this file for the sdl2
# libraries to work
# declaring constants
WINDOW_X = 800
WINDOW_Y = 600
# Window resolution
REFRESH_TIME = 25
# time it takes to go to next step in ms
WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLACK = sdl2.ext.Color(0, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
PINK = sdl2.ext.Color(255, 105, 180)
BLUE = sdl2.ext.Color(0, 0, 255)
LIGHT_GREY = sdl2.ext.Color(211, 211, 211)
DARK_GREY = sdl2.ext.Color(105, 105, 105)

# Common color constants
BACKGROUND_COLOR = (128, 128, 128)
# The background color for the game
sdl2.ext.init()
# Initializes sdl2's functions
window = sdl2.ext.Window("PYTRON", size=(WINDOW_X, WINDOW_Y))
# Creating the window
window.show()
renderer = sdl2.ext.Renderer(window)
# defines the renderer so we can use it to draw stuff
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


class Menu(object):
    # contains the possible stages for the menu and flags for changing
    # the game state
    def __init__(self):
        self.should_render = True
        self.stage = "main"
        self.buttons = []
        start_button = Button(WINDOW_X // 2, WINDOW_Y // 2, BLACK)
        # creates a black button in the middle of the screen
        self.buttons.append(start_button)
        # list for buttons to be stored and accessed

    def draw_main_menu(self):
        # draws the menu when starting the game
        # buttons[0] is the start button
        self.buttons[0].render()
        # draws the button

    def draw_pause_menu(self):
        # draws the version of the menu when in-game
        pass


class Player(object):
    # The player class will represent the cars on the screen
    def __init__(self, color, wall_color, pos_x=0, pos_y=0, orientation=0, speed=2, size_x=10, size_y=10,):
        self.speed = speed
        self.color = color
        self.wall_color = wall_color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.orientation = orientation
        self.last_x = pos_x
        self.last_y = pos_y
        self.turned = False
        self.god = False
        self.god_time = (self.size_x / self.speed) * REFRESH_TIME
        self.wall_list = []
        self.dead = False

    def move_left(self):
        # all moving functions move the unit in each direction at the rate of
        # its speed
        self.orientation = LEFT
        if self.pos_x - self.speed >= 0:
            self.pos_x = self.pos_x - self.speed
        else:
            self.pos_x = 0
            self.dead = True

    def move_right(self):
        self.orientation = RIGHT
        if self.pos_x + self.size_x + self.speed <= WINDOW_X:  # bounds checks
            self.pos_x = self.pos_x + self.speed
        else:
            self.pos_x = WINDOW_X - self.size_x
            self.dead = True

    def move_up(self):
        self.orientation = UP
        if self.pos_y - self.speed >= 0:
            self.pos_y = self.pos_y - self.speed
        else:
            self.pos_y = 0
            self.dead = True

    def move_down(self):
        self.orientation = DOWN
        if self.pos_y + self.size_y + self.speed <= WINDOW_Y:  # bounds checks
            self.pos_y = self.pos_y + self.speed
        else:
            self.pos_y = WINDOW_Y - self.size_y
            self.dead = True

    def render(self):
        # tells the renderer to fill a square from its top left corner
        # (posx, posy) and its width of x and y
        # orientations: 0 for right, 1 for down, 2 for left, 3 for up
        if self.orientation == 0:
            renderer.fill((self.pos_x, self.pos_y, self.size_x, self.size_y), self.color)
        elif self.orientation == 1:
            renderer.fill((self.pos_x, self.pos_y, self.size_y, self.size_x), self.color)
        elif self.orientation == 2:
            renderer.fill((self.pos_x - self.size_x + self.size_y, self.pos_y, self.size_x, self.size_y), self.color)
        elif self.orientation == 3:
            renderer.fill((self.pos_x, self.pos_y - self.size_x + self.size_y, self.size_y, self.size_x), self.color)
        else:
            print("error: in render func, orientation not valid")

    def render_wall(self, menu):
    # renders wall and checks for any collisions
        if len(self.wall_list) > 0:
            for i in range(len(self.wall_list)):
                # iteration through every block that
                # a player has moved through
                wall_x = self.wall_list[i]["x"]
                wall_y = self.wall_list[i]["y"]
                wall_w = self.wall_list[i]["w"]
                wall_h = self.wall_list[i]["h"]
                wall_x2 = wall_w + wall_x
                wall_y2 = wall_h + wall_y
                self_x = self.pos_x
                self_y = self.pos_y
                self_x2 = self.pos_x + self.size_x
                self_y2 = self.pos_y + self.size_y
                renderer.fill((wall_x, wall_y, wall_w, wall_h), self.wall_color)
                if not self.god and self.chump(wall_x, wall_y, wall_x2, wall_y2):
                    print("COLLISION CHUMP")
                #print("bool check")
                #print("x check", self.pos_x >= wall_x and self.pos_x <= wall_x2 and not self.god)
                #print("y check", self.pos_y >= wall_y and self.pos_y <= wall_y2 and not self.god)
                collision = True
                if self.god or self_y > wall_y2:
                    #print("(y)box top: {} wall bottom: {}".format(self_y, wall_y2))
                    collision = False
                if self.god or self_y2 < wall_y:
                    #print("(y)box bottom: {} wall top: {}".format(self_y2, wall_y))
                    collision = False
                if self.god or self_x2 < wall_x:
                    #print("(x)box right: {} wall left: {}".format(self_x2, wall_x))
                    collision = False
                if self.god or self_x > wall_x2:
                    #print("(x)box left: {} wall right: {}".format(self_x, wall_x2))
                    collision = False
                if collision:
                    self.dead = True
                    print("COLLISION")
                    print("(y)box top: {} wall bottom: {}".format(self_y, wall_y2))
                    print("(y)box bottom: {} wall top: {}".format(self_y2, wall_y))
                    print("(x)box right: {} wall left: {}".format(self_x2, wall_x))
                    print("(x)box left: {} wall right: {}".format(self_x, wall_x2))
    def chump(self, wall_x, wall_y, wall_x2, wall_y2):
        leftA = self.pos_x
        rightA = self.pos_x + self.size_x
        topA = self.pos_y
        bottomA = self.pos_y + self.size_y
        leftB = wall_x
        rightB = wall_x2
        topB = wall_y
        bottomB = wall_y2

        if( bottomA <= topB ):
            return False
        if( topA >= bottomB ):
            return False
        if( rightA <= leftB ):
            return False
        if( leftA >= rightB ):
            return False
        return True

    def god_timer(self):
        if self.god_time <= 0:
            self.god = False
            self.god_time = (self.size_x / self.speed) * REFRESH_TIME
            print("god off: posx: {} posy: {}".format(self.pos_x, self.pos_y))
        else:
            self.god_time -= REFRESH_TIME
            self.god = True
            print("god on: posx: {} posy: {}".format(self.pos_x, self.pos_y))
            #print("p has godmode - time left: {}s".format(str(self.god_time / 1000)))


class Button(object):
    # creates a button on the screen for future options
    def __init__(self, pos_x, pos_y, color, width_x=100, width_y=30):
        self.width_x = width_x
        self.width_y = width_y
        self.pos_x = pos_x - width_x // 2
        # integer division by two so the button is centered on its given
        # position
        self.pos_y = pos_y - width_y // 2
        self.color = color
        self.color2 = sdl2.ext.Color(abs(self.color.r-255), abs(self.color.g-255), abs(self.color.b-255))
        # color2 is the inverse of color
        self.default_color = True

    def render(self):
        # draws the button on the screen
        renderer.fill((self.pos_x, self.pos_y, self.width_x, self.width_y), self.color)

    def invert_color(self):
        # changes the color to the inverse of self.color
        if not self.default_color:
            temp = self.color
            self.color = self.color2
            self.color2 = temp
            self.default_color = True
        else:
            temp = self.color
            self.color = self.color2
            self.color2 = temp
            self.default_color = False


def menu_event(event, menu):
    # takes in an event and checks if it should do anything with the menu
    if (event.type == sdl2.SDL_MOUSEBUTTONDOWN or event.type == sdl2.SDL_MOUSEBUTTONUP):
        # if the user clicked
        if event.button.button == sdl2.SDL_BUTTON_LEFT:
            # if the click was the left button
            mouse_x = event.button.x
            mouse_y = event.button.y
            if menu.stage == "main":
                button = menu.buttons[0]
                # button is the start button (buttons[0])
                if (mouse_x >= button.pos_x and mouse_x <= button.pos_x + button.width_x) and (mouse_y >= button.pos_y and mouse_y <= button.pos_y + button.width_y):
                    button.invert_color()
                    if event.type == sdl2.SDL_MOUSEBUTTONUP:
                        menu.should_render = False
                elif not button.default_color:
                    button.invert_color()

def build_players():
    playerlist = []
    playerlist.append(Player(WHITE, LIGHT_GREY, 0, WINDOW_Y // 2, 0))
    playerlist.append(Player(BLACK, DARK_GREY, WINDOW_X - 10, WINDOW_Y // 2, 2))
    return playerlist

def main():
    game_state = "game"
    # a variable for switching to different stages of the game
    menu = Menu()
    playerlist = build_players()
    game_running = True
    last_step = 0
    playerlist[0].speed = 2
    while game_running:
        if sdl2.SDL_GetTicks() - last_step >= REFRESH_TIME:
            # restriction on game update time
            renderer.clear(BACKGROUND_COLOR)
            # blank screen
            if menu.should_render:
                menu.draw_main_menu()
            else:
                p1 = playerlist[0]
                p2 = playerlist[1]
                if not p1.dead and not p2.dead:
                    print("")
                    #print("{0:.2f}s".format(sdl2.SDL_GetTicks() / 1000))
                    for p in playerlist:
                        print(p.turned)
                        if p.god:
                            p.god_timer()
                        if p.turned:
                            p.god = True
                        p.render_wall(menu)
                    keystatus = sdl2.SDL_GetKeyboardState(None)
                    p1.turned = False
                    p2.turned = False
                    if keystatus[sdl2.SDL_SCANCODE_W] and p1.orientation != DOWN:
                        # if a player wants to go up and is not going down
                        if p1.orientation != UP:
                            # or already going up
                            p1.turned = True
                            if p1.orientation == RIGHT:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                            elif p1.orientation == LEFT:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + 0, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                        p1.move_up()
                    elif keystatus[sdl2.SDL_SCANCODE_S] and p1.orientation != UP:
                        if p1.orientation != DOWN:
                            p1.turned = True
                            if p1.orientation == RIGHT:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                                
                            elif p1.orientation == LEFT:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + 0, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                        p1.move_down()
                        
                    elif keystatus[sdl2.SDL_SCANCODE_A] and p1.orientation != RIGHT:
                        if p1.orientation != LEFT:
                            p1.turned = True
                            if p1.orientation == DOWN:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                            elif p1.orientation == UP:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + 0})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                        p1.move_left()
                    elif keystatus[sdl2.SDL_SCANCODE_D] and p1.orientation != LEFT:
                        if p1.orientation != RIGHT:
                            p1.turned = True
                            if p1.orientation == DOWN:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + p1.size_y})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                            elif p1.orientation == UP:
                                p1.wall_list.append({"x":p1.last_x, "y":p1.last_y, "w":p1.pos_x - p1.last_x + p1.size_x, "h":p1.pos_y - p1.last_y + 0})
                                p1.last_x = p1.pos_x
                                p1.last_y = p1.pos_y
                        p1.move_right()
                    else:
                        # orientations: 0 for right, 1 for down, 2 for left,
                        # 3 for up
                        if p1.orientation == RIGHT:
                            p1.move_right()
                        elif p1.orientation == DOWN:
                            p1.move_down()
                        elif p1.orientation == LEFT:
                            p1.move_left()
                        elif p1.orientation == UP:
                            p1.move_up()
                    if keystatus[sdl2.SDL_SCANCODE_UP] and p2.orientation != DOWN:
                        if p2.orientation != UP:
                            p2.turned = True
                            if p2.orientation == RIGHT:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                            elif p2.orientation == LEFT:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + 0, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                        p2.move_up()
                    elif keystatus[sdl2.SDL_SCANCODE_DOWN] and p2.orientation != UP:
                        if p2.orientation != DOWN:
                            p2.turned = True
                            if p2.orientation == RIGHT:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                                
                            elif p2.orientation == LEFT:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + 0, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                        p2.move_down()
                        
                    elif keystatus[sdl2.SDL_SCANCODE_LEFT] and p2.orientation != RIGHT:
                        if p2.orientation != LEFT:
                            p2.turned = True
                            if p2.orientation == DOWN:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                            elif p2.orientation == UP:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + 0})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                        p2.move_left()
                    elif keystatus[sdl2.SDL_SCANCODE_RIGHT] and p2.orientation != LEFT:
                        if p2.orientation != RIGHT:
                            p2.turned = True
                            if p2.orientation == DOWN:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + p2.size_y})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                            elif p2.orientation == UP:
                                p2.wall_list.append({"x":p2.last_x, "y":p2.last_y, "w":p2.pos_x - p2.last_x + p2.size_x, "h":p2.pos_y - p2.last_y + 0})
                                p2.last_x = p2.pos_x
                                p2.last_y = p2.pos_y
                        p2.move_right()
                    else:
                        # orientations: 0 for right, 1 for down, 2 for left, 3 for up
                        if p2.orientation == RIGHT:
                            p2.move_right()
                        elif p2.orientation == DOWN:
                            p2.move_down()
                        elif p2.orientation == LEFT:
                            p2.move_left()
                        elif p2.orientation == UP:
                            p2.move_up()
                    p1.render()
                    p2.render()
                else:
                    menu.should_render = True
                    if p1.dead:
                        print("p1 has died. resetting...")
                    elif p2.dead:
                        print("p2 has died. resetting...")
                    playerlist = build_players()
            for event in sdl2.ext.get_events():
                # loops through all possible events
                if event.type == sdl2.SDL_QUIT:
                    # if the player wants to exit
                    game_running = False
                    break
                    # break so we dont waste time going through events
                    # after this one
                elif (event.type == sdl2.SDL_KEYDOWN and (event.key.keysym.sym == sdl2.SDLK_ESCAPE or event.key.keysym.sym == sdl2.SDLK_PAUSE)):
                        menu.should_render = not menu.should_render
                        button = menu.buttons[0]
                        if not button.default_color:
                            button.invert_color()
                elif menu.should_render:
                    # if the game is at the menu
                    menu_event(event, menu)
            renderer.present()
            window.refresh()
            last_step = sdl2.SDL_GetTicks()
    sdl2.ext.quit()

if __name__ == "__main__":
    main()

'''storage
if not p1.god and (p1.pos_x >= wall_x and p1.pos_x + p1.size_x <= wall_x2):
                                # p1.turned is the signal that the player has just
                                # turned and should not be killed from their own
                                # square.
                                if p1.pos_y >= wall_y and p1.pos_y + p1.size_y <= wall_y2:
                                    print("p1 dead")
                                    #menu.should_render = True
                                    
if self.orientation == RIGHT:
                    if not self.god and self.pos_x + self.size_x >= wall_x and self.pos_x + self.size_x <= wall_x2:
                        if self.pos_y >= wall_y and self.pos_y <= wall_y2:
                            self.dead = True
                elif self.orientation == LEFT:
                    if not self.god and self.pos_x >= wall_x and self.pos_x <= wall_x2:
                        if self.pos_y >= wall_y and self.pos_y <= wall_y2:
                            self.dead = True
                elif self.orientation == UP:
                    if not self.god and self.pos_x >= wall_x and self.pos_x <= wall_x2:
                        if self.pos_y >= wall_y and self.pos_y <= wall_y2:
                            self.dead = True
                elif self.orientation == DOWN:
                    if not self.god and self.pos_x + self.size_x >= wall_x and self.pos_x + self.size_x <= wall_x2:
                        if self.pos_y + self.size_y >= wall_y and self.pos_y + self.size_y <= wall_y2:
                            self.dead = True
'''