# collin gros
#
# tron game in python
# this version is going to be elitist
import sdl2.ext 


class Game:
    def __init__(self):
        self.consts = {
            "BLACK":(0, 0, 0),
            "GREEN":(0, 255, 0),
            "RED":(255, 0, 0),
            "P_SIZE":10,
            "P_SPEED":2
        }
        self.cvt_scan = {
            sdl2.SDL_SCANCODE_W:8, sdl2.SDL_SCANCODE_A:4,
            sdl2.SDL_SCANCODE_S:2, sdl2.SDL_SCANCODE_D:6,
            sdl2.SDL_SCANCODE_UP:8, sdl2.SDL_SCANCODE_LEFT:4,
            sdl2.SDL_SCANCODE_DOWN:2, sdl2.SDL_SCANCODE_RIGHT:6
        }
        self.controls = {
            "0":[sdl2.SDL_SCANCODE_W, sdl2.SDL_SCANCODE_A,
                 sdl2.SDL_SCANCODE_S, sdl2.SDL_SCANCODE_D],
            "1":[sdl2.SDL_SCANCODE_UP, sdl2.SDL_SCANCODE_LEFT,
                 sdl2.SDL_SCANCODE_DOWN, sdl2.SDL_SCANCODE_RIGHT]
        }

        BLACK = self.consts["BLACK"]
        self.screen = Screen(640, 480, BLACK)

        self.players = {}


    def init_players(self):
        # give players correct spawn locations, directions, and values
        center_y = int(self.screen.y / 2)

        GREEN = self.consts["GREEN"]
        RED = self.consts["RED"]
        P_SIZE = self.consts["P_SIZE"]
        P_SPEED = self.consts["P_SPEED"]

        p0 = Player(self.screen, GREEN, 0,
                    center_y, 6, P_SIZE, P_SPEED)
        p1 = Player(self.screen, RED, self.screen.x - P_SIZE,
                    center_y, 4, P_SIZE, P_SPEED)
        p0.add_wall()
        p1.add_wall()

        self.players["0"] = p0
        self.players["1"] = p1


    def move_players(self):
        for name, player in self.players.items():
            player.move()


    def analyze_events(self):
        # game should quit if sdl_Quit event is recognized
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                exit()


    def player_dead(self):
        # game should quit if true
        pass


    def update_keys(self):
        # update keyboard states
        key_status = sdl2.SDL_GetKeyboardState(None)

        for name, player in self.players.items():
            for control in self.controls[name]:
                if key_status[control]:
                    player.turn(self.cvt_scan[control])


    def render_all(self):
        self.screen.render_bkg()
        self.screen.render_players(self.players)

        self.screen.update()
         


class Screen:
    def __init__(self, x, y, bkg_color):
        sdl2.ext.init()

        self.x = x
        self.y = y
        self.bkg_color = bkg_color

        self.window = sdl2.ext.Window("PYTRON", size=(x, y))
        self.renderer = sdl2.ext.Renderer(self.window)

        self.window.show()


    def render_players(self, players):
        # render the players and their walls
        for name, player in players.items():
            player.render()
            for wall in player.walls:
                wall.render()


    def render_bkg(self):
        # render the background color
        self.renderer.clear(self.bkg_color)


    def update(self):
        self.renderer.present()
        self.window.refresh()


class Player:
    def __init__(self, screen, color, x, y, direct, size, speed):
        # dirs: 4 - left    6 - right   8 - up   2 - down
        self.screen = screen
        self.color = color

        self.x = x
        self.y = y

        self.direct = direct
        self.size = size
        self.speed = speed

        self.walls = []


    def move(self):
        # move the player in direction
        if self.in_bounds():
            if self.direct == 4:
                self.x -= self.speed
            elif self.direct == 6:
                self.x += self.speed
            elif self.direct == 8:
                self.y -= self.speed
            elif self.direct == 2:
                self.y += self.speed

            self.walls[-1].extend()


    def turn(self, new_direct):
        # change players direction if they arent already moving in the
        # same direction they want to move in
        if new_direct == 4 and self.direct == 6:
            return
        elif new_direct == 6 and self.direct == 4:
            return
        elif new_direct == 8 and self.direct == 2:
            return
        elif new_direct == 2 and self.direct == 8:
            return

        self.direct = new_direct
        self.add_wall()


    def in_bounds(self):
        if self.direct == 4:
            if self.x - self.speed < 0:
                return False
        elif self.direct == 6:
            if self.x + self.speed > self.screen.x - self.size:
                return False
        elif self.direct == 8:
            if self.y - self.speed < 0:
                return False
        elif self.direct == 2:
            if self.y + self.speed > self.screen.y - self.size:
                return False

        return True


    def add_wall(self):
        new_wall = Wall(self.screen, self)
        self.walls.append(new_wall)


    def render(self):
        self.screen.renderer.fill((self.x, self.y, self.size, self.size),
                                   self.color)


class Wall:
    def __init__(self, screen, player):
        self.screen = screen

        self.player = player
        self.direct = player.direct
        self.w = player.size
        self.h = player.size

        if self.direct == 4:
            self.x = self.player.x + self.player.size
            self.y = self.player.y
        elif self.direct == 6:
            self.x = self.player.x - self.w
            self.y = self.player.y
        elif self.direct == 8:
            self.y = self.player.y + self.player.size
            self.x = self.player.x
        elif self.direct == 2:
            self.y = self.player.y - self.w
            self.x = self.player.x

        self.old_x = self.x

    def extend(self):
        # pencil paper
        if self.direct == 4:
            self.w = self.x - self.old_x
            self.x = self.player.x + self.player.size
        elif self.direct == 6:
            self.w += self.player.speed
        elif self.direct == 8:
            self.h -= self.player.speed
        elif self.direct == 2:
            self.h += self.player.speed


    def render(self):
        if self.direct == 4 or self.direct == 6:
            self.screen.renderer.fill((self.x, self.y, self.w,
                                       self.h), self.player.color)
        elif self.direct == 8 or self.direct == 2:
            self.screen.renderer.fill((self.x, self.y, self.h,
                                       self.w), self.player.color)


game = Game()

game.init_players()

REFRESH = 20
last_step = 0
while True:
    if sdl2.SDL_GetTicks() - last_step >= REFRESH:
        game.analyze_events()

        game.update_keys()
        game.move_players()

        game.render_all()

        last_step = sdl2.SDL_GetTicks()
    else:
        pass

    
    
















