# collin gros
# 2/25/19
# nano wars in python
import sdl2
import random


def print_cells(cells):
    for cell in cells:
        print(cell.hp)
        print(cell.radius)
        print(cell.owner)
        print()


def spot_taken(cells, our_cell):
# return 1 if x, y in our cell is inside another existing cell
    if len(cells) == 0:
        return 0

    for cell in cells:
        radius = cell.radius
        x = cell.x
        y = cell.y

        left = x - radius
        right = x + radius
        up = y - radius
        down = y + radius

        our_radius = our_cell.radius
        our_x = our_cell.x
        our_y = our_cell.y

        our_left = our_x - our_radius
        our_right = our_x + our_radius
        our_up = our_y - our_radius
        our_down = our_y + our_radius

        if ((our_left > left and our_left < right) or
            (our_right > left and our_right < right) or
            (our_up > up and our_up < down) or
            (our_down > up and our_down < down)):
            return 1

    return 0

def gen_map(width, height, num):
# generate neutral cells, given number of cells and map size
    cells = []
    for i in range(0, num):
        radius = random.randint(1, 5)
        x = random.randint(radius, width-radius)
        y = random.randint(radius, width-radius)

        cell = Cell(0, radius, "neutral", x, y)
        if spot_taken(cells, cell):
            continue

        cells.append(cell)

    return cells


def update_cells(cells):
    for cell in cells:
        cell.inc()


def get_rate(radius):
# radius range: 1 - 5
    rates = {1: 2,
             2: 4,
             3: 8,
             4: 16,
             5: 32}
    rate = rates[radius]

    return rate


class Map:
    def __init__(self, width, height, num_cells):
        self.width = width
        self.height = height
        self.num_cells = num_cells
        self.cells = []


    def generate_map(self):
    # generate all cells used for the game, some will be converted to
    # ply cells at the start using generate_ply(num_plys)
        pass

    def generate_ply(self, num_plys):
    # change the owner to player colors of a cell of Map's cells
        colors = ["red", "blue", "green", "yellow"]
        my_cells = []
        # cells to assign to players as starter cells
        radius = random.randint(1, 5)
        for cell in self.cells:
            if cell.radius == radius:
            # each player starts with cell of same radius
                my_cells.append(cell)

        prev_i = []
        # so we don't give 2 players the same randomly selected cell
        for i in range(0, num_plys):
            color = colors[i]

            while True:
                rand_cell_i = random.randint(0, len(my_cells) - 1)
                if rand_cell_i in prev_i:
                    # pick new random cell, as this one is already taken
                    continue
                else:
                    prev_i.append(rand_cell_i)
                    break
            prev_i.append(rand_cell_i)

            cell = my_cells[rand_cell_i]


class Cell:
    def __init__(self, owner, x, y, radius):
        self.owner = owner
        self.x = x
        self.y = y
        self.radius = radius

    def inc(self):
        rate = get_rate(self.radius)
        self.hp += rate


map = gen_map(640, 480, 3)
plys = gen_cells(640, 480, map, 2)

last_tick = sdl2.SDL_GetTicks()
while True:
    tick = sdl2.SDL_GetTicks()
    if tick - last_tick <= 250:
        continue

    update_cells(cells)
    print_cells(cells)

    last_tick = tick
