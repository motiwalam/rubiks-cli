#!/usr/bin/env python3

import sys, pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

from typing import Tuple, Union, List
from projeuler.commonFunctions import invert_dict
import random

# Positions:
# Corners:
# BackTopLeft: 0
# BackTopRight: 1
# FrontTopLeft: 2
# FrontTopRight: 3
# BackBottomLeft: 4
# BackBottomRight: 5
# FrontBottomLeft: 6
# FrontBottomRight: 7

# Edges:
# TopLeft: 8             #MiddleFrontLeft: 14
# TopBack: 9             #MiddleFrontRight: 15
# TopRight: 10           #BottomLeft: 16
# TopFront: 11           #BottomBack: 17
# MiddleBackLeft: 12     #BottomRight: 18
# MiddleBackRight: 13    #BottomFront: 19

# type for either None or str
NoneStr = Union[str, None]
# valid moves index
validmoves = ['R', 'Rp', 'L', 'Lp', 'U', 'Up', 'D', 'Dp', 'B', 'Bp', 'F', 'Fp', 'R2', 'L2', 'U2', 'D2', 'B2', 'F2',
              "R'", "L'", "U'", "D'", "B'", "F'", 'x', 'y', 'z', 'xp', 'yp', 'zp', "x'", "y'", "z'", 'x2', 'y2', 'z2',
              'M', 'Mp', "M'", 'S', "Sp", "S'", 'E', 'Ep', "E'", 'M2', 'S2', 'E2']
cubedefinition = ''


class Piece:
    def __init__(self, pos: int, x: str, y: str, z: str):
        self.orientation = (x, y, z)
        self.pos = pos

    def __eq__(self, other):
        return self.pos == other.pos and self.orientation == other.orientation

    def __getitem__(self, item):
        return self.orientation[item]

    def piece_move(self, move, iscorner: bool = True) -> None:
        if move.endswith('p') or move.endswith("'"):
            clockwise = False

        else:
            clockwise = True

        axisindex = {
            # x and y colours are swapped, z colour remains the same
            'R': (2, 0, 1),
            'L': (2, 0, 1),
            # x and z colours are swapped, y colour remains the same
            'U': (1, 0, 2),
            'D': (1, 0, 2),
            # z and y colours are swapped, x colour remains the same
            'B': (0, 2, 1),
            'F': (0, 2, 1)
        }
        if iscorner:
            moveindex = {
                'R': (1, 5, 7, 3),
                'L': (0, 2, 6, 4),
                'U': (0, 1, 3, 2),
                'D': (4, 6, 7, 5),
                'B': (0, 4, 5, 1),
                'F': (2, 3, 7, 6)
            }

        else:
            moveindex = {
                'R': (10, 13, 18, 15),
                'L': (8, 14, 16, 12),
                'U': (8, 9, 10, 11),
                'D': (16, 19, 18, 17),
                'B': (9, 12, 17, 13),
                'F': (11, 15, 19, 14)
            }

        # transform position
        pos1, pos2, pos3, pos4 = moveindex[move[0]][0], moveindex[move[0]][1], moveindex[move[0]][2], \
                                 moveindex[move[0]][3]
        _generic_pos_move(self, pos1, pos2, pos3, pos4, clockwise)

        # transform orientation
        constant, switch1, switch2 = axisindex[move[0]][0], axisindex[move[0]][1], axisindex[move[0]][2]
        _generic_orientation_move(self, constant, switch1, switch2)

        # double moves
        if move.endswith('2'):
            _generic_pos_move(self, pos1, pos2, pos3, pos4, clockwise)
            _generic_orientation_move(self, constant, switch1, switch2)


class Square:
    def __init__(self, colour: str):
        if colour:
            self.colour = colour

        else:
            self.colour = 'Unknown'

    def __str__(self):
        colourindex = {
            'w': '[w]',
            'y': '[y]',
            'r': '[r]',
            'o': '[o]',
            'g': '[g]',
            'b': '[b]',
            'Unknown': '[NA]'
        }

        return colourindex[self.colour]

    def __repr__(self):
        ansicolourindex = {
            'w': "\x1b[48;2;255;255;255m",
            'y': "\x1b[48;2;255;255;45m",
            'r': "\x1b[48;2;255;0;0m",
            'o': "\x1b[48;2;255;110;0m",
            'g': "\x1b[48;2;0;255;0m",
            'b': "\x1b[48;2;0;174;255m",
            'Unknown': "\x1b[40m"
        }

        return ansicolourindex[self.colour] + "  \x1b[49m"


