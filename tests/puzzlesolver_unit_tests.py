"""
puzzlesolver_unit_tests.py
:created on: 20160624
__author__ = 'Frederic Dupont'
:License: GPL3
"""

# import sys

import unittest

from sudoku.puzzle import Puzzle, make_grid_from_string
# from sudoku.puzzleconstants import DIGITS, SQUARES
from sudoku.puzzlesolver import PuzzleSolver


class TestPuzzleSolver(unittest.TestCase):

    #                         empty   solved   grid_0   grid_1   grid_2   grid_3   grid_4
    #
    # eliminate candidates      v        v       v
    # propagate                 v        v
    # fill_singles
    # recursive search


    def setUp(self):
        grid_string_0 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
        self.grid_0 = make_grid_from_string(grid_string_0)
        self.grid_0.parse_grid_candidates()

        grid_string_1 = '1...895..5....7819........72.4..8.7.9.71.54.8.8.7..3.531.4..78.4682....3..985...1'
        self.grid_1 = make_grid_from_string(grid_string_1)
        self.grid_1.parse_grid_candidates()

        grid_string_2 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
        self.grid_2 = make_grid_from_string(grid_string_2)
        self.grid_2.parse_grid_candidates()

        grid_string_3 = '.82...59....8.1..3..52...78...37842...........27945...91...68..2..7.9....73...95.'
        self.grid_3 = make_grid_from_string(grid_string_3)
        self.grid_3.parse_grid_candidates()

        grid_string_4 = '437...189.6.183.......9.536.73..1...9..4.7..1...5..69.124.7.......645.1.356...974'
        self.grid_4 = make_grid_from_string(grid_string_4)
        self.grid_4.parse_grid_candidates()

    def test_PuzzleSolver_object(self):
        """tests if a PuzzleSolver object is created
        """
        puzzle_string = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
        puzzle = make_grid_from_string(puzzle_string)
        puzzle_clone = puzzle.clone()
        solver = PuzzleSolver(puzzle_clone)
        self.assertIsInstance(solver, PuzzleSolver)

    def test_prppagate_empty(self):
        """tests that propagation on an empty puzzle does not change the state
        """
        grid_string = '.................................................................................'
        grid = make_grid_from_string(grid_string)
        grid.parse_grid_candidates()

        solver = PuzzleSolver(grid.clone())
        pre_puzzle = """  a b c d e f g h i
A . . .|. . .|. . .
B . . .|. . .|. . .
C . . .|. . .|. . .
  -----+-----+-----
D . . .|. . .|. . .
E . . .|. . .|. . .
F . . .|. . .|. . .
  -----+-----+-----
G . . .|. . .|. . .
H . . .|. . .|. . .
I . . .|. . .|. . .
"""
        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
B | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
C | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
E | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
F | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
H | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
I | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), pre_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), pre_puzzle)

        solver.propagate()
        post_puzzle = """  a b c d e f g h i
A . . .|. . .|. . .
B . . .|. . .|. . .
C . . .|. . .|. . .
  -----+-----+-----
D . . .|. . .|. . .
E . . .|. . .|. . .
F . . .|. . .|. . .
  -----+-----+-----
G . . .|. . .|. . .
H . . .|. . .|. . .
I . . .|. . .|. . .
"""
        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
B | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
C | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
E | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
F | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
H | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
I | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), post_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), post_puzzle)

    def test_prppagate_full(self):
        """tests that propagation on an empty puzzle does not change the state
        """
        grid_string = '437256189569183742812794536673921458985467321241538697124379865798645213356812974'
        grid = make_grid_from_string(grid_string)
        grid.print_puzzle()
        grid.parse_grid_candidates()

        solver = PuzzleSolver(grid.clone())
        pre_puzzle = """  a b c d e f g h i
A 4 3 7|2 5 6|1 8 9
B 5 6 9|1 8 3|7 4 2
C 8 1 2|7 9 4|5 3 6
  -----+-----+-----
D 6 7 3|9 2 1|4 5 8
E 9 8 5|4 6 7|3 2 1
F 2 4 1|5 3 8|6 9 7
  -----+-----+-----
G 1 2 4|3 7 9|8 6 5
H 7 9 8|6 4 5|2 1 3
I 3 5 6|8 1 2|9 7 4
"""
        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  ..3......  ......7.. | .2.......  ....5....  .....6... | 1........  .......8.  ........9 |\n\
