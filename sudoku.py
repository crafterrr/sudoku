def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
                      ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    grid = []
    previousrow = -1
    for i in range(0, len(values)):
        if i // n > previousrow:
            grid.append([])
            previousrow += 1
        grid[i // n].append(values[i])
    return grid


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return values[row]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']], (0, 1))
    ['2', '5', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [row[pos[1]] for row in values]


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    row, col = pos
    row //= 3
    col //= 3
    block = []
    for rowadd in range(row * 3, row * 3 + 3):
        for coladd in range(col * 3, col * 3 + 3):
            block.append(values[rowadd][coladd])
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    pos = (-1, -1)
    for row in range(0, len(grid)):
        for col in range(0, len(grid[row])):
            if grid[row][col] == '.':
                pos = row, col
                return pos
    if pos == (-1, -1):
        return False


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции """
    values = []
    block = get_block(grid, pos)
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    for i in range(1, 10):
        isok = True
        for rowy in range(0, len(block)):
            for coly in range(0, len(block[rowy])):
                if str(i) == block[rowy][coly]:
                    isok = False
        for index in range(0, len(row)):
            if str(i) == row[index]:
                isok = False
        for index in range(0, len(col)):
            if str(i) == col[index]:
                isok = False
        if isok is True:
            values.append(str(i))
    row, col = pos
    if grid[row][col] != '.':  # Для функции check_solution
        values.append(grid[row][col])
    return values


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения,
           которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    pos = find_empty_positions(grid)
    if pos is False:
        return grid
    row, col = pos
    values = find_possible_values(grid, pos)
    # print(row, col, values)
    for i in values:
        grid[row][col] = i
        if solve(grid) is not False:
            return grid
        grid[row][col] = '.'
    return False


def check_solution(solution):
    """ Если решение solution верно,
     то вернуть True, в противном случае False """
    for row in range(0, len(solution)):
        for col in range(0, len(solution[row])):
            if find_possible_values(solution, (row, col))[0] \
                    != solution[row][col]:
                return False
    return True

import random
def generate_sudoku(N):
    grid = [['.' for i in range(0, 9)] for i in range(0, 9)]
    for i in range(0, 3, 2):
        for j in range(0, 3, 2):
            for t in range(0, 1):
                row = random.randrange(3 * i, 3 * (i + 1))
                col = random.randrange(3 * j, 3 * (j + 1))
                values = find_possible_values(grid, (row, col))
                grid[row][col] = values[random.randrange(0, len(values))]
    row = random.randrange(3, 6)
    col = random.randrange(3, 6)
    values = find_possible_values(grid, (row, col))
    grid[row][col] = values[random.randrange(0, len(values))]
    solve(grid)
    i = 0
    while i < (81 - N):
        row = random.randrange(0, 9)
        col = random.randrange(0, 9)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            i += 1
    return grid


# if __name__ == '__main__':
    # grid = generate_sudoku(40)
    # display(grid)
    # solve(grid)
    # print(grid)

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solve(grid)
        display(grid)
        # print(check_solution(solution))
