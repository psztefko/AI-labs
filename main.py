import csv
import random


def load_data(path):
    list_of_rows = []
    with open(path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            list_of_rows.append(row)

    return list_of_rows


list_of_rows = load_data('test.txt')

SIZE = int(list_of_rows[0][0])


def create_matrix(list_of_rows):
    matrix = [[None] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        for j in range(SIZE):
            if j <= i:
                matrix[i][j] = int(list_of_rows[i + 1][j])
            else:
                matrix[i][j] = int(list_of_rows[j + 1][i])
    return matrix


def generate_population_array():
    array = []
    population = []
    for i in range(SIZE):
        array.append(i)
    for i in range(SIZE):
        population.append(random.shuffle(array))
    return population

matrix = create_matrix(list_of_rows)



# for row in matrix:
#     print(row)
