import random
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
import cube


# ------------------------------------------------- CROSS ------------------------------------------------- #
def check_cross(cubeobj: cube.Cube) -> bool:
    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    for cross_pos in (16, 17, 18, 19):
        if cubeobj[cross_pos] != solved[cross_pos]:
            return False

    return True


def get_badpos(cubeobj: cube.Cube) -> tuple:
    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    output = []
    for edge in cubeobj.cube[8:]:
        if cubeobj.bottom in edge.orientation and (solved.find_piece(edge) != edge.pos):
            output.append(edge.pos)

    return tuple(output)


def to_bottom(cubeobj: cube.Cube, target_pos: int) -> None:
    tb_index = {
        8: 16,
        9: 17,
        10: 18,
        11: 19
    }

    moveindex = {
        8: 'L2',
        9: 'B2',
        10: 'R2',
        11: 'F2'
    }

    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    target_piece = cubeobj[target_pos]
    goal = solved.find_piece(target_piece)

    while tb_index[target_piece.pos] != goal:
        cubeobj.cube_move('U')

    cubeobj.perform_algorithm(moveindex[target_piece.pos])


def to_top(cubeobj: cube.Cube, target_pos: int) -> None:
    moveindex = {
        12: "L U Lp",
        13: "R' U R",
        14: "Lp Up L'",
        15: "R U Rp",
        16: 'L2',
        17: 'B2',
        18: 'R2',
        19: 'F2'
    }

    cubeobj.perform_algorithm(moveindex[target_pos])


def reorient_flipped(cubeobj: cube.Cube):
    # find incorrectly oriented pieces
    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    incorrects = [edge.pos for edge in cubeobj[8:] if edge != solved[edge.pos]]

    if incorrects:
        for _ in range(4):
            if cubeobj[19][1] != cubeobj.bottom:
                cubeobj.perform_algorithm('Fp R U Rp F2')

            cubeobj.cube_move('y')


def cross_looper(cubeobj: cube.Cube, abs_positions: tuple, targets: tuple, direction: str, counter=0) -> tuple:
    flag = True
    for pos in abs_positions:
        if pos in targets:
            flag = False
            if direction == 'down':
                to_bottom(cubeobj, pos)

            else:
                to_top(cubeobj, pos)

        counter += 1
        targets = find_badpos(cubeobj)

    if flag:
        return get_badpos(cubeobj), counter

    else:
        targets = get_badpos(cubeobj)
        return cross_looper(cubeobj, abs_positions, targets, direction)


def cross(cubeobj: cube.Cube) -> None:
    # while there are incorrectly positioned edges
    targets = get_badpos(cubeobj)
    counter = 0
    threshold = 10
    while len(targets) > 0 and counter < threshold:
        for top_pos in (8, 9, 10, 11):
            if top_pos in targets:
                to_bottom(cubeobj, top_pos)
                targets = get_badpos(cubeobj)
                counter += 1

        for target in targets:
            if target not in (8, 9, 10, 11):
                to_top(cubeobj, target)
                targets = get_badpos(cubeobj)
                counter += 1

    reorient_flipped(cubeobj)

    if counter > threshold or not check_cross(cubeobj):
        cubeobj.scramble(10, printrepr=False)
        cross(cubeobj)

    while len(targets) != 0 and counter < threshold:
        # do top positions
        top_positions = (0, 1, 2, 3)
        targets, counter = cross_looper(cubeobj, top_positions, targets, 'down')

        # do bottom positions
        bottom_positions = (4, 5, 6, 7)
        targets, counter = cross_looper(cubeobj, bottom_positions, targets, 'up', counter)

    if counter > threshold or not check_cross(cubeobj):
        destructors = ['M', 'S', 'E']
        shaker = ' '.join([random.choice(destructors) for _ in range(5)])

        before = cubeobj.define()
        cubeobj.perform_algorithm(shaker)
        after = cubeobj.define()

        with open('scramblesShaker10.txt', 'a') as file:
            file.write('Cr{:^5}\tBefore: {:^60}\tAfter: {:^60}\n'.format(len(shaker.split()), before, after))

        cross(cubeobj)

# ------------------------------------------------- CORNERS ------------------------------------------------- #
# similar to cross method get_badpos; find all incorrectly positioned corners
def find_badpos(cubeobj: cube.Cube) -> tuple:
    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    output = []

    for corner in cubeobj.cube[:8]:
        if cubeobj.bottom in corner.orientation and solved.find_piece(corner) != corner.pos:
            output.append(corner.pos)

    return tuple(output)


def to_down(cubeobj: cube.Cube, target_pos: int) -> None:
    tb_index = {
        0: 4,
        1: 5,
        2: 6,
        3: 7
    }

    moveindex = {
        0: 'U R Up Rp',
        1: "F R' F' R2 U R' U' F R' F' R",
        2: 'F Rp Fp R'
    }

    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    target_piece = cubeobj[target_pos]
    goal = solved.find_piece(target_piece)

    # get piece above target position
    while tb_index[target_piece.pos] != goal:
        cubeobj.cube_move('U')

    # get cube into position
    while target_piece.pos != 3:
        cubeobj.cube_move('y')

    # 0 = bottom facing, 1 = bottom on top, 2 = bottom on side
    piece_orientation = target_piece.orientation.index(cubeobj.bottom)
    cubeobj.perform_algorithm(moveindex[piece_orientation])


