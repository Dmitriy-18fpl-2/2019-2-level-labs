"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if type(num_rows) == int and type(num_cols) == int:
        global edit_matrix
        edit_matrix = [[0] * num_cols for i in range(num_rows)]
        print(edit_matrix)
        return edit_matrix
    else:
        edit_matrix = []
        return edit_matrix


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if type(add_weight) != int or type(remove_weight) != int:
        print('error')
        return list(edit_matrix)
    if edit_matrix == []:
        print('error')
        return list(edit_matrix)
    for i in edit_matrix:
        if i == []:
            print('error')
            return list(edit_matrix)
    else:
        for i in range(1, len(edit_matrix[0])):
            edit_matrix[0][i] = edit_matrix[0][i - 1] + add_weight
        for i in range(len(1, edit_matrix)):
            edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight
        return list(edit_matrix)


def minimum_value(numbers: tuple) -> int:
    min_number = min(numbers)
    return min_number


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if type(original_word) != str or type(target_word) != str:
        print('error')
        return list(edit_matrix)
    if type(add_weight) != int or type(remove_weight) != int or type(substitute_weight) != int:
        print('error')
        return list(edit_matrix)
    if edit_matrix == ():
        print('error')
        edit_matrix = []
        return edit_matrix
    if len(edit_matrix) == 1:
        return list(edit_matrix)
    else:
        for i in range(len(edit_matrix)):
            if edit_matrix[i] == []:
                print('error')
                return list(edit_matrix)
            if len(edit_matrix[i]) == 1:
                return list(edit_matrix)
        for i in range(1, len(edit_matrix)):
            for j in range(1, len(edit_matrix[i])):
                num_1 = edit_matrix[i - 1][j] + remove_weight
                num_2 = edit_matrix[i][j - 1] + add_weight
                if original_word[i - 1] == target_word[j - 1]:
                    num_3 = edit_matrix[i - 1][j - 1] + 0
                else:
                    num_3 = edit_matrix[i - 1][j - 1] + substitute_weight
                numbers = (num_1, num_2, num_3)
                edit_matrix[i][j] += minimum_value(numbers)
        return list(edit_matrix)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    num_rows = len(original_word) + 1
    num_cols = len(target_word) + 1
    generate_edit_matrix(num_rows, num_cols)
    initialize_edit_matrix(edit_matrix, add_weight, remove_weight)
    fill_edit_matrix(edit_matrix, add_weight, remove_weight, substitute_weight, original_word, target_word)
    the_number = edit_matrix[len(edit_matrix) - 1][len(edit_matrix[0]) - 1]
    return the_number


def save_to_csv(edit_matrix):
    with open('file.csv', 'w') as f:
        for i in range(len(edit_matrix)):
            counter = 0
            for j in edit_matrix[i]:
                counter += 1
                if counter == len(edit_matrix[i]):
                    f.write(str(j) + '\n')
                else:
                    f.write(str(j) + ';')
    return None


def load_from_csv(path_to_file):
    with open(path_to_file, 'r') as f:
        almost_matrix = f.read()
    edit_matrix = [[]]
    counter = 0
    for i in almost_matrix:
        if i == '\n':
            edit_matrix.append([])
            counter += 1
            continue
        if i == ';':
            continue
        else:
            edit_matrix[counter].append(int(i))
    edit_matrix.pop()
