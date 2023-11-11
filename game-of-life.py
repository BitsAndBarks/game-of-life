from termcolor import colored

cell_dead = 0  # default value of cell
cell_alive = 1


def set_cell_alive(grid, x, y):
    grid[y][x] = cell_alive  # swap x, y due to how python processes 2D arrays


def print_grid(grid):
    for row in grid:
        for char in row:
            if char == cell_alive:
                print('🟦', end=" ")  # alive cells with value 1
            else:
                print('⬜️', end=" ")  # dead cells with value 0
        print()  # new line after each row


while True:
    which_setup = input(
        "Press 'q' for quick, pre-defined setup or 'i' for individual "
        "configuration of grid and alive cells.\n")

    if which_setup not in ['q', 'i']:
        print("Invalid command.")
        continue

    # grid dimension
    if which_setup == 'q':
        width, height = 16, 14  # pre-defined values
    else:
        # request dimensions from user with error handling
        while True:
            # TODO? currently needs to re-enter a correct x-axis value if
            #  y-axis value throws error. Separation requires restructure.
            try:
                width = int(input('Dimension on x-axis:\n'))
                if not (width > 0):
                    raise ValueError()
                height = int(input('Dimension on y-axis:\n'))
                if not (height > 0):
                    raise ValueError()
                break  # break out of loop if _both_ inputs are valid
            except ValueError as v:
                print(colored(f"Invalid input. Please enter positive "
                              f"integers >= 1 for dimensions. {v}",
                              'red',
                              'on_yellow',
                              ['bold']))

    # creates the grid with the specified dimensions (either pre-defined or
    # own values)
    grid = [[cell_dead for _ in range(width)] for _ in range(height)]

    # glider placement
    if which_setup == 'q':
        print(colored('Quick setup...', 'grey', 'on_blue',
                      ['bold']))
        # top left glider
        set_cell_alive(grid, 3, 1)
        set_cell_alive(grid, 4, 2)
        set_cell_alive(grid, 5, 2)
        set_cell_alive(grid, 3, 3)
        set_cell_alive(grid, 4, 3)

        # bottom right glider
        set_cell_alive(grid, 10, 9)
        set_cell_alive(grid, 11, 10)
        set_cell_alive(grid, 12, 10)
        set_cell_alive(grid, 11, 11)
        set_cell_alive(grid, 12, 9)
        break

    else:
        print(colored('Initialising grid...', 'grey', 'on_blue', ['bold']))
        print('Place the glider on your grid.')
        while True:
            user_input = input(
                "Enter the cells which are alive as coordinates separated by a comma (e.g., 'x,y') or press 'n' to stop:\n").strip()
            if user_input == 'n':
                break

            try:
                x_str, y_str = user_input.split(',')
                x = int(x_str.strip())
                y = int(y_str.strip())

                if not (0 <= x < width) or not (0 <= y < height):
                    raise IndexError("Coordinate out of grid bounds. "
                                     "Value must be between 0 and "
                                     + str(width - 1) +
                                     " for x-coordinate and between 0 and "
                                     + str(height - 1) +
                                     " for y-coordinate.")

                set_cell_alive(grid, x, y)

            except ValueError:
                print(
                    "Invalid input format. Please enter coordinates as 'x,y'.")
            except IndexError as e:
                print(colored(f"Active cell not in range of grid. {e}",
                              'red', 'on_yellow', ['bold']))

    break

print_grid(grid)