B | ....5....  .....6...  ........9 | 1........  .......8.  ..3...... | ......7..  ...4.....  .2....... |\n\
C | .......8.  1........  .2....... | ......7..  ........9  ...4..... | ....5....  ..3......  .....6... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | .....6...  ......7..  ..3...... | ........9  .2.......  1........ | ...4.....  ....5....  .......8. |\n\
E | ........9  .......8.  ....5.... | ...4.....  .....6...  ......7.. | ..3......  .2.......  1........ |\n\
F | .2.......  ...4.....  1........ | ....5....  ..3......  .......8. | .....6...  ........9  ......7.. |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 1........  .2.......  ...4..... | ..3......  ......7..  ........9 | .......8.  .....6...  ....5.... |\n\
H | ......7..  ........9  .......8. | .....6...  ...4.....  ....5.... | .2.......  1........  ..3...... |\n\
I | ..3......  ....5....  .....6... | .......8.  1........  .2....... | ........9  ......7..  ...4..... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""

        self.assertEqual(str(solver._puzzle), pre_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), pre_puzzle)

        solver.propagate()
        post_puzzle = """  a b c d e f g h i
A 4 3 7|2 5 6|1 8 9
B 5 6 9|1 8 3|7 4 2
C 8 1 2|7 9 4|5 3 6
  -----+-----+-----
D 6 7 3|9 2 1|4 5 8
E 9 8 5|4 6 7|3 2 1
F 2 4 1|5 3 8|6 9 7
  -----+-----+-----
G 1 2 4|3 7 9|8 6 5
H 7 9 8|6 4 5|2 1 3
I 3 5 6|8 1 2|9 7 4
"""
        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  ..3......  ......7.. | .2.......  ....5....  .....6... | 1........  .......8.  ........9 |\n\
B | ....5....  .....6...  ........9 | 1........  .......8.  ..3...... | ......7..  ...4.....  .2....... |\n\
C | .......8.  1........  .2....... | ......7..  ........9  ...4..... | ....5....  ..3......  .....6... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | .....6...  ......7..  ..3...... | ........9  .2.......  1........ | ...4.....  ....5....  .......8. |\n\
E | ........9  .......8.  ....5.... | ...4.....  .....6...  ......7.. | ..3......  .2.......  1........ |\n\
F | .2.......  ...4.....  1........ | ....5....  ..3......  .......8. | .....6...  ........9  ......7.. |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 1........  .2.......  ...4..... | ..3......  ......7..  ........9 | .......8.  .....6...  ....5.... |\n\
H | ......7..  ........9  .......8. | .....6...  ...4.....  ....5.... | .2.......  1........  ..3...... |\n\
I | ..3......  ....5....  .....6... | .......8.  1........  .2....... | ........9  ......7..  ...4..... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), post_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), post_puzzle)

    def test_propagate_grid_0(self):
        """tests change of state whan calling propagate on a puzzle
        """
        solver = PuzzleSolver(self.grid_0.clone())
        solver.eliminate_candidates()

        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  1....67.9  12...67.9 | 1.3.....9  .23..6..9  12...6..9 | .......8.  123.....9  ....5.... |\n\
B | .2...6789  ..3......  12..56789 | 1..45..89  .2.456..9  12.456.89 | 12...67.9  12.4....9  12.4.67.9 |\n\
C | .2...6.89  1...56.89  12..56.89 | ......7..  .23456..9  12.456.89 | 123..6..9  1234....9  1234.6..9 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | ..3...789  .2.......  1.3.5.789 | ..345...9  ..345.7.9  ...45.7.9 | 1.3.5.7.9  .....6...  1.3...789 |\n\
E | ..3..67.9  1...567.9  1.3.567.9 | ..3.5...9  .......8.  .2..567.9 | ...4.....  123.5...9  123...7.9 |\n\
F | ..3..6789  ...456789  ..3.56789 | ..345...9  1........  .2.4567.9 | .23.5.7.9  .23.5..89  .23...789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | .2.....89  .......89  .2.....89 | .....6...  ...45...9  ..3...... | 12..5...9  ......7..  12.4...89 |\n\
H | ....5....  .....6789  ..3..6789 | .2.......  ...4..7.9  1..4..789 | 1.3..6..9  1.34...89  1.34.6.89 |\n\
I | 1........  .....6789  ...4..... | ....5..89  ....5.7.9  ....5.789 | .23.56..9  .23.5..89  .23..6.89 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        pre_puzzle = """  a b c d e f g h i\n\
A 4 . .|. . .|8 . 5\n\
B . 3 .|. . .|. . .\n\
C . . .|7 . .|. . .\n\
  -----+-----+-----\n\
D . 2 .|. . .|. 6 .\n\
E . . .|. 8 .|4 . .\n\
F . . .|. 1 .|. . .\n\
  -----+-----+-----\n\
G . . .|6 . 3|. 7 .\n\
H 5 . .|2 . .|. . .\n\
I 1 . 4|. . .|. . .\n\
"""
        self.assertEqual(str(solver._puzzle), pre_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), pre_puzzle)

        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  1....67.9  12...67.9 | 1.3.....9  .23..6..9  12...6..9 | .......8.  123.....9  ....5.... |\n\
