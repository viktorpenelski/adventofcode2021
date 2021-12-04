from unittest import TestCase

from day4.solution import Board


class TestBoard(TestCase):

    def test_single_board_creation(self):
        lines = [
            "14 21 17 24  4",
            "18  8 23 26 20",
            "22 11 13  6  5",
            "22 11 13  6  5",
            "2  0 12  3  7",
        ]
        board = Board.from_raw(lines)
        self.assertEqual(5, len(board.numbers))
        for line in board.numbers:
            self.assertEqual(5, len(line))
        self.assertEqual(14, board.numbers[0][0])
        self.assertEqual(20, board.numbers[1][4])
        self.assertEqual(7, board.numbers[4][4])

    def test_bingo_visit_row(self):
        lines = [
            "14 21 17 24  4",
            "10 16 15  9 19",
            "18  8 23 26 20",
            "22 11 13  6  5",
            "2  0 12  3  7",
        ]
        board = Board.from_raw(lines)
        self.assertFalse(board.visit(14))
        self.assertFalse(board.visit(21))
        self.assertFalse(board.visit(17))
        self.assertFalse(board.visit(24))
        self.assertTrue(board.visit(4))

    def test_bingo_visit_col(self):
        lines = [
            "14 21 17 24  4",
            "10 16 15  9 19",
            "18  8 23 26 20",
            "22 11 13  6  5",
            "2  0 12  3  7",
        ]
        board = Board.from_raw(lines)
        self.assertFalse(board.visit(24))
        self.assertFalse(board.visit(9))
        self.assertFalse(board.visit(26))
        self.assertFalse(board.visit(6))
        self.assertTrue(board.visit(3))

    def test_sum_no_visists(self):
        lines = [
            "1   2  3  4  5",
            "6   7  8  9 10",
            "11 12 13 14 15",
            "16 17 18 19 20",
            "21 22 23 24 25",
        ]
        board = Board.from_raw(lines)
        sum_all = 25/2*(1+25)  # Gauss summation - (n/2)*(first_num + last_num)
        self.assertEqual(sum_all, board.sum_not_hit_numbers())

    def test_sum_skips_visited(self):
        lines = [
            "1   2  3  4  5",
            "6   7  8  9 10",
            "11 12 13 14 15",
            "16 17 18 19 20",
            "21 22 23 24 25",
        ]
        board = Board.from_raw(lines)
        sum_all = 25/2*(1+25)  # Gauss summation - (n/2)*(first_num + last_num)
        board.visit(23)
        sum_all -= 23
        board.visit(8)
        sum_all -= 8
        board.visit(1)
        sum_all -= 1

        self.assertEqual(sum_all, board.sum_not_hit_numbers())
