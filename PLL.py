import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
import cube


def pll(cubeobj: cube.Cube):
    solved_cube = cube.Cube()
    permute_corners(cubeobj)
    permute_edges(cubeobj)

    # will be solved but may not have the top layer lining up with the rest of the cube
    while cubeobj != solved_cube:
        cubeobj.cube_move('U')


################################ PERMUTE CORNERS ################################

# keep performing corner permutation algorithm until all corners are solved
def permute_corners(cubeobj: cube.Cube):
    while not _check_all_corners(cubeobj):
        _position_corners(cubeobj)
        cubeobj.perform_algorithm("R' F R' B2 R F' R' B2 R2")


# position top layer so that correctly permuted corners (if any) are at the back
def _position_corners(cubeobj: cube.Cube):
    for _ in range(4):
        if _check_corners(cubeobj):
            break
        else:
            cubeobj.cube_move('U')


# check if all corners are permuted correctly
def _check_all_corners(cubeobj: cube.Cube):
    # if back and front corners work, then all corners match
    back = _check_corners(cubeobj)
    cubeobj.cube_move('U2')
    front = _check_corners(cubeobj)
    return back and front


# check if back corners are permuted correctly
def _check_corners(cubeobj):
    return cubeobj.cube[0][0] == cubeobj.cube[1][0]


################################ PERMUTE EDGES ################################

# permute all edges of the top layer
def permute_edges(cubeobj: cube.Cube()):
    leftward = "F2 U R' L F2 R L' U F2"
    rightward = "F2 U' R' L F2 R L' U' F2"
    while not _check_all_edges(cubeobj):
        _position_edges(cubeobj)
        # use the leftward algorithm
        if _find_direction(cubeobj):
            cubeobj.perform_algorithm(leftward)

        # use the rightward algorithm
        else:
            cubeobj.perform_algorithm(rightward)


# position top layer so that if any edge is permuted correctly, it is at the back
def _position_edges(cubeobj: cube.Cube) -> None:
    # if top and back corners and edge match colours
    for _ in range(4):
        if _check_edges(cubeobj):
            break
        else:
            cubeobj.cube_move('U')


# check if back edge is permuted correctly
def _check_edges(cubeobj) -> bool:
    return cubeobj.cube[0][0] == cubeobj.cube[1][0] == cubeobj.cube[9][0]


# check if all edges are permuted correctly
def _check_all_edges(cubeobj: cube.Cube) -> bool:
    back = _check_edges(cubeobj)
    cubeobj.cube_move('U2')
    front = _check_edges(cubeobj)
    return back and front


# check if edge colour facing you is the same as the corners on the left ->>>> TRUE = Go left, FALSE = Go right
def _find_direction(cubeobj: cube.Cube) -> bool:
    return cubeobj.cube[11][0] == cubeobj.cube[0][2] == cubeobj.cube[2][2]
