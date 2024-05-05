import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
import cube


def oll(cubeobj: cube.Cube) -> None:
    cross(cubeobj)
    finish_oll(cubeobj)


############################# CROSS #############################

# make cross
def cross(cubeobj: cube.Cube) -> None:
    hinge_algorithm = "F U R U' R' F'"
    line_algorithm = "F R U R' U' F'"

    if _check_cross(cubeobj):
        return

    if _is_hinge(cubeobj):
        cubeobj.perform_algorithm(hinge_algorithm)

    elif _is_line(cubeobj):
        cubeobj.perform_algorithm(line_algorithm)

    # or it is dot
    else:
        cubeobj.perform_algorithm(hinge_algorithm)
        cross(cubeobj)


# check if there is a cross on the top layer
def _check_cross(cubeobj: cube.Cube) -> bool:
    topcolour = cubeobj.top
    cubelist = cubeobj.cube
    return cubelist[8][1] == cubelist[9][1] == cubelist[10][1] == cubelist[11][1] == topcolour


def _is_hinge(cubeobj: cube.Cube) -> bool:
    for _ in range(4):
        if cubeobj.cube[8][1] == cubeobj.cube[9][1] == cubeobj.top:
            return True

        cubeobj.cube_move('U')


def _is_line(cubeobj: cube.Cube) -> bool:
    for _ in range(2):
        if cubeobj.cube[8][1] == cubeobj.cube[9][1] == cubeobj.top:
            return True

        cubeobj.cube_move('U')


############################################## FINISH OLL ##############################################
def finish_oll(cubeobj: cube.Cube) -> None:
    oll_algo = "R U R' U R U2 R'"

    while not _is_oll_complete(cubeobj):
        cross_type = _get_cross_type(cubeobj)
        _position_cross(cubeobj, cross_type)
        cubeobj.perform_algorithm(oll_algo)

    return


def _get_cross_type(cubeobj: cube.Cube) -> int:
    count = 0
    for corner in (0, 1, 2, 3):
        if cubeobj.cube[corner][1] == cubeobj.top:
            count += 1

    return count


def _position_cross(cubeobj: cube.Cube, cross_type: int) -> None:
    # no matter what type of cross, you are always looking at UFL corner, just a different colour each time
    type_index = {
        0: 2,  # no colours on top you position the UFL corner with yellow on the left
        1: 1,  # 1 colour on top, you position cube so UFL corner has yellow on top
        2: 0  # 2 colours on top, you position cube so UFL corner has yellow facing
    }
    colour = type_index[cross_type]

    while cubeobj.cube[2][colour] != cubeobj.top:
        cubeobj.cube_move('U')

    return


def _is_oll_complete(cubeobj: cube.Cube) -> bool:
    # positions of top side
    topside = (0, 1, 2, 3, 8, 9, 10, 11)

    for piece in topside:
        if cubeobj.cube[piece][1] != cubeobj.top:
            return False

    return True
