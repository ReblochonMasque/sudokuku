"""
puzzlesolver.py
:created on: 20160624
__author__ = 'Frederic Dupont'
:License: GPL3
"""


__author__ = 'Fred Dupont'


import sys

from sudoku import puzzleconstants as p_const
from sudoku.puzzle import Puzzle, make_grid_from_string

class PuzzleInvalidException(Exception):
    """Exception raised when puzzle is invalid
    """
    pass


class PuzzleSolver(object):
    """
    class that solves a sudoku puzzle
    takes the clone of a puzzle and solves it
    """
    def __init__(self, puzzle_clone):
        self._puzzle = puzzle_clone

    def __str__(self):
        return repr(self._puzzle)

    def _is_solved(self):
        """
        check if the puzzle is solved
        :return: True if solved, False otherwise
        """
        return self._puzzle.is_solved()

    def _is_valid(self):
        """
        check if the puzzle is valid
        :return: True if valid, False otherwise
        """
        return self._puzzle.is_valid()

    def _clone(self):
        """returns a clone of self"""
        result = PuzzleSolver(self._puzzle.clone())
        result.eliminate_propagate_fill()
        return result

    def eliminate_candidates(self):
        """For each square in the grid that has a single assigned value,
        run through the PEERS and eliminate this value from the candidates
        *** This will have to be redone each time the puzzle is cloned ***
        :return: False if an inconsistency is discovered --> makes the puzzle invalid
                 True otherwise
        """
        for square in p_const.SQUARES:
            current_value = self._puzzle.grid[square]
            if current_value not in '.0':
                # this says if there is an inconsistency
                # that means it must return False to signal it
                if self._puzzle.candidates[square] != p_const.VALUE_TO_CANDIDATES[current_value]:
                    return False
                for peer in p_const.PEERS[square]:
                    self._puzzle.candidates[peer] = self._puzzle.candidates[peer].replace(current_value, '.')
        return True

    def propagate(self):
        """if a UNIT has only one possible place for a value,
         assign this value there, and adjust the candidates for this place
        """
        for unit in p_const.UNIT_LISTS:
            for digit in p_const.DIGITS:
                result = []
                for square in unit:
                    if digit in self._puzzle.candidates[square]:
                        result.append(square)
                if len(result) == 1:
                    sq = result[0]
                    try:    # assigns digit to grid[square] no matter what, 
                        self._puzzle.candidates[sq] = p_const.VALUE_TO_CANDIDATES[digit]
                        self._puzzle.grid[sq] = digit
                    except KeyError:
                        return False
        return True

    def fill_singles(self):
        """
        completes a unit that is missing only one value
        by updating the grid and the candidates values
        :return: False if an inconsistency is discovered, True otherwise
        """
        for unit in p_const.UNIT_LISTS:
            result = []
            result_string_builder = [str(_) for _ in range(1, 10)]
            for square in unit:
                val = self._puzzle.grid[square]
                if val in '.0':
                    result.append(square)
                else:
                    result_string_builder[int(val) - 1] = '.'
            if len(result) == 1:
                sq = result[0]
                self._puzzle.candidates[sq] = ''.join(result_string_builder)
                try:
                    self._puzzle.grid[sq] = p_const.CANDIDATES_TO_VALUE[''.join(result_string_builder)]
                except KeyError:
                    return False
        return True

    def _get_next_square(self):
        """
        Finds the square to explore next:
            --> not filled
            --> with the lowest number of candidates
        :return: the square to explore next
        """
        lowest_num_candidates = 10
        next_square = None
        for open_square in [square for square in p_const.SQUARES if self._puzzle._grid[square] in '.0']:
            num_candidates = sum(1 for d in self._puzzle.candidates[open_square] if d in '123456789')
            if num_candidates == 2:
                return open_square
            elif num_candidates < lowest_num_candidates:
                next_square = open_square
                lowest_num_candidates = num_candidates
        return next_square

    def eliminate_propagate_fill(self):
        """
        Propagates the constraints by successively eliminating, propagating and filling the
        solved squares until all constraints have been propagated. (no more change in the
        puzzle states)
        ...or the puzzle is solved
        :return: False if an inconsistency is discovered, True otherwise
        """
        while not self._puzzle.is_solved():
            pre_grid_state, pre_candidates_state = repr(self._puzzle), str(self._puzzle)
            if not self.eliminate_candidates() or not self._is_valid():
                return False
            if not self.propagate() or not self._is_valid():
                return False
            if not self.fill_singles() or not self._is_valid():
                return False
            # @TODO: 3 times self._is_valid() to refactor when time comes
            post_grid_state, post_candidates_state = repr(self._puzzle), str(self._puzzle)
            if pre_grid_state == post_grid_state and pre_candidates_state == post_candidates_state:
                return True
        return True

    # def search(self):
    #     """
    #     creates a new clone solver
    #     assigns the next candidate value to the empty square with the less candidates
    #     recursively calls solve() on the new puzzle
    #     """
    #     temp = self
    #     liste_candidates = []
    #     while not self._is_solved():
    #
    #         next_square = self._get_next_square()
    #         candidates = [d for d in     self._puzzle.candidates[next_square] if d not in '.0']
    #         liste_candidates.append(list(candidates))
    #         candidate = candidates.pop()
    #         new_solver = self._clone()
    #         new_solver._puzzle.grid[next_square] = candidate
    #
    #         temp = new_solver
    #
    #         if not temp.eliminate_propagate_fill():
    #             if len(candidates) > 0:  # on change de feuille
    #                 candidate = candidates.pop()
    #                 new_solver = new_solver._clone()
    #                 new_solver._puzzle.grid[next_square] = candidate
    #             else:  # on doit changer la racine
    #                 candidates = liste_candidates.pop()
    #                 candidate = candidates.pop()   # pas sur de ça
    #                 new_solver = new_solver._clone()   # pas sur de ça
    #                 new_solver._puzzle.grid[next_square] = candidate   # pas sur de ça
    #         # si c'est bon :
    #         else:
    #             continue  # recommence la boucle au début.
    #
    #     return str(self)
    #
    #     # print('ouverture de search')
    #     # if self._is_solved():  # cas d'arrêt
    #     #     print('is solved')
    #     #     return str(self)
    #     # next_square = self._get_next_square()
    #     # candidates = [d for d in self._puzzle.candidates[next_square] if d not in '.0']
    #     # candidate = candidates.pop()
    #     # new_solver = self._clone()
    #     # new_solver._puzzle.grid[next_square] = candidate
    #     # if new_solver.eliminate_propagate_fill():
    #     #     print('self.eliminate_propagate_fill() verifié')
    #     #
    #     #
    #     #     if new_solver._is_valid():
    #     #         print('new_solver._is_valid() verifié')
    #     #         res = new_solver.search()
    #     #         return str(res)
    #     #         print('is_valid new solver')
    #     #     else:
    #     #         self._puzzle.grid[next_square] = candidates.pop()
    #     #         self.search()
    #     #         print('refus de l\'hypothèse')
    #     # else:
    #     #     candidate = candidates.pop()
    #     #     # self.search()

    #
    # def search(self):
    #     """
    #     creates a new clone solver
    #     assigns the next candidate value to the empty square with the less candidates
    #     recursively calls solve() on the new puzzle
    #     """
    #     # if not self._is_valid():
    #     #     return 'stuck there'
    #     # if self._is_solved():
    #     #     return str(self)
    #
    #     # new_solver = self._clone()
    #
    #     # if not new_solver._is_valid():
    #     #     #raise PuzzleInvalidException
    #     #     return 'stuck there 2' #raise  error°1
    #     if self._is_solved():
    #         return str(self)
    #
    #     next_square = self._get_next_square()
    #     candidates = [d for d in self._puzzle.candidates[next_square] if d not in '.0']
    #
    #     # if next_square is None:
    #     #     # print(new_solver)
    #     #     return str(new_solver + 'next square was None')
    #
    #     while len(candidates) > 0:   # or not new_solver._is_solved()  :
    #         new_solver = self._clone()
    #         candidate = candidates.pop()
    #         new_solver._puzzle.grid[next_square] = candidate
    #         if not new_solver.eliminate_propagate_fill():
    #             continue
    #
    #         # if not new_solver._is_valid():
    #         #     #new_solver._puzzle.grid[next_square] = candidate
    #             # new_solver.eliminate_propagate_fill()
    #             # break
    #         else :
    #
    #             new_solver.search()
    #
    #     return str(new_solver)
    #     # for candidate in candidates:
    #     #     new_solver._puzzle.grid[next_square] = candidate
    #     #     print('next_square =', next_square, 'candidate =', candidate, ' - ', new_solver)
    #     #     #try:
    #     #     new_solver.search()
    #     #     if new_solver._is_valid():
    #     #         break
    #     #     else:
    #     #         self.search()
    #     #     # except PuzzleInvalidException:   # except error°1
    #     #     #     print('coucou et vive le qwerty')
    #     #     #     return self   # clone d'avant
    #     # return str(new_solver)
    #


    def solve(self):
        """
        manages the operations to conduct in order to solve a puzzla
        :return: a solved solver object or an error message
        """
        # if self._is_solved():
        #     return self
        # if self.eliminate_propagate_fill():
        #     # self.eliminate_propagate_fill()
        #     return self.search()
        # self.solve()
        self.eliminate_propagate_fill()
        return str(self)


