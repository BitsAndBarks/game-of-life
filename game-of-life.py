# imports
from termcolor import colored
from time import sleep

# global variables
CELL_DEAD = 0  # default value of cell
CELL_ALIVE = 1
CELL_ACTIVE = 2  # marks the cell whose neighbours to check

# variables
cell_number = 1  # each cell gets a number, starting at 1 on (0,0)
num_cols = 0  # no. of cols represents x-coordinate; later: len(grid)
num_rows = 0  # no. of rows represents y-coordinate; later: len(grid[0])


# function definitions:

def set_cell_alive(grid, x, y):
    grid[y][x] = CELL_ALIVE  # swap x, y due to how python processes 2D arrays


def set_active_cell(grid, i, j, it_count):
    grid[i][j] = CELL_ACTIVE
    # it_count += 1


def cell_value_and_number(grid, y, x, cell_number):
    cell_value = grid[x][y]
    print(f"Value at ({y}, {x}): {cell_value}")  # (y, x) for proper view
    cell_number += 1
    print(f"Value in cell {cell_number}: {cell_value}")
    return cell_value, cell_number


# prints grid with active, alive and dead cells
def print_grid(grid):
    for row in grid:
        for char in row:
            if char == CELL_ALIVE:
                print('🟦', end=" ")  # alive cells with value 1
            elif char == CELL_ACTIVE:
                print('🟨', end=" ")
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
    print_grid(default_grid)


# board setup: grid and cells
while True:
    which_setup = input(
        "Press 'q' for quick, pre-defined setup or 'i' for individual configuration of grid and alive cells.\n")

    if which_setup not in ['q', 'i']:
        print("Invalid command.")
        continue

    if which_setup == 'q':
        default_setup()
        break
    else:
        # grid dimensions:
        while True:
            # TODO? currently needs to re-enter a correct x-axis value if y-axis value throws error. Separation
            #  requires restructure.
            try:
                setup_width = int(input('Dimension of x-axis:\n'))
                if not (setup_width > 0):
                    raise ValueError()
                setup_height = int(input('Dimension of y-axis:\n'))
                if not (setup_height > 0):
                    raise ValueError()
            except ValueError as v:
                print(colored(f"Invalid input. Please enter positive integers >= 1 for dimensions. {v}",
                              'red', 'on_yellow', ['bold']))

            print(colored('Initialising grid...', 'grey', 'on_blue', ['bold']))
            setup_grid = [[CELL_DEAD for _ in range(setup_width)] for _ in range(setup_height)]
            break  # breaks out of loop if input for coordinates is correct

        sleep(1)
        print('Place the glider on your grid.')
        # glider placement:
        while True:
            user_input = input("Enter the cells which are alive as coordinates separated by a comma (e.g., 'x,y') or "
                               "press 'n' to stop: ").strip()

            if user_input == 'n':
                break

            try:
                x_str, y_str = user_input.split(',')
                x = int(x_str.strip())
                y = int(y_str.strip())

                if not (0 <= x < setup_width) or not (0 <= y < setup_height):
                    raise IndexError("Coordinate out of grid bounds. Value must be between 0 and "
                                     + str(setup_width - 1) + " for x-coordinate and between 0 and "
                                     + str(setup_height - 1) + " for y-coordinate.")

                set_cell_alive(setup_grid, x, y)

            except ValueError:
                print(
                    "Invalid input format. Please enter coordinates as 'x,y'.")
            except IndexError as e:
                print(colored(f"Active cell not in range of grid. {e}",
                              'red', 'on_yellow', ['bold']))

        print_grid(setup_grid)
        break

print(colored('Setup done!', 'green', 'on_light_green', ['bold']))