class Corner(Piece):
    def __init__(self, pos: int, x: str, y: str, z: str) -> None:
        super().__init__(pos, x, y, z)

    def __str__(self):
        x, y, z = self.orientation[0], self.orientation[1], self.orientation[2]
        x, y, z = Square(x), Square(y), Square(z)
        output = '{}\n{}{}'.format(y, x, z)
        return output

    def __repr__(self):
        x, y, z = self.orientation[0], self.orientation[1], self.orientation[2]
        x, y, z = Square(x), Square(y), Square(z)
        output = '{}\n{}{}'.format(repr(y), repr(x), repr(z))
        return output


class Edge(Piece):
    def __init__(self, pos: int, x: NoneStr, y: NoneStr, z: NoneStr) -> None:
        super().__init__(pos, x, y, z)

    def __str__(self):
        squares = [Square(colour) for colour in self.orientation if colour]
        return '{}{}'.format(squares[0], squares[1])

    def __repr__(self):
        squares = [Square(colour) for colour in self.orientation if colour]
        return '{}{}'.format(repr(squares[0]), repr(squares[1]))

    def piece_move(self, move: str, iscorner: bool = False) -> None:
        super().piece_move(move, iscorner)


class Cube:
    def __init__(self, front='green', right='red', top='white'):
        opposites = {
            'w': 'y',
            'g': 'b',
            'r': 'o',
            'y': 'w',
            'b': 'g',
            'o': 'r'
        }

        self.front = front[0].lower()
        self.back = opposites[self.front]

        self.right = right[0].lower()
        self.left = opposites[self.right]

        self.top = top[0].lower()
        self.bottom = opposites[self.top]

        self.orientation = (self.front, self.right, self.top)
        self.axes = {
            'x': (self.front, self.back),
            'y': (self.top, self.bottom),
            'z': (self.left, self.right)
        }

        self.positions = _generate_positions(self)

        x, y, z = 0, 1, 2
        p = self.positions
        corners = [Corner(pos, p[pos][x], p[pos][y], p[pos][z]) for pos in self.positions if pos <= 7]
        edges = [Edge(pos, p[pos][x], p[pos][y], p[pos][z]) for pos in self.positions if pos >= 8]

        self.cube = corners + edges

    def __repr__(self) -> str:
        # there will be a total of 9 vertical rows in the display/ the actual printing must be done in this way
        sides = _generate_sides(self)
        display = []

        # create rows for each side
        for side in sides:
            side = sides[side]
            for row in range(len(side)):
                side[row] = ''.join([repr(square) for square in side[row]])

        # top side
        for row in sides[self.top]:
            display.append('      {}'.format(row))

        # middle (in the display) sides: left, front, right, back
        for linenum in range(3):
            line = sides[self.left][linenum] + sides[self.front][linenum] + sides[self.right][linenum] + \
                   sides[self.back][linenum]

            display.append(line)

        # bottom side
        for row in sides[self.bottom]:
            display.append('      {}'.format(row))

        display = '\n'.join(display)
        return display + '\n'

    def __str__(self) -> str:
        # there will be a total of 9 rows top to bottom in the display
        sides = _generate_sides(self)
        display = []

        # create rows for each side
        for side in sides:
            side = sides[side]
            for row in range(len(side)):
                side[row] = ''.join([str(square) for square in side[row]])

        # top side
        for row in sides[self.top]:
            display.append('         {}'.format(row))

        # middle sides: left, front, right, back
        for linenum in range(3):
            line = sides[self.left][linenum] + sides[self.front][linenum] + sides[self.right][linenum] + \
                   sides[self.back][linenum]

            display.append(line)

        # bottom side
        for row in sides[self.bottom]:
            display.append('         {}'.format(row))

        display = '\n'.join(display)
        return display

    def __eq__(self, other):
        reverse_seq = ' '.join(self._make_sameorientation(other).__reversed__())
        equality = self.cube == other.cube
        self.perform_algorithm(reverse_seq, printrepr=False)
        return equality

    def __getitem__(self, item):
        return self.cube[item]

    def _make_sameorientation(self, other):
        """ cycle through all 24 possible orientations until orientations of self and other are the same """
        reverse_seq = []
        for z in range(4):
            for y in range(4):
                self.cube_move('y')
                reverse_seq.append('yp')
                if self._get_orientation() == other._get_orientation():
                    return reverse_seq
            self.cube_move('z')
            reverse_seq.append('zp')

        self.cube_move('x')
        reverse_seq = ['xp']
        for y in range(4):
            self.cube_move('y')
            reverse_seq.append('yp')
            if self._get_orientation() == other._get_orientation():
                return reverse_seq

        self.cube_move('x2')
        reverse_seq = ['x']
        for y in range(4):
            self.cube_move('y')
            reverse_seq.append('yp')
            if self._get_orientation() == other._get_orientation():
                return reverse_seq

    def _get_orientation(self):
        return self.front, self.right, self.top

    def cube_move(self, move: str, printrepr=False) -> None:
        moveindex = {
            'R': (1, 3, 5, 7, 10, 13, 15, 18),
            'L': (0, 2, 4, 6, 8, 12, 14, 16),
            'U': (0, 1, 2, 3, 8, 9, 10, 11),
            'D': (4, 5, 6, 7, 16, 17, 18, 19),
            'B': (0, 1, 4, 5, 9, 12, 13, 17),
            'F': (2, 3, 6, 7, 11, 14, 15, 19)
        }
        # normal moves
        if move[0] in moveindex:
            positions = moveindex[move[0]]
            _generic_cube_move(self, positions, move)

        # axis moves
        elif move[0] in 'xyz':
            if move.endswith('2'):
                self._axis_move(move[0])
                self._axis_move(move[0])
            else:
                self._axis_move(move)

        elif move[0] in 'MES':
            if move.endswith('2'):
                self._special_move(move[0])
                self._special_move(move[0])
            else:
                self._special_move(move)

        if printrepr:
            print('\nMove: {}'.format(move))
            print(repr(self))

    def _axis_move(self, move: str):
        if move.endswith('p') or move.endswith("'"):
            clockwise = False

        else:
            clockwise = True

        moveindex = {
            'x': ('top', 'right', 'bottom', 'left'),
            'y': ('front', 'left', 'back', 'right'),
            'z': ('front', 'top', 'back', 'bottom')
        }

        orientation_index = {
            'x': (0, 1, 2),
            'y': (1, 0, 2),
            'z': (2, 1, 0)
        }
        _generic_axis_colours(self, moveindex[move[0]], clockwise)
        _axis_move_positions(self, move, clockwise)

        for piece in self.cube:
            temp = orientation_index[move[0]]
            constant, switch1, switch2 = temp[0], temp[1], temp[2]
            _generic_orientation_move(piece, constant, switch1, switch2)

    # for moves that are really just combinations of other moves; like M, S, E and their primes
    def _special_move(self, move: str) -> None:
        if move == 'M':
            self.perform_algorithm('R Lp zp')
        elif move == 'Mp' or move == "M'":
            self.perform_algorithm('Rp L z')

        elif move == 'E':
            self.perform_algorithm('U Dp yp')
        elif move == 'Ep' or move == "E'":
            self.perform_algorithm('Up D y')

        elif move == 'S':
            self.perform_algorithm('Fp B x')
        elif move == 'Sp' or move == "S'":
            self.perform_algorithm('F Bp xp')

    # find piece position in cube
    def find_piece(self, piece: Piece) -> int:
        for cubie in self.cube:
            flag = True
            for colour in piece.orientation:
                if colour not in cubie:
                    flag = False

            if flag:
                return cubie.pos

    def scramble(self, nummoves=100, printrepr=True) -> None:
        scramble_algo = generate_scramble(nummoves)
        before = self.define()

        if printrepr:
            print('Scramble: {}'.format(scramble_algo))
            self.perform_algorithm(scramble_algo, printrepr=True)

        else:
            self.perform_algorithm(scramble_algo)

        after = self.define()
        # TODO: REMOVE THIS FOR DEBUGGING PURPOSES ONLY
        with open('scramblesShaker10.txt', 'a') as file:
            file.write('{:^5}\tBefore: {:^60}\tAfter: {:^60}\n'.format(len(scramble_algo.split()), before, after))

    def solve(self, show_steps=False):
        import F2L, OLL, PLL
        if show_steps:
            print('Cross: ')
            F2L.cross(self)
            print(repr(self))

            print('Corners: ')
            F2L.corners(self)
            print(repr(self))

            print('Second layer: \n')
            F2L.edges(self)
            print(repr(self))

            print('OLL: \n')
            OLL.oll(self)
            print(repr(self))

            print('PLL: \n')
            PLL.pll(self)
            print(repr(self))

        else:
            F2L.f2l(self)
            OLL.oll(self)
            PLL.pll(self)

            # print(repr(self))

    def perform_algorithm(self, moves: str, printrepr=False, verbose=False) -> None:
        moves = validate_algo(moves)
        for move in moves:
            if move == 'q':
                return

            else:
                self.cube_move(move, printrepr=verbose)

        if printrepr and not verbose:
            print(repr(self))

    def define(self) -> str:
        sides = _get_sidedict(self)
        for side in sides:
            newside = ''
            for row in sides[side]:
                for piece in row:
                    if isinstance(piece, str):
                        newside += piece
                        continue

                    if side in '{}{}'.format(self.top, self.bottom):
                        newside += self[piece][1]

                    elif side in '{}{}'.format(self.front, self.back):
                        newside += self[piece][0]

                    else:
                        newside += self[piece][2]
            sides[side] = newside

        definition = sides[self.top] + sides[self.front] + sides[self.right] + sides[self.back] + sides[self.left] + \
                     sides[self.bottom]

        return definition