def main(argv):

    # require search
    g1 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    partial_s1 = '4.....8.5.3..........7......2.....6.....8.4...4..1.......6.3.7.5.32.1...1.4......'
    s1 = '417369825632158947958724316825437169791586432346912758289643571573291684164875293'
    solve_puzzle('g1', g1, s1)

    # require search
    g2 = '1...895..5....7819........72.4..8.7.9.71.54.8.8.7..3.531.4..78.4682....3..985...1'
    partial_s2 = '172.895.454..2781989.5142.7254938176937165428681742395315496782468271953729853641'
    s2 = '172389564543627819896514237254938176937165428681742395315496782468271953729853641'
    solve_puzzle('g2', g2, s2)
    print()

    # exits with "stuck there"
    g3 = '58261..9.3..79528117928..6....4389..9..126..8..89571..25..61.79.9..72..3....496.2'
    s3 = '582614397346795281179283564761438925935126748428957136253861479694572813817349652'
    solve_puzzle('g3', g3, s3)
    print()

    # Expert level
    # Exits with "stuck there"
    g5 = '5.9........6.......1.85...3...7....8..51...4.3...4.7..9.1......7.4.1639.........4'
    # g5 = '5.9........6.......1.85...3...7.9..8..51...4.3...4.7..9.1......7.4.1639.........4'
    s5 = '539674821826391475417852963142769538675138249398245716951423687784516392263987154'
    solve_puzzle('g5', g5, s5)
    print()

    # exits with key error
    # self._puzzle.grid[result[0]] = p_const.CANDIDATES_TO_VALUE[''.join(res_string)]
    # KeyError: '..3.5....'
    g4 = '2.....38..........1.3..4.575.73.281.......236....8..........1....28......6...7.4.'
    s4 = '294756381675138492183294657547362819918475236326981574759643128432819765861527943'
    solve_puzzle('g4', g4, s4)
    print()