def to_up(cubeobj: cube.Cube, target_pos: int) -> None:
    moveindex = {
        4: 'L U Lp',
        5: 'Rp Up R',
        6: 'Lp Up L',
        7: 'R U Rp'
    }

    cubeobj.perform_algorithm(moveindex[target_pos])


def check_firstlayer(cubeobj: cube.Cube) -> bool:
    corner_flag = True
    for piece in (4, 5, 6, 7):
        if cubeobj[piece][1] != cubeobj.bottom:
            return False

    return corner_flag and check_cross(cubeobj)


def corner_looper(cubeobj: cube.Cube, abs_positions: tuple, targets: tuple, direction: str, counter=0) -> tuple:
    flag = True
    for pos in abs_positions:
        if pos in targets:
            flag = False
            if direction == 'down':
                to_down(cubeobj, pos)

            else:
                to_up(cubeobj, pos)

        counter += 1
        targets = find_badpos(cubeobj)

    if flag:
        return find_badpos(cubeobj), counter

    else:
        targets = find_badpos(cubeobj)
        return corner_looper(cubeobj, abs_positions, targets, direction)


def corners(cubeobj: cube.Cube):
    targets = find_badpos(cubeobj)
    counter = 0
    threshold = 15
    while len(targets) != 0 and counter < threshold:
        # do top positions
        top_positions = (0, 1, 2, 3)
        targets, counter = corner_looper(cubeobj, top_positions, targets, 'down')

        # do bottom positions
        bottom_positions = (4, 5, 6, 7)
        targets, counter = corner_looper(cubeobj, bottom_positions, targets, 'up', counter)

    if counter > threshold or not check_firstlayer(cubeobj):
        destructors = ['M', 'S', 'E']
        shaker = ' '.join([random.choice(destructors) for _ in range(5)])

        before = cubeobj.define()
        cubeobj.perform_algorithm(shaker)
        after = cubeobj.define()

        with open('scramblesShaker10.txt', 'a') as file:
            file.write('Co{:^5}\tBefore: {:^60}\tAfter: {:^60}\n'.format(len(shaker.split()), before, after))

        cross(cubeobj)
        corners(cubeobj)


# ------------------------------------------------- Second Edges ------------------------------------------------- #
def get_positions(cubeobj: cube.Cube) -> tuple:
    solved = cube.Cube(front=cubeobj.front, right=cubeobj.right, top=cubeobj.top)
    output = []
    for piece in (12, 13, 14, 15):
        cur_piece = cubeobj[cubeobj.find_piece(solved[piece])]
        if cur_piece != solved[piece]:
            output.append(cur_piece.pos)

    return tuple(output)


# get incorrect edge out
def remove_edge(cubeobj: cube.Cube, target_pos: int) -> None:
    moveindex = {
        12: "L U' L' B L' B' L",
        13: "R' U R B' R B R'",
        14: "L' U L F' L F L'",
        15: "R U' R' F R' F' R"
    }

    cubeobj.perform_algorithm(moveindex[target_pos])


def insert_edge(cubeobj: cube.Cube, target_pos: int) -> None:
    # index mapping non y-axis colour to correct position on cube
    position_index = {
        cubeobj.left: 8,
        cubeobj.back: 9,
        cubeobj.right: 10,
        cubeobj.front: 11
    }

    target_piece = cubeobj[target_pos]

    # get non-y axis colour, since other two will be always be either None or an actual string
    outward_colour = (str(target_piece[0]) + str(target_piece[2])).replace('None', '')
    # position piece
    while target_piece.pos != position_index[outward_colour]:
        cubeobj.cube_move('U')

    # position cube
    while target_piece.pos != 11:
        cubeobj.cube_move('y')

    # perform algorithm leftward or rightward depending on top colour of edge piece
    leftward = "U' L' U L F' L F L'"
    rightward = "U R U' R' F R' F' R"

    if target_piece[1] == cubeobj.left:
        cubeobj.perform_algorithm(leftward)

    else:
        cubeobj.perform_algorithm(rightward)


def edges(cubeobj: cube.Cube) -> None:
    targets = get_positions(cubeobj)

    while len(targets) > 0:
        for top_pos in (8, 9, 10, 11):
            if top_pos in targets:
                insert_edge(cubeobj, top_pos)
                targets = get_positions(cubeobj)

        for middle_pos in (12, 13, 14, 15):
            if middle_pos in targets:
                remove_edge(cubeobj, middle_pos)
                targets = get_positions(cubeobj)


def f2l(cubeobj: cube.Cube) -> None:
    cross(cubeobj)
    corners(cubeobj)
    edges(cubeobj)


if __name__ == '__main__':
    kube = cube.build('royybwbyywobbrywoyrrgryggbwowbwobrbbwgowwoogoggrrgryyg')
    kube.solve(True)
