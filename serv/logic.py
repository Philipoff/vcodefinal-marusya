import random


def create_matrix():
    matrix = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    return matrix[:][:]


def generate_new_num(matrix):
    empty_cells = []
    for y in range(4):
        for x in range(4):
            if matrix[y][x] == 0:
                empty_cells.append((y, x))
    if empty_cells:
        y, x = random.choice(empty_cells)
        matrix[y][x] = 2
        if random.random() <= 0.1:
            matrix[y][x] = 4
    return matrix[:][:]


def row_left_swipe(row, score):
    if sum(row) == 0:
        return row[:], score

    # stage 1: remove zeroes
    new_row = []
    for i in range(4):
        if row[i] != 0:
            new_row.append(row[i])
    new_row += [0] * (4 - len(new_row))

    # stage 2: merging tiles
    for i in range(3):
        if new_row[i] == new_row[i + 1]:
            new_row[i] = new_row[i] * 2
            score += new_row[i]
            new_row.pop(i + 1)
            new_row.append(0)

    return new_row[:], score


def swipe_left(matrix, score):
    for i in range(4):
        matrix[i], score = row_left_swipe(matrix[i], score)

    return matrix[:][:], score


def rotate_ccw(matrix, score):
    new_matrix = [[0] * 4 for _ in range(4)]

    for row in range(4):
        for col in range(4):
            new_matrix[col][3 - row] = matrix[row][col]
    return new_matrix[:][:], score


def rotate_cw(matrix, score):
    for i in range(3):
        matrix, score = rotate_ccw(matrix, score)
    return matrix[:][:], score


rotate_count = {
    "влево": 0,
    "вверх": 3,
    "вправо": 2,
    "вниз": 1
}


def swipe(matrix, direction, score):
    rotates = rotate_count[direction]

    for i in range(rotates):
        matrix, score = rotate_ccw(matrix, score)

    matrix, score = swipe_left(matrix, score)

    for i in range(rotates):
        matrix, score = rotate_cw(matrix, score)

    return matrix[:][:], score


def is_move_is_impossible(matrix, score):
    return matrix[:][:] == swipe(matrix, "влево", score)[0] and matrix[:][:] == swipe(matrix, "вправо", score)[
        0] and matrix[:][:] == swipe(matrix, "вниз", score)[0] and matrix[:][:] == swipe(matrix, "вверх", score)[0]
