import csv
import random
import sys


def load_data(path):
    list_of_rows = []
    with open(path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            list_of_rows.append(row)

    return list_of_rows


def create_distances_matrix(list_of_rows):
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
    for i in range(POPULATION):
        random.shuffle(array)
        population.append(array[:])
    return population


def count_population_scores(matrix, population):
    scores_array = []
    for i in range(POPULATION):
        sum = 0
        for j in range(SIZE):
            index = population[i % 5][j]
            sum += matrix[i % 5][index]
        scores_array.append(sum)
    return scores_array


def selection(population, scores, selection_pressure=3):

    best_individual = []
    best_score = sys.maxsize

    random_indexes = random.sample(range(0, POPULATION), selection_pressure)

    for index in random_indexes:

        if scores[index] < best_score:
            best_individual = population[index]

    return best_individual


list_of_rows = load_data('test.txt')

SIZE = int(list_of_rows[0][0])

POPULATION = 200

distance_matrix = create_distances_matrix(list_of_rows)

population = generate_population_array()

scores = count_population_scores(distance_matrix, population)

selection(population, scores)