def take_moves_input() -> str:
    moves = input('\nEnter sequence of moves here: ')

    return " ".join(validate_algo(moves))


def validate_algo(moves: str) -> List[str]:
    global validmoves
    _validmoves = validmoves + ['q']
    output = []

    # flag to print conditional message
    validityflag = True
    for move in moves.split():
        if move in _validmoves:
            output.append(move)

        else:
            validityflag = False
            print('Unrecognized move {} discarded'.format(move))

    if not validityflag:
        print('Algorithm "{}" will be performed'.format(' '.join(output)))

    return output


def generate_scramble(nummoves: int = 100) -> str:
    global validmoves
    moves = [move for move in validmoves if not move.endswith('p')]
    scramble_algo = []

    for _ in range(nummoves):
        scramble_algo.append(random.choice(moves))

    scramble_algo = ' '.join(scramble_algo)

    return scramble_algo


def _generic_axis_colours(cubeobj: Cube, sides: Tuple[str, str, str, str], clockwise=True) -> None:
    clockwise_transformations = {
        sides[0]: sides[1],
        sides[1]: sides[2],
        sides[2]: sides[3],
        sides[3]: sides[0]
    }
    anti_clockwise = invert_dict(clockwise_transformations)

    if clockwise:
        old_colours = [getattr(cubeobj, side) for side in clockwise_transformations]
        colouridx = 0
        for side in clockwise_transformations:
            setattr(cubeobj, clockwise_transformations[side], old_colours[colouridx])
            colouridx += 1

    else:
        old_colours = [getattr(cubeobj, side) for side in anti_clockwise]
        colouridx = 0
        for side in anti_clockwise:
            setattr(cubeobj, anti_clockwise[side], old_colours[colouridx])
            colouridx += 1

    return


