# imports
from termcolor import colored
from time import sleep

# constants
CELL_DEAD = 0  # default value of cell
CELL_ALIVE = 1
NEIGHBOURS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),  # offset of 8 surrounding cells of currently active cell
              (1, -1), (1, 0), (1, 1)]


# function definitions:
def set_cell_alive(grid, x, y):
    grid[y][x] = CELL_ALIVE  # swap x, y due to how python processes 2D arrays


# prints grid with active, alive and dead cells
def print_grid(grid):
    for row in grid:
        for char in row:
            if char == CELL_ALIVE:
                print('🟦', end=" ")  # alive cells with value 1
            else:
                print('⬜️', end=" ")  # dead cells with value 0
        print()  # new line after each row


# default grid with two gliders:
def default_setup():
    default_width = 16
    default_height = 14
    default_grid = [[CELL_DEAD for _ in range(default_width)]
                    for _ in range(default_height)]
    alive_cells = [(1, 3), (2, 4), (2, 5), (3, 3), (3, 4),  # top left glider
                   (9, 10), (10, 11), (10, 12), (11, 11), (9, 12)  # bottom right glider
                   ]
    for row, col in alive_cells:
        default_grid[row][col] = CELL_ALIVE

    print(colored('Quick setup...', 'grey', 'on_blue', ['bold']))
    sleep(1)
    return default_grid


# user specifies width and height of grid and which cells start as alive cells
def individual_setup():
    setup_width, setup_height = get_grid_dimensions()
    setup_grid = [[CELL_DEAD for _ in range(setup_width)] for _ in range(setup_height)]

    print(colored('Initialising grid...', 'grey', 'on_blue', ['bold']))
    sleep(1)

    set_alive_cells(setup_grid, setup_width, setup_height)
    return setup_grid


# helper for grid dimension on individual setup
def get_grid_dimensions():
    while True:
        try:
            width = int(input('Dimension of x-axis:\n'))
            height = int(input('Dimension of y-axis:\n'))
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive integers.")
            return width, height
        except ValueError as e:
            print(colored(f"Invalid input. {e}", 'red', 'on_yellow', ['bold']))


# helper for alive cells on individual setup (allows any form or shape)
def set_alive_cells(grid, width, height):
    print('Place the glider on your grid.')
    while True:
        user_input = input("Enter alive cells as 'x,y' or press 'n' to stop: ").strip()
        if user_input == 'n':
            break

        try:
            x, y = parse_coordinates(user_input, width, height)
            set_cell_alive(grid, x, y)
        except (ValueError, IndexError) as e:
            print(colored(f"Invalid input. {e}", 'red', 'on_yellow', ['bold']))


# helper for parsing sole coordinates from user input
def parse_coordinates(input_str, max_x, max_y):
    x_str, y_str = input_str.split(',')
    x = int(x_str.strip())
    y = int(y_str.strip())
    if not (0 <= x < max_x) or not (0 <= y < max_y):
        raise IndexError("Coordinates out of bounds.")
    return x, y


# function to update the state of a cell based on its current state and the number of alive neighbours
def next_cell_state(grid, x, y, neighbours):
    alive_ngb_count = 0
    for dx, dy in neighbours:
        actual_ngb_x = (x + dx) % len(grid)
        actual_ngb_y = (y + dy) % len(grid[0])
        alive_ngb_count += grid[actual_ngb_x][actual_ngb_y] == CELL_ALIVE

    if grid[x][y] == CELL_ALIVE and (alive_ngb_count < 2 or alive_ngb_count > 3):
        return CELL_DEAD
    elif grid[x][y] == CELL_DEAD and alive_ngb_count == 3:
        return CELL_ALIVE
    return grid[x][y]


# separate function to apply updated cell state to every cell in the grid; creates a new grid!
def apply_rules_to_grid(grid):
    new_grid = [[CELL_DEAD for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            new_grid[x][y] = next_cell_state(grid, x, y, NEIGHBOURS)
    return new_grid


def main():
    which_setup = input("Press 'q' for quick setup or 'i' for individual configuration:\n").lower()
    current_grid = default_setup() if which_setup == 'q' else individual_setup()

    print_grid(current_grid)
    print(colored('Setup done!', 'green', 'on_light_green', ['bold']))

    # apply rules and update the grid
    for x in range(100):
        current_grid = apply_rules_to_grid(current_grid)
        print(f"----------iteration {x + 1}----------")
        print_grid(current_grid)


main()