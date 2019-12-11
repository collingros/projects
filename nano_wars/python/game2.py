# nano wars
#
# collin gros
# 3/8/19
#
import random
import sdl2.ext


def draw_square(renderer, coords, radius, color):
# draw square
    x0 = coords[0]
    y0 = coords[1]

    x = radius - 1
    y = 0

    dx = 1
    dy = 1
    err = dx - (radius * 2)

    while x >= y:
        renderer.fill((x0, y0, radius, radius), color)

        if err <= 0:
            y += 1
            err += dy
            dy += 2
        elif err > 0:
            x -= 1
            dx += 2
            err += dx - (radius * 2)


def draw_circle(renderer, coords, radius, color, t):
# draw circle using midpoint algorithm (wikipedia)
# t = thickness (messes with bounds)
    x0 = coords[0]
    y0 = coords[1]

    x = radius - 1
    y = 0

    dx = 1
    dy = 1
    err = dx - (radius * 2)

    while x >= y:
        renderer.fill((x0 + x, y0 + y, t, t), color)
        renderer.fill((x0 + y, y0 + x, t, t), color)
        renderer.fill((x0 - y, y0 + x, t, t), color)
        renderer.fill((x0 - x, y0 + y, t, t), color)
        renderer.fill((x0 - x, y0 - y, t, t), color)
        renderer.fill((x0 - y, y0 - x, t, t), color)
        renderer.fill((x0 + y, y0 - x, t, t), color)
        renderer.fill((x0 + x, y0 - y, t, t), color)

        if err <= 0:
            y += 1
            err += dy
            dy += 2
        elif err > 0:
            x -= 1
            dx += 2
            err += dx - (radius * 2)


def get_rate(max):
# return rate to grow a cell dependent on radius
    return 1


def get_color(str):
# return a 3-tuple (R,G,B) of a corresponding color to str
    if str == "neutral":
        return (128, 128, 128)
    elif str == "red":
        return (255, 0, 0)
    elif str == "green":
        return (0, 255, 0)
    elif str == "blue":
        return (0, 0, 255)
    else:
        return (255, 255, 255)


def collision(l1, r1, u1, d1, l2, r2, u2, d2):
# 1 if there is a collision in the *RECTANGLE*
# defined by these borders
    if (l1 < r2 and r1 > l2 and
        u1 < d2 and d1 > u2):
        return 1

    return 0


def not_taken(radius, coords, cells):
# 1 if spot defined by (coords[0], coords[1]) is
# available
    my_x = coords[0]
    my_y = coords[1]
    my_r = radius

    my_left = my_x - my_r
    my_right = my_x + my_r
    my_up = my_y - my_r
    my_down = my_y + my_r

    for cell in cells:
        x = cell.coords[0]
        y = cell.coords[1]
        r = cell.radius_max

        left = x - r
        right = x + r
        up = y - r
        down = y + r

        if collision(my_left, my_right, my_up, my_down,
                     left, right, up, down):
            return 0

    return 1


class Map:
    def __init__(self, width, height, size, radius_min, radius_max, ply_c):
        self.width = width
        self.height = height
        self.size = size
        self.radius_min = radius_min
        self.radius_max = radius_max
        self.ply_c = ply_c
        # player count, cant exceed 3, (need to add more colors)

        self.players = []

        self.init_sdl()
        self.init_cells()
        self.init_players()

        self.window.show()


    def grow(self):
    # grow all cells, according to radius
        for cell in self.cells:
            rate = get_rate(cell.radius_max)

            sum = cell.radius + rate
            if sum == cell.radius_max:
                continue
            elif sum > cell.radius_max:
                cell.radius = cell.radius_max
                continue

            cell.radius += rate


    def render(self):
    # draw the map
        self.renderer.clear((0, 0, 0))

        self.draw_cells()

        self.renderer.present()
        self.window.refresh()


    def draw_cells(self):
    # draw all cells
        for cell in self.cells:
            color = get_color(cell.owner)

#            draw_square(self.renderer, cell.coords,
#                        cell.radius, color)
            draw_circle(self.renderer, cell.coords,
                        cell.radius, color, 1)


    def init_players(self):
    # pick player cells from all cells and assign to self.players[]
        count = 0
        history = []
        while True:
            if count == self.ply_c:
                break

            rand = random.randint(0, len(self.cells) - 1)
            if rand in history:
                continue

            history.append(rand)
            count += 1

        for i in history:
            cur_cell = self.cells[i]
            self.players.append(cur_cell)


        colors = ["red", "green", "blue"]
        # same as in get_color()
        count = 0
        for i in range(0, self.ply_c):
            player = self.players[i]
            color = colors[i]
            player.owner = color


    def init_sdl(self):
    # init window and renderer
        sdl2.ext.init()

        self.window = sdl2.ext.Window("NANO WARS", size=(self.width, self.height))
        self.renderer = sdl2.ext.Renderer(self.window)


    def init_cells(self):
    # return arr of cell objects defining the map
        self.cells = []
        for i in range(0, self.size):
            radius = 0
            coords = []
            while True:
                coords = []
                radius = random.randint(self.radius_min, self.radius_max)

                border = self.width - self.radius_max
                x = random.randint(self.radius_max, border)
                coords.append(x)

                border = self.height - self.radius_max
                y = random.randint(self.radius_max, border)
                coords.append(y)

                if not_taken(radius, coords, self.cells):
                    break

            my_cell = Cell(radius, coords, "neutral")
            self.cells.append(my_cell)


class Cell:
    def __init__(self, radius, coords, owner):
        self.radius = 1
        self.radius_max = radius

        self.coords = coords
        self.owner = owner


map = Map(640, 480, 20, 10, 50, 3)
#        (width, height, size, radius_min, radius_max, ply_c)
last_tick = 0
while True:
    tick = sdl2.SDL_GetTicks()
    print(tick - last_tick)
#    if tick - last_tick < 250:
#        continue

    map.grow()
    map.render()

    last_tick = sdl2.SDL_GetTicks()
