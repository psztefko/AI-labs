import csv
import random


def load_data(path):
    list_of_rows = []
    with open(path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            list_of_rows.append(row)

    return list_of_rows

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
        random.shuffle(array)
        population.append(array[:])
    return population

def count_population_score(matrix, population):
    scores_array = []
    for i in range(SIZE):
        sum = 0
        for j in range(SIZE):
            index = population[i][j]
            sum += matrix[i][index]
        scores_array.append(sum)
    return scores_array


list_of_rows = load_data('test.txt')

SIZE = int(list_of_rows[0][0])

matrix = create_matrix(list_of_rows)

population = generate_population_array()

count_population_score(matrix, population)