def solve_puzzle(name, provided_string, expected_solved_string):

    print('\n\n#----N-E-X-T---T-E-S-T---' + name + '---------------------------------------------#\n')
    print('original string                 - ', provided_string)

    provided_puzzle = make_grid_from_string(provided_string)
    expected_puzzle = make_grid_from_string(expected_solved_string)
    solver = PuzzleSolver(provided_puzzle.clone())
    res = solver.solve()
    if len(res) == 81:
        result = make_grid_from_string(res)
    else:
        result = make_grid_from_string('.' * 81)

    print('Solution                        - ', repr(result))
    print('Exit search/solve with          - ', res)

    print('\nstarting puzzle :')
    print(provided_puzzle.get_puzzle_str())
    print('expected solution :')
    print(expected_puzzle.get_puzzle_str())

    print('obtained solution :')
    print(result.get_puzzle_str())




if __name__ == '__main__':
    sys.exit(main(sys.argv))
#     grid_string_1 = '1...895..5....7819........72.4..8.7.9.71.54.8.8.7..3.531.4..78.4682....3..985...1'
#     grid_1 = make_grid_from_string(grid_string_1)
#     grid_1.parse_grid_candidates()
#
#
#     solver = PuzzleSolver(grid_1.clone())
#     solver.eliminate_candidates()
#     solver.propagate()
#     print('prepuzzle = \n' + solver._puzzle.get_puzzle_str())
#     print('pre_candidate = \n' + solver._puzzle.__str__())
#
#     solver.fill_singles()
#     #solver.eliminate_candidates()
#     # solver.fill_singles()
#     print('postpuzzle = \n' + solver._puzzle.get_puzzle_str())
#     print('post_candidate = \n' + solver._puzzle.__str__())