B | .2...6789  ..3......  12..56789 | 1..45..89  .2.456..9  12.456.89 | 12...67.9  12.4....9  12.4.67.9 |\n\
C | .2...6.89  1...56.89  12..56.89 | ......7..  .23456..9  12.456.89 | 123..6..9  1234....9  1234.6..9 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | ..3...789  .2.......  1.3.5.789 | ..345...9  ..345.7.9  ...45.7.9 | 1.3.5.7.9  .....6...  1.3...789 |\n\
E | ..3..67.9  1...567.9  1.3.567.9 | ..3.5...9  .......8.  .2..567.9 | ...4.....  123.5...9  123...7.9 |\n\
F | ..3..6789  ...4.....  ..3.56789 | ..345...9  1........  .2.4567.9 | .23.5.7.9  .23.5..89  .23...789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | .2.....89  .......89  .2.....89 | .....6...  ...45...9  ..3...... | 12..5...9  ......7..  12.4...89 |\n\
H | ....5....  .....6789  ..3...... | .2.......  ...4..7.9  1........ | 1.3..6..9  1.34...89  1.34.6.89 |\n\
I | 1........  .....6789  ...4..... | ....5..89  ....5.7.9  ....5.789 | .23.56..9  .23.5..89  .23..6.89 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        post_puzzle = """  a b c d e f g h i\n\
A 4 . .|. . .|8 . 5\n\
B . 3 .|. . .|. . .\n\
C . . .|7 . .|. . .\n\
  -----+-----+-----\n\
D . 2 .|. . .|. 6 .\n\
E . . .|. 8 .|4 . .\n\
F . 4 .|. 1 .|. . .\n\
  -----+-----+-----\n\
G . . .|6 . 3|. 7 .\n\
H 5 . 3|2 . 1|. . .\n\
I 1 . 4|. . .|. . .\n\
"""
        solver.propagate()
        self.assertEqual(str(solver._puzzle), post_candidates)
        self.assertEqual(solver._puzzle.print_puzzle(), post_puzzle)

    def test_eliminate_candidates_grid_empty(self):
        """tests that eliminate candidates does not change the state of an empty puzzle
        """
        grid_string = '.................................................................................'
        grid = make_grid_from_string(grid_string)
        grid.parse_grid_candidates()

        solver = PuzzleSolver(grid.clone())
        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
B | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
C | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
E | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
F | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
H | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
I | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), pre_candidates)

        solver.eliminate_candidates()
        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
B | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
C | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
E | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
F | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
H | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
I | 123456789  123456789  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), post_candidates)

    def test_eliminate_candidates_grid_solved(self):
        """tests that eliminate candidates does not change the state of an empty puzzle
        """
        grid_string = '437256189569183742812794536673921458985467321241538697124379865798645213356812974'
        grid = make_grid_from_string(grid_string)
        grid.parse_grid_candidates()

        solver = PuzzleSolver(grid.clone())
        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  ..3......  ......7.. | .2.......  ....5....  .....6... | 1........  .......8.  ........9 |\n\
B | ....5....  .....6...  ........9 | 1........  .......8.  ..3...... | ......7..  ...4.....  .2....... |\n\
C | .......8.  1........  .2....... | ......7..  ........9  ...4..... | ....5....  ..3......  .....6... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | .....6...  ......7..  ..3...... | ........9  .2.......  1........ | ...4.....  ....5....  .......8. |\n\
E | ........9  .......8.  ....5.... | ...4.....  .....6...  ......7.. | ..3......  .2.......  1........ |\n\
F | .2.......  ...4.....  1........ | ....5....  ..3......  .......8. | .....6...  ........9  ......7.. |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 1........  .2.......  ...4..... | ..3......  ......7..  ........9 | .......8.  .....6...  ....5.... |\n\
H | ......7..  ........9  .......8. | .....6...  ...4.....  ....5.... | .2.......  1........  ..3...... |\n\
I | ..3......  ....5....  .....6... | .......8.  1........  .2....... | ........9  ......7..  ...4..... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), pre_candidates)

        solver.eliminate_candidates()
        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  ..3......  ......7.. | .2.......  ....5....  .....6... | 1........  .......8.  ........9 |\n\
