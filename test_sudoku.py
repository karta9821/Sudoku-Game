import unittest

import pygame

import backend
import interface


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def test_empty_place(self):
        self.assertEqual(backend.is_empty_place(self.grid), (0, 0, True))

        self.grid = [[0 if x // 5 == 1 else 1 for x in range(9)] for _ in range(9)]
        self.assertEqual(backend.is_empty_place(self.grid), (0, 5, True))

        self.grid = [[1 for _ in range(9)] for _ in range(9)]
        self.assertEqual(backend.is_empty_place(self.grid), (0, 0, False))

    def test_is_possible_to_enter(self):
        self.assertEqual(backend.is_possible_to_enter(0, 0, 1, self.grid), True)

        self.grid[0][0] = 1
        self.assertEqual(backend.is_possible_to_enter(0, 0, 1, self.grid), False)

        self.grid = [[x + 1 if _ < 1 else 0 for x in range(9)] for _ in range(9)]
        self.assertEqual(backend.is_possible_to_enter(0, 0, 5, self.grid), False)
        self.assertEqual(backend.is_possible_to_enter(1, 0, 5, self.grid), True)

        self.grid = [[_ + 1 if x == 5 and _ > 0 else 0 for x in range(9)] for _ in range(9)]
        self.assertEqual(backend.is_possible_to_enter(0, 5, 1, self.grid), True)
        self.assertEqual(backend.is_possible_to_enter(0, 5, 5, self.grid), False)

        value = 1
        for x in range(3):
            for y in range(3):
                if value == 5:
                    value += 1
                    continue
                self.grid[x][y] = value
                value += 1
        self.assertEqual(backend.is_possible_to_enter(0, 2, 1, self.grid), False)
        self.assertEqual(backend.is_possible_to_enter(1, 1, 5, self.grid), True)
        self.assertEqual(backend.is_possible_to_enter(1, 1, 3, self.grid), False)

    def test_get_possibilities(self):
        self.assertEqual(backend.get_possibilities(5, 5, self.grid), [1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.grid[5][5] = 5
        self.assertEqual(backend.get_possibilities(5, 5, self.grid), None)

        value = 1
        for x in range(3):
            for y in range(3):
                if value == 5:
                    value += 1
                    continue
                self.grid[x][y] = value
                value += 1
        self.assertEqual(backend.get_possibilities(1, 1, self.grid), [5])

        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        for col in range(9):
            if 7 > col > 3:
                self.grid[0][col] = col + 1
        self.assertEqual(backend.get_possibilities(0, 0, self.grid), [1, 2, 3, 4, 8, 9])

        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        for col in range(9):
            if 7 > col > 3:
                self.grid[col][0] = col + 1
        self.assertEqual(backend.get_possibilities(0, 0, self.grid), [1, 2, 3, 4, 8, 9])

    def test_solver(self):
        self.assertEqual(backend.solver(self.grid), True)

        self.grid = [[_ if y < 2 else 0 for _ in range(9)] for y in range(9)]
        self.assertEqual(backend.solver(self.grid), False)

    def test_fill_grid(self):
        self.assertEqual(backend.fill_grid(False, self.grid), False)


class TestCell(unittest.TestCase):
    def setUp(self):
        screen = pygame.display.set_mode((0, 0))
        self.cells = {}
        padding_x, padding_y = 57, 5
        width = 50
        gap = 53
        for row in range(1, 10):
            for column in range(1, 10):
                self.cells.setdefault(str(row - 1) + str(column - 1),
                                      interface.Cell(screen, padding_x, padding_y, width, width, row - 1,
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

    def test_same_color(self):
        backend.grid = [[1 for _ in range(9)] for _ in range(9)]
        [[interface.same_number(row, col) for row in range(9)] for col in range(9)]
        self.assertEqual(backend.color['00'], interface.colors['same_number'])
        self.assertEqual(backend.color['88'], interface.colors['same_number'])

    def test_input_action(self):
        self.cells['00'].input_digit_candidates = '123456789'
        interface.input_action(self.cells, '00', 'del', 0)
        self.assertEqual(self.cells['00'].input_digit_candidates, '12345678')

        self.cells['00'].input_digit_candidates = ''
        interface.input_action(self.cells, '00', 'del', 0)
        self.assertEqual(self.cells['00'].input_digit_candidates, '')

        self.cells['00'].input_digit_candidates = '123456789'
        interface.input_action(self.cells, '00', '9', 3)
        self.assertEqual(self.cells['00'].input_digit_candidates, '123456789')

        self.cells['00'].value = 0
        self.cells['00'].input_digit_candidates = '1234'
        interface.input_action(self.cells, '00', '7', self.cells['00'].pos_y+5)
        self.assertEqual(self.cells['00'].input_digit_candidates, '12347')

        interface.input_action(self.cells, '00', '7', self.cells['00'].pos_y+22)
        self.assertEqual(self.cells['00'].input_value, '7')

        self.cells['00'].value = 1
        self.cells['00'].input_value = '8'
        interface.input_action(self.cells, '00', '1', self.cells['00'].pos_y+22)
        self.assertEqual(self.cells['00'].input_value, '8')


if __name__ == '__main__':
    unittest.main()
