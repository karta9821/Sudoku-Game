import copy
from numpy import random as np

is_filled = False


grid =[
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
]

grid_c = None


def copy_grid():
    global grid_c
    grid_c = copy.deepcopy(grid)


color = {'00': (255, 255, 255), '01': (255, 255, 255), '02': (255, 255, 255), '03': (255, 255, 255), '04': (255, 255, 255),
       '05': (255, 255, 255),
       '06': (255, 255, 255), '07': (255, 255, 255), '08': (255, 255, 255), '10': (255, 255, 255), '11': (255, 255, 255), '12': (255, 255, 255),
       '13': (255, 255, 255),
       '14': (255, 255, 255), '15': (255, 255, 255), '16': (255, 255, 255), '17': (255, 255, 255), '18': (255, 255, 255), '20': (255, 255, 255),
       '21': (255, 255, 255),
       '22': (255, 255, 255), '23': (255, 255, 255), '24': (255, 255, 255), '25': (255, 255, 255), '26': (255, 255, 255), '27': (255, 255, 255),
       '28': (255, 255, 255),
       '30': (255, 255, 255), '31': (255, 255, 255), '32': (255, 255, 255), '33': (255, 255, 255), '34': (255, 255, 255), '35': (255, 255, 255),
       '36': (255, 255, 255),
       '37': (255, 255, 255), '38': (255, 255, 255), '40': (255, 255, 255), '41': (255, 255, 255), '42': (255, 255, 255), '43': (255, 255, 255),
       '44': (255, 255, 255),
       '45': (255, 255, 255), '46': (255, 255, 255), '47': (255, 255, 255), '48': (255, 255, 255), '50': (255, 255, 255), '51': (255, 255, 255),
       '52': (255, 255, 255),
       '53': (255, 255, 255), '54': (255, 255, 255), '55': (255, 255, 255), '56': (255, 255, 255), '57': (255, 255, 255), '58': (255, 255, 255),
       '60': (255, 255, 255),
       '61': (255, 255, 255), '62': (255, 255, 255), '63': (255, 255, 255), '64': (255, 255, 255), '65': (255, 255, 255), '66': (255, 255, 255),
       '67': (255, 255, 255),
       '68': (255, 255, 255), '70': (255, 255, 255), '71': (255, 255, 255), '72': (255, 255, 255), '73': (255, 255, 255), '74': (255, 255, 255),
       '75': (255, 255, 255),
       '76': (255, 255, 255), '77': (255, 255, 255), '78': (255, 255, 255), '80': (255, 255, 255), '81': (255, 255, 255), '82': (255, 255, 255),
       '83': (255, 255, 255),
       '84': (255, 255, 255), '85': (255, 255, 255), '86': (255, 255, 255), '87': (255, 255, 255), '88': (255, 255, 255)
}

input_available = {'00': True, '01': True, '02': True, '03': True, '04': True, '05': True, '06': True, '07': True, '08': True,
    '10': True, '11': True, '12': True, '13': True, '14': True, '15': True, '16': True, '17': True, '18': True,
    '20': True, '21': True, '22': True, '23': True, '24': True, '25': True, '26': True, '27': True, '28': True,
    '30': True, '31': True, '32': True, '33': True, '34': True, '35': True, '36': True, '37': True, '38': True,
    '40': True, '41': True, '42': True, '43': True, '44': True, '45': True, '46': True, '47': True, '48': True,
    '50': True, '51': True, '52': True, '53': True, '54': True, '55': True, '56': True, '57': True, '58': True,
    '60': True, '61': True, '62': True, '63': True, '64': True, '65': True, '66': True, '67': True, '68': True,
    '70': True, '71': True, '72': True, '73': True, '74': True, '75': True, '76': True, '77': True, '78': True,
    '80': True, '81': True, '82': True, '83': True, '84': True, '85': True, '86': True, '87': True, '88': True
}







def is_empty(board):
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
    edge_x = (x//3) * 3
    edge_y = (y//3) * 3
    for i in range(3):
        for j in range(3):
            if board[i+edge_x][j+edge_y] == value:
                return False
    return True


def solver(board):
    row, col, state = is_empty(board)
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


def fill_grid(is_fil):
    if not is_fil:
        clear()
        is_fil = True
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                np.shuffle(num_list)
                for value in num_list:
                    if is_possible_to_enter(row, col, value, grid):
                        grid[row][col] = value
                        board_copy = copy.deepcopy(grid)
                        if solver(board_copy):
                            fill_grid(is_fil)
                        else:
                            grid[row][col] = 0

                return False


def remove_digits(attemps):
    while attemps != 0:
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


def get_possibilities(row, col):
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if grid[row][col] == 0:
        for y in range(9):
            if grid[row][y] in digits:
                digits.remove(grid[row][y])
        for x in range(9):
            if grid[x][col] in digits:
                digits.remove(grid[x][col])
        sq_x = (row//3) * 3
        sq_y = (col//3) * 3
        for x in range(3):
            for y in range(3):
                if grid[x + sq_x][y + sq_y] in digits:
                    digits.remove(grid[x + sq_x][y + sq_y])
    return digits