def _axis_move_positions(cubeobj: Cube, move: str, clockwise):
    transformation_idx = {
        'x': {
            0: 1, 1: 5, 2: 3, 3: 7, 4: 0, 5: 4, 6: 2, 7: 6,
            8: 10, 9: 13, 10: 18, 11: 15, 12: 9, 13: 17, 14: 11, 15: 19, 16: 8, 17: 12, 18: 16, 19: 14},

        'y': {0: 1, 1: 3, 3: 2, 2: 0, 4: 5, 5: 7, 7: 6, 6: 4,
              8: 9, 9: 10, 10: 11, 11: 8, 12: 13, 13: 15, 15: 14, 14: 12, 16: 17, 17: 18, 18: 19, 19: 16},

        'z': {0: 4, 1: 5, 2: 0, 3: 1, 4: 6, 5: 7, 6: 2, 7: 3,
              8: 12, 9: 17, 10: 13, 11: 9, 12: 16, 13: 18, 14: 8, 15: 10, 16: 14, 17: 19, 18: 15, 19: 11}

    }

    if clockwise:
        for piece in cubeobj.cube:
            piece.pos = transformation_idx[move[0]][piece.pos]

    else:
        anti_clockwise = invert_dict(transformation_idx[move[0]])
        for piece in cubeobj.cube:
            piece.pos = anti_clockwise[piece.pos]

    _reorder_positions(cubeobj)

    return


