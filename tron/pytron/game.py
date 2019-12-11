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
WHITE = sdl2.ext.Color(255, 255, 255)
RED = sdl2.ext.Color(255, 0, 0)
BLACK = sdl2.ext.Color(0, 0, 0)
GREEN = sdl2.ext.Color(0, 255, 0)
PINK = sdl2.ext.Color(255, 105, 180)
BLUE = sdl2.ext.Color(0, 0, 255)
# Common color constants
BACKGROUND_COLOR = (255, 0, 0)
# The background color for the game
sdl2.ext.init()
# Initializes sdl2's functions
window = sdl2.ext.Window("PYTRON", size=(WINDOW_X, WINDOW_Y))
# Creating the window
window.show()
renderer = sdl2.ext.Renderer(window)
# defines the renderer so we can use it to draw stuff
 
 
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
    def __init__(self, color, pos_x=0, pos_y=0, orientation=0, speed=2, size_x=10, size_y=10,):
        self.speed = speed
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.orientation = orientation
        self.last_x = pos_x
        self.last_y = pos_y
        # orientations: 0 for right, 1 for down, 2 for left, 3 for up

    def move_left(self):
        # all moving functions move the unit in each direction at the rate of
        # its speed
        # sees if the new position will exceed the left of the window
        self.orientation = 2
        if self.pos_x - self.speed >= 0:
            self.pos_x = self.pos_x - self.speed
        else:
            self.pos_x = 0
 
    def move_right(self):
        # sees if the new position will exceed the right of the window
        self.orientation = 0
        if self.pos_x + self.size_x + self.speed <= WINDOW_X:
            self.pos_x = self.pos_x + self.speed
        else:
            self.pos_x = WINDOW_X - self.size_x
 
    def move_up(self):
        # sees if the new position will exceed the top of the window
        self.orientation = 3
        if self.pos_y - self.speed >= 0:
            self.pos_y = self.pos_y - self.speed
        else:
            self.pos_y = 0
 
    def move_down(self):
        # sees if the new position will exceed the top of the window
        self.orientation = 1
        if self.pos_y + self.size_y + self.speed <= WINDOW_Y:
            self.pos_y = self.pos_y + self.speed
        else:
            self.pos_y = WINDOW_Y - self.size_y
 
    def render(self):
        # tells the renderer to fill a square from its top left corner
        # (posx, posy) and it's width of x and y
        # orientations: 0 for right, 1 for down, 2 for left, 3 for up
        if self.orientation == 0:
            renderer.fill((self.pos_x, self.pos_y,
                       self.size_x, self.size_y), self.color)
        elif self.orientation == 1:
            renderer.fill((self.pos_x, self.pos_y,
                       self.size_y, self.size_x), self.color)
        elif self.orientation == 2:
            renderer.fill((self.pos_x - self.size_x + self.size_y, self.pos_y,
                       self.size_x, self.size_y), self.color)
        elif self.orientation == 3:
            renderer.fill((self.pos_x, self.pos_y - self.size_x + self.size_y,
                       self.size_y, self.size_x), self.color)
        else:
            print("error: in render func, orientation not valid")
 
 
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
        self.color2 = sdl2.ext.Color(abs(self.color.r-255),
                       abs(self.color.g-255),
                       abs(self.color.b-255))
        # color2 is the inverse of color
        self.default_color = True
 
    def render(self):
        # draws the button on the screen
        renderer.fill((self.pos_x, self.pos_y,
                       self.width_x, self.width_y), self.color)
 
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
 
 
def menu_event(event, menu):\
    # takes in an event and checks if it should do anything with the menu
    if event.type == sdl2.SDL_MOUSEBUTTONDOWN or event.type == sdl2.SDL_MOUSEBUTTONUP:
        # if the user clicked
        if event.button.button == sdl2.SDL_BUTTON_LEFT:
            # if the click was the left button
            mouse_x = event.button.x
            mouse_y = event.button.y
            if menu.stage == "main":
                button = menu.buttons[0]
                # button is the start button (buttons[0])
                if (mouse_x >= button.pos_x and mouse_x <= button.pos_x +
                        button.width_x) and (mouse_y >= button.pos_y and
                        mouse_y <= button.pos_y + button.width_y):
                    button.invert_color()
                    if event.type == sdl2.SDL_MOUSEBUTTONUP:
                        menu.should_render = False
                elif not button.default_color:
                    button.invert_color()
 
