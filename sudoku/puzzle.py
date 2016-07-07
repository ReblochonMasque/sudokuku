# -*- coding: utf-8 -*-
"""
puzzle.py
sudoku solver
Created on Wed Jun  1 15:27:23 2016

"""

# # Constants used
# SQUARES --> an ordered list of every square_key used to access UNITS, PEERS
# UNITS   --> a dictionary containing the access keys for the rows, cols & boxes
#             of a square {'square_key' : [[square_keys for row],
#                                          [square_keys for col],
#                                          [square_keys for box]]}
# PEERS   --> a dictionary containing the access keys for the peers
#             {'square_key': [peers]}
# DIGITS  --> legal values for a solved square '123456789'


__author__ = 'Fred Dupont'


from . import puzzleconstants as p_const
# import sudoku.puzzleconstants as p_const


class Puzzle(object):
    """
    represents a sudoku grid as a dictionary of {squares: values}
    """

    def __init__(self):
        self._grid = None
        self._candidates = {square: p_const.DIGITS for square in p_const.SQUARES}

    @property
    def candidates(self):
        """getter"""
        return self._candidates

    @property
    def grid(self):
        """getter"""
        return self._grid

    def clone(self):
        """
        makes a clone of the puzzle
        :return: a Puzzle object, clone of self
        """
        cloned_puzzle =  make_grid_from_string(self.get_puzzle_str())
        assert cloned_puzzle.is_valid()
        cloned_puzzle.parse_grid_candidates()
        return cloned_puzzle

    def parse_grid_candidates(self):
        """
        assigns candidates to self._candidates according
        to the values in self._grid
        """
        for square, value in self._grid.items():
            if value not in '.0':
                self._candidates[square] = p_const.VALUE_TO_CANDIDATES[value]

    def from_string(self, chars):
        """
        :param chars: a string containing the values of a sudoku grid, in a row/col order
        :return: a sudoku grid build from the input values and checked for validity
                 but not for uniqueness of solution
        """
        if len(chars) != len(p_const.SQUARES):
            raise ValueError('Parameter string length is wrong')
        else:
            self._grid = {key: value for key, value in zip(p_const.SQUARES, chars)}
        return self

    def is_solved(self):
        """
        Checks is a puzzle is solved (full and valid)
        :return: True is the puzzle is solved, False otherwise
        """
        return not any([val in '.0' for _, val in self._grid.items()]) and self.is_valid()

    def is_valid(self) -> bool:
        """
        verifies if a grid is valid
        --> proper size -> all squares have a value assigned                       V
                        -> no extra entries                                        V
        --> all values assigned to squares are legal <=> are in DIGITS or '0.'     V
        --> unique values in rows / columns / boxes (UNITS)                        V
        --> unique values in PEERS                                                 V

        :return: True if is valid, False otherwise
        """
        # TODO: Change to lazy evaluation
        # TODO: Refactor (checking PEERS is likely redundant)
        result = True
        result &= self._contains_all_keys()
        result &= self._are_values_legal()
        for square in p_const.SQUARES:
            result &= self._is_unique_in_block(self._grid[square], p_const.PEERS[square])
            for block in p_const.UNITS[square]:
                result &= self._is_unique_in_block(self._grid[square], block)
        return result

    def _is_unique_in_block(self, value, block):
        """
        checks if the given value is unique for the provided block of keys
        :param value: a value for a square
        :param block: a list of keys to access the values of a block
        :return: True if the value is unique, False otherwise
        """
        seen = 0
        for square in block:
            if self._grid[square] in p_const.DIGITS and self._grid[square] == value:
                seen += 1
        return seen <= 1

    def _are_values_legal(self):
        """
        checks that all values in self._grid are legal (in DIGITS or '0.')
        :return: True if all values are legal, False otherwise
        """
        return all([value in p_const.DIGITS or value in '0.' for value in self._grid.values()])

    def _contains_all_keys(self) -> bool:
        """
        checks if self._grid.keys() contains the proper keys and not more
        :return: True if self_grid contains all keys and not more, False otherwise
        """
        temp = sorted(list(self._grid.keys()))
        return temp == p_const.SQUARES and len(temp) == len(p_const.SQUARES)

    def __repr__(self):
        """
        :return: a simple string representation of sa puzzle
        """
        return ''.join([self._grid[square] for square in p_const.SQUARES])

    def __str__(self):
        result = '   '
        for col, char2 in enumerate('abcdefghi'):
            result += '     ' + char2 + '     '
            if (col + 1) % 3 == 0:
                result += ' '
        result += '\n   ' + '--------------------------------- ' * 3 + '\n'
        for row, char1 in enumerate('ABCDEFGHI'):
            result += char1 + ' |'
            for col, char2 in enumerate('abcdefghi'):
                result += ' ' + self._candidates[char1 + char2] + ' '
                if (col + 1) % 3 == 0:
                    result += '|'
            result += '\n'
            if (row + 1) % 3 == 0:
                result += '   ' + '--------------------------------- ' * 3 + '\n'
        # print(result)
        return result

    def get_puzzle_str(self):
        """
        returns a string to print a puzzle
        :return: a string that represents a puzzle
        """
        result = '  a b c d e f g h i\n'
        for row, char1 in enumerate('ABCDEFGHI'):
            result += char1 + ' '
            for col, char2 in enumerate('abcdefghi'):
                res = self._grid[char1 + char2]
                if res == '0':
                    res = '.'
                result += res
                if (col + 1) % 3 != 0:
                    result += ' '
                elif (col + 1) < 9:
                    result += '|'
            result += '\n'
            if(row + 1) % 3 == 0 and (row + 1) < 9:
                result += '  -----+-----+-----\n'
        return result

# @TODO: make a grid of values
# @TODO: add a __str__ for self._possible_values


def make_grid_from_string(values):
    """
    converts a string of values into a sudoku grid dictionary {square:char}
    using a DIGIT for value and '0' or '.' for empties
    ignores everything else
    """
    _grid = Puzzle()
    chars = [char for char in values if char in p_const.DIGITS or char in '0.']
    assert len(chars) == 81, "the grid has an incorrect size"
    return _grid.from_string(chars)


# if __name__ == '__main__':
#
#     grid = make_grid_from_string(''.join(['.'] * 81))
#     print(grid)
#     print(grid.print_puzzle())
#
#     grid_string =
#     '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#     grid2 = make_grid_from_string(grid_string)
#     print(grid2)
#     print(grid2.print_puzzle())
#     grid.is_valid_grid()
#     grid = make_grid_from_string(''.join(['123456789'] * 9))
#     print(grid)
#
#     chars_repeats_in_row =
#     '4..4..8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
#     invalid_grid = Puzzle().from_string(chars_repeats_in_row)
#     invalid_result = invalid_grid.is_valid_grid()
#     print(invalid_result)