def _generic_cube_move(cubeobj: Cube, positions: tuple, move: str):
    # execute moves
    for piece in positions:
        piece = cubeobj.cube[piece]
        piece.piece_move(move)

    # reorder positions
    _reorder_positions(cubeobj)


def _reorder_positions(cubeobj: Cube):
    temp = [0] * 20
    for piece in cubeobj.cube:
        temp[piece.pos] = piece

    cubeobj.cube = temp[:]
    return


# to transform position of piece: there is a cycle of 4 positions for any side
def _generic_pos_move(piece: Piece, pos1: int, pos2: int, pos3: int, pos4: int, clockwise=True) -> None:
    clockwise_transformations = {
        pos1: pos2,
        pos2: pos3,
        pos3: pos4,
        pos4: pos1
    }
    anti_clockwise = invert_dict(clockwise_transformations)

    if clockwise:
        piece.pos = clockwise_transformations[piece.pos]

    else:
        piece.pos = anti_clockwise[piece.pos]


# for each move, the colour on one axis remains the same, while the two other axes switch
def _generic_orientation_move(piece: Piece, constantidx: int, switch1: int, switch2: int) -> None:
    """takes Piece and three integers representing the constant axis and the other two to be switched
    0: x; 1: y, 2: z"""

    output = [0, 0, 0]
    output[constantidx] = piece.orientation[constantidx]
    output[switch1] = piece.orientation[switch2]
    output[switch2] = piece.orientation[switch1]

    piece.orientation = tuple(output)


def _generate_positions(cubeobj: Cube) -> dict:
    positions = {
        0: (cubeobj.back, cubeobj.top, cubeobj.left),
        1: (cubeobj.back, cubeobj.top, cubeobj.right),
        2: (cubeobj.front, cubeobj.top, cubeobj.left),
        3: (cubeobj.front, cubeobj.top, cubeobj.right),
        4: (cubeobj.back, cubeobj.bottom, cubeobj.left),
        5: (cubeobj.back, cubeobj.bottom, cubeobj.right),
        6: (cubeobj.front, cubeobj.bottom, cubeobj.left),
        7: (cubeobj.front, cubeobj.bottom, cubeobj.right),
        8: (None, cubeobj.top, cubeobj.left),
        9: (cubeobj.back, cubeobj.top, None),
        10: (None, cubeobj.top, cubeobj.right),
        11: (cubeobj.front, cubeobj.top, None),
        12: (cubeobj.back, None, cubeobj.left),
        13: (cubeobj.back, None, cubeobj.right),
        14: (cubeobj.front, None, cubeobj.left),
        15: (cubeobj.front, None, cubeobj.right),
        16: (None, cubeobj.bottom, cubeobj.left),
        17: (cubeobj.back, cubeobj.bottom, None),
        18: (None, cubeobj.bottom, cubeobj.right),
        19: (cubeobj.front, cubeobj.bottom, None),
    }

    return positions


def _get_sidedict(cubeobj: Cube) -> dict:
    sides = {
        cubeobj.top: ((0, 9, 1), (8, cubeobj.top, 10), (2, 11, 3)),
        cubeobj.bottom: ((6, 19, 7), (16, cubeobj.bottom, 18), (4, 17, 5)),
        cubeobj.left: ((0, 8, 2), (12, cubeobj.left, 14), (4, 16, 6)),
        cubeobj.right: ((3, 10, 1), (15, cubeobj.right, 13), (7, 18, 5)),
        cubeobj.back: ((1, 9, 0), (13, cubeobj.back, 12), (5, 17, 4)),
        cubeobj.front: ((2, 11, 3), (14, cubeobj.front, 15), (6, 19, 7))
    }
    return sides


