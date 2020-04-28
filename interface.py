import pygame
import backend

WIDTH = 600
HEIGHT = 600
FONT_SIZE = 35

pygame.init()
pygame.font.init()

colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (211, 211, 211),
    'easy': (0, 255, 0),
    'medium': (255, 255, 0),
    'hard': (26, 83, 255),
    'expert': (255, 0, 0),
    'selected': (102, 163, 255),
    'sub_selected': (200, 179, 255),
    'same_number': (255, 102, 102),
    'dark_gray': (47, 79, 79),
    'win': (0, 128, 0)
}

cells = {}


class Rectangle(pygame.Rect):

    def __init__(self, window, text, color, pos_x, pos_y, width, height, font_size=20):
        super(Rectangle, self).__init__(pos_x, pos_y, width, height)
        self.window = window
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.text = text
        self.color = color
        self.text_width, self.text_height = self.font.size(self.text)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self)
        self.window.blit(self.font.render(self.text, True, colors['black']), (self.centerx - self.text_width / 2,
                                                                              self.centery - self.text_height / 2))


class Cell:
    digit_font = 35
    font = pygame.font.SysFont('Arial', digit_font)
    candidates_font = pygame.font.SysFont('Arial', 9)
    input_font = pygame.font.SysFont('Arial', 20)

    def __init__(self, window, pos_x, pos_y, width, height, row, column):
        self.window = window
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.row = row
        self.column = column
        self.input_digit_candidates = ''
        self.input_value = ''
        self.color = backend.color[str(self.row) + str(self.column)]
        self.value = backend.grid[self.row][self.column]

    def draw(self):
        self.color = backend.color[str(self.row) + str(self.column)]
        self.value = backend.grid[self.row][self.column]
        pygame.draw.rect(self.window, self.color, (self.pos_x, self.pos_y, self.width, self.height))
        pygame.draw.rect(self.window, colors['gray'], (self.pos_x, self.pos_y+20, self.width, 1))

    def draw_text(self, candidates_state):
        if self.value != 0:
            self.window.blit(Cell.font.render(str(self.value), True, colors['black']),
                             (self.pos_x + Cell.digit_font / 2,
                              self.pos_y + Cell.digit_font / 20))
        elif candidates_state == colors['easy'] and self.value == 0:
            candidates = backend.get_possibilities(self.row, self.column, backend.grid)
            for candidate in candidates:
                if candidate < 4:
                    x = self.pos_x + candidate * 12
                    y = self.pos_y + 8
                elif candidate < 7:
                    x = self.pos_x + (candidate - 3) * 12
                    y = self.pos_y + 18
                else:
                    x = self.pos_x + (candidate - 6) * 12
                    y = self.pos_y + 28
                self.window.blit(Cell.candidates_font.render(f'{candidate}', True, colors['black']), (x, y))

    def draw_input_candidates_and_value(self):
        self.window.blit(Cell.candidates_font.render(f'{self.input_digit_candidates}', True, colors['dark_gray']),
                         (self.pos_x+2, self.pos_y+5))
        self.window.blit(Cell.input_font.render(f'{self.input_value}', True, colors['dark_gray']),
                         (self.pos_x + 10, self.pos_y + 25))


def same_number(row, col):
    value = backend.grid[row][col]
    if value == 0:
        return
    for i in range(9):
        for j in range(9):
            if i != row and j != col:
                if backend.grid[i][j] == value:
                    backend.color[str(i) + str(j)] = colors['same_number']


def click_action(x_cord, y_cord, difficulty, is_filled, blanks, candidates, selected_cell):
    if WIDTH / 2 + 63 + 75 > x_cord > WIDTH / 2 + 63 and \
            575 > y_cord > 555:
        if difficulty == colors['easy']:
            difficulty = colors['medium']
            blanks = 30
        elif difficulty == colors['medium']:
            difficulty = colors['hard']
            blanks = 45
        elif difficulty == colors['hard']:
            difficulty = colors['expert']
            blanks = 63
        else:
            difficulty = colors['easy']
            blanks = 15
    elif WIDTH // 2 - 50 + 100 > x_cord > WIDTH // 2 - 50 and 525 + 50 > \
            pygame.mouse.get_pos()[1] > 525:
        generate_new_grid(is_filled, blanks)
    elif WIDTH - 50 > x_cord > WIDTH - 150 and 575 > y_cord > 525:
        backend.grid = backend.grid_c
    elif 210 > x_cord > 160 and 575 > y_cord > 525:
        if candidates == colors['easy']:
            candidates = colors['expert']
        else:
            candidates = colors['easy']
    elif 57 < x_cord < 543 and 5 < y_cord < 492:
        try:
            for cell in cells.values():
                if cell.pos_x <= x_cord <= cell.pos_x + cell.width and \
                        cell.pos_y <= y_cord <= cell.pos_y + cell.height:
                    color_board(cell.row, cell.column)
                    selected_cell = str(cell.row) + str(cell.column)
        except TypeError:
            pass
    return difficulty, is_filled, blanks, candidates, selected_cell