B | ....5....  .....6...  ........9 | 1........  .......8.  ..3...... | ......7..  ...4.....  .2....... |\n\
C | .......8.  1........  .2....... | ......7..  ........9  ...4..... | ....5....  ..3......  .....6... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | .....6...  ......7..  ..3...... | ........9  .2.......  1........ | ...4.....  ....5....  .......8. |\n\
E | ........9  .......8.  ....5.... | ...4.....  .....6...  ......7.. | ..3......  .2.......  1........ |\n\
F | .2.......  ...4.....  1........ | ....5....  ..3......  .......8. | .....6...  ........9  ......7.. |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 1........  .2.......  ...4..... | ..3......  ......7..  ........9 | .......8.  .....6...  ....5.... |\n\
H | ......7..  ........9  .......8. | .....6...  ...4.....  ....5.... | .2.......  1........  ..3...... |\n\
I | ..3......  ....5....  .....6... | .......8.  1........  .2....... | ........9  ......7..  ...4..... |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), post_candidates)

    def test_eliminate_candidates_grid_0(self):
        """tests that candidates are properly eliminated
        """
        solver = PuzzleSolver(self.grid_0.clone())
        pre_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  123456789  123456789 | 123456789  123456789  123456789 | .......8.  123456789  ....5.... |\n\
B | 123456789  ..3......  123456789 | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
C | 123456789  123456789  123456789 | ......7..  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | 123456789  .2.......  123456789 | 123456789  123456789  123456789 | 123456789  .....6...  123456789 |\n\
E | 123456789  123456789  123456789 | 123456789  .......8.  123456789 | ...4.....  123456789  123456789 |\n\
F | 123456789  123456789  123456789 | 123456789  1........  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | 123456789  123456789  123456789 | .....6...  123456789  ..3...... | 123456789  ......7..  123456789 |\n\
H | ....5....  123456789  123456789 | .2.......  123456789  123456789 | 123456789  123456789  123456789 |\n\
I | 1........  123456789  ...4..... | 123456789  123456789  123456789 | 123456789  123456789  123456789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), pre_candidates)

        solver.eliminate_candidates()
        post_candidates = """        a          b          c           d          e          f           g          h          i      \n\
   --------------------------------- --------------------------------- --------------------------------- \n\
A | ...4.....  1....67.9  12...67.9 | 1.3.....9  .23..6..9  12...6..9 | .......8.  123.....9  ....5.... |\n\
B | .2...6789  ..3......  12..56789 | 1..45..89  .2.456..9  12.456.89 | 12...67.9  12.4....9  12.4.67.9 |\n\
C | .2...6.89  1...56.89  12..56.89 | ......7..  .23456..9  12.456.89 | 123..6..9  1234....9  1234.6..9 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
D | ..3...789  .2.......  1.3.5.789 | ..345...9  ..345.7.9  ...45.7.9 | 1.3.5.7.9  .....6...  1.3...789 |\n\
E | ..3..67.9  1...567.9  1.3.567.9 | ..3.5...9  .......8.  .2..567.9 | ...4.....  123.5...9  123...7.9 |\n\
F | ..3..6789  ...456789  ..3.56789 | ..345...9  1........  .2.4567.9 | .23.5.7.9  .23.5..89  .23...789 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
G | .2.....89  .......89  .2.....89 | .....6...  ...45...9  ..3...... | 12..5...9  ......7..  12.4...89 |\n\
H | ....5....  .....6789  ..3..6789 | .2.......  ...4..7.9  1..4..789 | 1.3..6..9  1.34...89  1.34.6.89 |\n\
I | 1........  .....6789  ...4..... | ....5..89  ....5.7.9  ....5.789 | .23.56..9  .23.5..89  .23..6.89 |\n\
   --------------------------------- --------------------------------- --------------------------------- \n\
"""
        self.assertEqual(str(solver._puzzle), post_candidates)


if __name__ == '__main__':
    unittest.main()