def _generate_sides(cubeobj: Cube) -> dict:
    c = cubeobj.cube
    # helper lambdas to retrieve x, y, and z colours of Piece object
    x = lambda g: g.orientation[0]
    y = lambda g: g.orientation[1]
    z = lambda g: g.orientation[2]

    sides = _get_sidedict(cubeobj)

    for side in sides:
        temp = []
        for row in sides[side]:
            temprow = []
            for piece in row:
                if not isinstance(piece, int):
                    temprow.append(Square(piece))
                    continue
                # get colour at y axis if side is top or bottom
                if side in '{}{}'.format(cubeobj.top, cubeobj.bottom):
                    temprow.append(Square(y(c[piece])))

                # get colour at z axis if side is left or right
                elif side in '{}{}'.format(cubeobj.left, cubeobj.right):
                    temprow.append(Square(z(c[piece])))

                # get colour at x axis if side is front or back
                else:
                    temprow.append(Square(x(c[piece])))

            # add row to full side when row is done
            temp.append(temprow)

        # update side once processing finished
        sides[side] = temp

    return sides


def tutorial():
    print('Welcome to Cube! This is a tutorial to help you get started..')
    print('To start, create a cube object like so... cube.Cube()')
    print('This has three main methods, the cube_move() for single steps, the perform_algorithm() for more complex'
          , 'sequences, and the interact() to keep going in real time!')
    print('Some helpful tips: the Cube object is initialized with three colours, the front, the right, and the top.')
    print('By default, these are green, red, and white respectively.')
    print('You may also make use of the verbose arguments in interact, perform_algorithm, and cube_move to display the',
          'state of the cube after each move. By default, this is set to False.')
    print('Finally, there is Cube.scramble(). By default, this will run 100 random moves. You may change this.')
    print('That\'s it! Call Cube.scramble() to get started!')


# takes cube definition string describing the colours of faces in this order
# UUUUUUUUU FFFFFFFFF RRRRRRRRR BBBBBBBBB LLLLLLLLL DDDDDDDDD
# each face is described going left to right from the top left corner as if you were facing
def build(cubedef: NoneStr = None) -> Cube:
    """This function builds a cube from the cube definition string. The string should consist of 54 letters, each
    describing the colour of a particular facelet. The cube is defined face by face in like order: U F R B L D where
    each face is 9 letters representing the colours on that face. The face should be read from top left to bottom right
    """

    # positions to tuple dict consisting of the index at which to find the appropriate colour in the definition string
    if cubedef is None:
        cubedef = _gui_build()

    try:
        cubedef = cubedef.lower()

    except AttributeError:
        return

    pos_to_index = {
        0: (29, 0, 36), 1: (27, 2, 20), 2: (9, 6, 38), 3: (11, 8, 18), 4: (35, 51, 42), 5: (33, 53, 26),
        6: (15, 45, 44), 7: (17, 47, 24), 8: (None, 3, 37), 9: (28, 1, None), 10: (None, 5, 19), 11: (10, 7, None),
        12: (32, None, 39), 13: (30, None, 23), 14: (12, None, 41), 15: (14, None, 21), 16: (None, 48, 43),
        17: (34, 52, None), 18: (None, 50, 25), 19: (16, 46, None)
    }

    cubeobj = Cube()
    cubeobj.top, cubeobj.front, cubeobj.right = cubedef[4], cubedef[13], cubedef[22]
    cubeobj.back, cubeobj.left, cubeobj.bottom = cubedef[31], cubedef[40], cubedef[49]

    corners = []
    for pos in pos_to_index:
        if pos > 7:
            break
        colours = pos_to_index[pos]
        corners.append(Corner(pos, cubedef[colours[0]], cubedef[colours[1]], cubedef[colours[2]]))

    edges = []
    for pos in pos_to_index:
        if pos < 8:
            continue

        colours = pos_to_index[pos]
        x, y, z = [cubedef[colours[idx]] if colours[idx] else colours[idx] for idx in range(3)]
        edges.append(Edge(pos, x, y, z))

    cubeobj.cube = corners + edges
    return cubeobj


def _gui_build():
    import builder_gui as gui
    exec(open(gui.__file__).read())
    if cubedefinition:
        return cubedefinition

    else:
        print('No definition found :(')


def interact(cube, verbose=False) -> None:
    print('Welcome to Cube Interact! Type "q" to quit. Here is your cube:')
    print(repr(cube))

    moves = take_moves_input()
    while 'q' not in moves:
        cube.perform_algorithm(moves, printrepr=True, verbose=verbose)
        moves = take_moves_input()


if __name__ == '__main__':
    cube = Cube()
    interact(cube)
