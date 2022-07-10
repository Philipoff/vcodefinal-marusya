from random import randint


def find_food(matrix, n=12):
    food_found = False
    food = (0, 0)
    for y in range(n):
        for x in range(n):
            if matrix[y][x] == 2:
                food = (y, x)
                food_found = True
                break
        if food_found:
            break
    return food


def create_matrix(n=12):
    matrix = [[0 for i in range(n)] for j in range(n)]
    matrix[5][5] = 1
    matrix[5][6] = 3
    y, x = randint(0, n - 1), randint(0, n - 1)
    y = 4
    x = 7
    while (y, x) in ((5, 5), (5, 6)):
        y, x = randint(0, n - 1), randint(0, n - 1)
    matrix[y][x] = 2
    return matrix


def move_up(matrix, body, score, n=12):
    food = find_food(matrix)
    if body[-2] == ((body[-1][0] - 1) % n, body[-1][1]):
        return [], [], 0, "Wrong direction"
    if matrix[(body[-1][0] - 1) % n][body[-1][1]] == 2:
        body.append(((body[-1][0] - 1) % n, body[-1][1]))
        score += 1
        y, x = randint(0, n - 1), randint(0, n - 1)
        while (y, x) in body:
            y, x = randint(0, n - 1), randint(0, n - 1)
        food = (y, x)
        print(y, x)
        matrix[(body[-1][0] - 1) % n][body[-1][1]] = 1
        matrix[y][x] = 2
    elif matrix[(body[-1][0] - 1) % n][body[-1][1]] == 1:
        return [], [], 0, "Collision"
    elif matrix[(body[-1][0] - 1) % n][body[-1][1]] == 0:
        body.append(((body[-1][0] - 1) % n, body[-1][1]))
        body = body[1:]
    matrix = draw_matrix(matrix, body, food)
    return matrix, body, score, ""


def move_down(matrix, body, score, n=12):
    food = find_food(matrix)
    if body[-2] == ((body[-1][0] + 1) % n, body[-1][1]):
        return [], [], 0, "Wrong direction"
    if matrix[(body[-1][0] + 1) % n][body[-1][1]] == 2:
        body.append(((body[-1][0] + 1) % n, body[-1][1]))
        score += 1
        y, x = randint(0, n - 1), randint(0, n - 1)
        while (y, x) in body:
            y, x = randint(0, n - 1), randint(0, n - 1)
        food = (y, x)
        matrix[(body[-1][0] + 1) % n][body[-1][1]] = 1
        matrix[y][x] = 2
    elif matrix[(body[-1][0] + 1) % n][body[-1][1]] == 1:
        return [], [], 0, "Collision"
    elif matrix[(body[-1][0] + 1) % n][body[-1][1]] == 0:
        body.append(((body[-1][0] + 1) % n, body[-1][1]))
        body = body[1:]
    matrix = draw_matrix(matrix, body, food)
    return matrix, body, score, ""


def move_right(matrix, body, score, n=12):
    food = find_food(matrix)
    if body[-2] == (body[-1][0], (body[-1][1] + 1) % n):
        return [], [], 0, "Wrong direction"
    if matrix[body[-1][0]][(body[-1][1] + 1) % n] == 2:
        body.append((body[-1][0], (body[-1][1] + 1) % n))
        score += 1
        y, x = randint(0, n - 1), randint(0, n - 1)
        while (y, x) in body:
            y, x = randint(0, n - 1), randint(0, n - 1)
        food = (y, x)
        matrix[body[-1][0]][(body[-1][1] + 1) % n] = 1
        matrix[y][x] = 2
    elif matrix[body[-1][0]][(body[-1][1] + 1) % n] == 1:
        return [], [], 0, "Collision"
    elif matrix[body[-1][0]][(body[-1][1] + 1) % n] == 0:
        body.append((body[-1][0], (body[-1][1] + 1) % n))
        body = body[1:]
    matrix = draw_matrix(matrix, body, food)
    return matrix, body, score, ""

# 11 0
# 11 11
def move_left(matrix, body, score, n=12):
    food = find_food(matrix)
    if body[-2] == (body[-1][0], (body[-1][1] - 1) % n):
        return [], [], 0, "Wrong direction"
    if matrix[body[-1][0]][(body[-1][1] - 1) % n] == 2:
        body.append((body[-1][0], (body[-1][1] - 1) % n))
        score += 1
        y, x = randint(0, n - 1), randint(0, n - 1)
        while (y, x) in body:
            y, x = randint(0, n - 1), randint(0, n - 1)
        food = (y, x)
        matrix[body[-1][0]][(body[-1][1] - 1) % n] = 1
        matrix[y][x] = 2
    elif matrix[body[-1][0]][(body[-1][1] - 1) % n] == 1:
        return [], [], 0, "Collision"
    elif matrix[body[-1][0]][(body[-1][1] - 1) % n] == 0:
        body.append((body[-1][0], (body[-1][1] - 1) % n))
        body = body[1:]
    matrix = draw_matrix(matrix, body, food)
    return matrix, body, score, ""


def draw_matrix(matrix, body, food, n=12):
    print(body)
    matrix = [[0 for i in range(n)] for j in range(n)]
    for i in body:
        matrix[i[0]][i[1]] = 1
    matrix[body[-1][0]][body[-1][1]] = 3
    matrix[food[0]][food[1]] = 2
    return matrix