def main():
    game_state = "game"
    # a variable for switching to different stages of the game
    menu = Menu()
    p1 = Player(GREEN, 0, WINDOW_Y // 2, 0)
    p2 = Player(BLUE, WINDOW_X, WINDOW_Y // 2, 2)
    game_running = True
    last_step = 0
    laser_wall = []
    while game_running:
        if sdl2.SDL_GetTicks() - last_step >= 25:
            renderer.clear(WHITE)
            if len(laser_wall) > 0:
                #renderer.fill((laser_wall[0][0][0], laser_wall[0][0][1], laser_wall[0][1][0], laser_wall[0][1][1]), BLACK)
                for i in range(len(laser_wall)):
                    renderer.fill((laser_wall[i][0][0], laser_wall[i][0][1], laser_wall[i][1][0], laser_wall[i][1][1]), BLACK)
            # makes the window blank
            if menu.should_render:
                menu.draw_main_menu()
            elif game_state == "game":
                keystatus = sdl2.SDL_GetKeyboardState(None)
                if keystatus[sdl2.SDL_SCANCODE_W]:
                    if p1.orientation != 3:
                        laser_wall.append([[p1.last_x, p1.pos_y + p1.size_y], [p1.pos_x - p1.last_x + p1.size_x, p1.last_y - p1.pos_y - + p1.size_y]])
                    p1.last_x = p1.pos_x
                    p1.last_y = p1.pos_y
                    p1.move_up()
                elif keystatus[sdl2.SDL_SCANCODE_S]:
                    if p1.orientation != 1:
                        #print(laser_wall)
                        laser_wall.append([[p1.last_x, p1.last_y], [p1.pos_x - p1.last_x + p1.size_x, p1.pos_y - p1.last_y + p1.size_y]])
                    p1.last_x = p1.pos_x
                    p1.last_y = p1.pos_y
                    p1.move_down()
                elif keystatus[sdl2.SDL_SCANCODE_A]:
                    if p1.orientation != 2:
                        laser_wall.append([[p1.last_x, p1.last_y], [p1.pos_x - p1.last_x + p1.size_x, p1.pos_y - p1.last_y + p1.size_y]])
                    p1.last_x = p1.pos_x
                    p1.last_y = p1.pos_y
                    p1.move_left()
                elif keystatus[sdl2.SDL_SCANCODE_D]:
                    if p1.orientation != 2:
                        laser_wall.append([[p1.last_x, p1.last_y], [p1.pos_x - p1.last_x + p1.size_x, p1.pos_y - p1.last_y + p1.size_y]])
                    p1.last_x = p1.pos_x
                    p1.last_y = p1.pos_y
                    p1.move_right()
                else:
                    # orientations: 0 for right, 1 for down, 2 for left, 
                    # 3 for up
                    if p1.orientation == 0:
                        p1.move_right()
                    elif p1.orientation == 1:
                        p1.move_down()
                    elif p1.orientation == 2:
                        p1.move_left()
                    elif p1.orientation == 3:
                        p1.move_up()
                if keystatus[sdl2.SDL_SCANCODE_UP]:
                    p2.move_up()
                elif keystatus[sdl2.SDL_SCANCODE_DOWN]:
                    p2.move_down()
                elif keystatus[sdl2.SDL_SCANCODE_LEFT]:
                    p2.move_left()
                elif keystatus[sdl2.SDL_SCANCODE_RIGHT]:
                    p2.move_right()
                else:
                    # orientations: 0 for right, 1 for down, 2 for left, 3 for up
                    if p2.orientation == 0:
                        p2.move_right()
                    elif p2.orientation == 1:
                        p2.move_down()
                    elif p2.orientation == 2:
                        p2.move_left()
                    elif p2.orientation == 3:
                        p2.move_up()
                p1.render()
                p2.render()
            elif game_state == "end":
                pass
            for event in sdl2.ext.get_events():
                # loops through all possible events
                if event.type == sdl2.SDL_QUIT:
                    # if the player wants to exit
                    game_running = False
                    break
                    # break so we dont waste time going through events
                    # after this one
                elif (event.type == sdl2.SDL_KEYDOWN and
                    (event.key.keysym.sym == sdl2.SDLK_ESCAPE or
                        event.key.keysym.sym == sdl2.SDLK_PAUSE)):
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