def confirm_input(dic):
    for cell in dic.values():
        if cell.value == 0 and len(cell.input_value):
            if int(cell.input_value) == backend.grid_c[cell.row][cell.column]:
                backend.grid[cell.row][cell.column] = int(cell.input_value)
                backend.color[str(cell.row)+str(cell.column)] = colors['sub_selected']
                cell.input_value = ''
                cell.input_digit_candidates = ''
            else:
                backend.color[str(cell.row)+str(cell.column)] = colors['expert']


def input_action(dic, selected, char, y_pos):
    try:
        if char == 'del':
            dic[selected].input_digit_candidates = dic[selected].input_digit_candidates[:-1]
        else:
            if dic[selected].pos_y + 20 > y_pos:
                if dic[selected].value == 0 and len(dic[selected].input_digit_candidates) < 9 and \
                        char not in dic[selected].input_digit_candidates:
                    dic[selected].input_digit_candidates += str(char)
            else:
                if dic[selected].value == 0:
                    dic[selected].input_value = str(char)
    except ValueError:
        pass


def color_board(row, col):
    backend.color = {key: colors['white'] for key in backend.color}
    backend.color[str(row) + str(col)] = colors['selected']
    for c in range(9):
        if c != col:
            backend.color[str(row) + str(c)] = colors['sub_selected']
    for r in range(9):
        if r != row:
            backend.color[str(r) + str(col)] = colors['sub_selected']
    edge_x = (row // 3) * 3
    edge_y = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if i + edge_x != row and j + edge_y != col:
                backend.color[str(i + edge_x) + str(j + edge_y)] = colors['sub_selected']
    same_number(row, col)


def generate_new_grid(is_filled, blanks):
    backend.color = {key: colors['white'] for key in backend.color}
    for cell in cells.values():
        cell.input_digit_candidates = ''
        cell.input_value = ''
    backend.fill_grid(is_filled, backend.grid)
    draw_grid(True)
    backend.copy_grid()
    pygame.time.wait(300)
    backend.remove_digits(blanks)


def win():
    backend.color = {key: colors['white'] for key in backend.color}
    for cell in cells.values():
        backend.color[str(cell.row)+str(cell.column)] = colors['win']
        pygame.time.wait(20)
        draw_grid(True)
    draw_grid(True)


def create_grid(screen):
    padding_x, padding_y = 57, 5
    width = 50
    gap = 53
    for row in range(1, 10):
        for column in range(1, 10):
            cells.setdefault(str(row - 1) + str(column - 1),
                             Cell(screen, padding_x, padding_y, width, width, row - 1,
                                  column - 1))
            if column % 3 == 0:
                padding_x += 59
            else:
                padding_x += gap
        padding_x = 57
        if row % 3 == 0:
            padding_y += 58
        else:
            padding_y += gap


def draw_grid(candidates_state):
    for cell in cells.values():
        cell.draw()
        cell.draw_text(candidates_state)
        if candidates_state == colors['expert']:
            cell.draw_input_candidates_and_value()
    pygame.display.update()


def draw_buttons(screen, difficulty, candidates):
    generate_button = Rectangle(screen, 'Generate', colors['gray'], WIDTH / 2 - 50, 525, 100, 50)
    solve_button = Rectangle(screen, 'Solve', colors['gray'], WIDTH - 150, 525, 100, 50)
    difficulty_button = Rectangle(screen, 'Difficulty', colors['gray'], WIDTH / 2 + 63, 525, 75, 25, 15)
    difficulty_rect = Rectangle(screen, '', difficulty, WIDTH / 2 + 63, 555, 75, 20)
    candidates_button_1 = Rectangle(screen, 'Show', colors['gray'], 50, 525, 100, 25, 20)
    candidates_button_2 = Rectangle(screen, 'Candidates', colors['gray'], 50, 550, 100, 25, 20)
    candidates_rect = Rectangle(screen, '', candidates, 160, 525, 50, 50)
    generate_button.draw()
    solve_button.draw()
    difficulty_button.draw()
    difficulty_rect.draw()
    candidates_button_1.draw()
    candidates_button_2.draw()
    candidates_rect.draw()
    pygame.display.update()


def update(screen, dif, candidates):
    draw_grid(candidates)
    draw_buttons(screen, dif, candidates)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku Solver-Generator')
    screen.fill(colors['white'])
    clock = pygame.time.Clock()
    run = True
    is_filled = False
    pygame.draw.rect(screen, colors['black'], (50, 0, 500, 500))
    create_grid(screen)
    difficulty, blanks = colors['easy'], 15
    candidates = colors['expert']
    draw_buttons(screen, difficulty, candidates)
    selected_cell = ''
    generate_new_grid(is_filled, blanks)
    while run:
        update(screen, difficulty, candidates)
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                difficulty, is_filled, blanks, candidates, selected_cell = click_action(x, y, difficulty, is_filled,
                                                                                        blanks, candidates,
                                                                                        selected_cell)
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    character = chr(event.key)
                    input_action(cells, selected_cell, character, y)
                elif event.key == pygame.K_BACKSPACE:
                    input_action(cells, selected_cell, 'del')
                elif event.key == pygame.K_RETURN:
                    confirm_input(cells)

        if backend.grid_c == backend.grid:
            win()
        clock.tick(60)


main()
