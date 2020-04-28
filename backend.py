import copy
from numpy import random as np

is_filled = False
grid_c = None

grid = [[0 for _ in range(9)] for _ in range(9)]
color = {f"{i:02}": (255, 255, 255) for i in range(89)}
input_available = {f"{i:02}": True for i in range(89)}


def copy_grid():
    global grid_c
    grid_c = copy.deepcopy(grid)


def is_empty_place(board):
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return row, column, True
    return 0, 0, False


def is_possible_to_enter(x, y, value, board):
    for row in range(9):
        if board[row][y] == value:
            return False
    for col in range(9):
        if board[x][col] == value:
            return False
    edge_x = (x // 3) * 3
    edge_y = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[i + edge_x][j + edge_y] == value:
                return False
    return True


def solver(board):
    row, col, state = is_empty_place(board)
    if not state:
        return True
    for val in range(1, 10):
        if is_possible_to_enter(row, col, val, board):
            board[row][col] = val
            if solver(board):
                return True
            board[row][col] = 0
    return False


def clear():
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0


def fill_grid(is_fil, board):
    if not is_fil:
        clear()
        is_fil = True
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                np.shuffle(num_list)
                for value in num_list:
                    if is_possible_to_enter(row, col, value, board):
                        board[row][col] = value
                        board_copy = copy.deepcopy(board)
                        if solver(board_copy):
                            fill_grid(is_fil, board)
                        else:
                            board[row][col] = 0

                return False


def remove_digits(attemps):
    while attemps:
        x = np.randint(0, 9)
        y = np.randint(0, 9)
        if grid[x][y] != 0:
            value = grid[x][y]
            grid[x][y] = 0
            board_copy = copy.deepcopy(grid)
            if solver(board_copy):
                attemps -= 1
            else:
                grid[x][y] = value


def count_zero():
    number_of_zero = 0
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                number_of_zero += 1

    return number_of_zero


def get_possibilities(row, col, board):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if board[row][col] == 0:
        for y in range(9):
            if board[row][y] in digits:
                digits.remove(board[row][y])
        for x in range(9):
            if board[x][col] in digits:
                digits.remove(board[x][col])
        sq_x = (row // 3) * 3
        sq_y = (col // 3) * 3
        for x in range(3):
            for y in range(3):
                if board[x + sq_x][y + sq_y] in digits:
                    digits.remove(board[x + sq_x][y + sq_y])
        return digits


