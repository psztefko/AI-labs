import csv
import random
import sys
from typing import List

#
# def load_data(path):
#     list_of_rows = []
#     with open(path, newline='') as file:
#         csv_reader = csv.reader(file, delimiter=' ')
#         for row in csv_reader:
#             list_of_rows.append(row)
#
#     return list_of_rows
#
#
# def create_distances_matrix(list_of_rows):
#     matrix = [[None] * INDIVIDUAL_SIZE for _ in range(INDIVIDUAL_SIZE)]
#     for i in range(INDIVIDUAL_SIZE):
#         for j in range(INDIVIDUAL_SIZE):
#             if j <= i:
#                 matrix[i][j] = int(list_of_rows[i + 1][j])
#             else:
#                 matrix[i][j] = int(list_of_rows[j + 1][i])
#     return matrix

def load_data(path: str, delimiter=" ") -> List[List[str]]:
    with open(path, newline="") as file:
        return [
            list(filter(None, row)) for row in csv.reader(file, delimiter=delimiter)
        ]


def create_distances_matrix(data: List[List[int]]) -> List[List[int]]:
    size = int(data[0][0])
    matrix = [[None] * size for _ in range(size)]
    for x in range(size):
        for y in range(size):
            try:
                matrix[x][y] = int(data[x + 1][y])
            except IndexError:
                matrix[x][y] = int(data[y + 1][x])
    return matrix

def generate_population_array():
    array = []
    population = []
    for i in range(INDIVIDUAL_SIZE):
        array.append(i)
    for i in range(POPULATION_SIZE):
        random.shuffle(array)
        population.append(array[:])
    return population


def count_population_scores(population) -> List:
    scores_array = []
    for i in range(POPULATION_SIZE):
        sum = 0
        for j in range(INDIVIDUAL_SIZE):
            index = population[i % INDIVIDUAL_SIZE][j]
            sum += DISTANCE_MATRIX[i % INDIVIDUAL_SIZE][index]
        scores_array.append(sum)
    return scores_array


def find_best_score(population):
    best_score = sys.maxsize

    for i in range(POPULATION_SIZE):
        tempScore = 0
        for j in range(INDIVIDUAL_SIZE):
            index = population[i % INDIVIDUAL_SIZE][j]
            tempScore += DISTANCE_MATRIX[i % INDIVIDUAL_SIZE][index]
        if tempScore < best_score:
            best_score = tempScore
    return best_score


def tournament_selection(population, scores) -> List:
    best_individual = []
    best_score = sys.maxsize

    random_indexes = random.sample(
        range(0, POPULATION_SIZE), SELECTIVE_PRESSURE)

    for index in random_indexes:
        if scores[index] < best_score:
            best_individual = population[index]
            best_score = scores[index]

    return best_individual


def single_point_crossover(individual_a: List, individual_b: List):
    x = random.randint(0, INDIVIDUAL_SIZE)

    new_individual_a = individual_a[:x] + individual_b[x:]
    new_individual_b = individual_b[:x] + individual_a[x:]

    return new_individual_a, new_individual_b


def make_single_point_crossover(population: List):
    for i in range(0, INDIVIDUAL_SIZE - 1, 2):
        population[i], population[i + 1] = single_point_crossover(population[i], population[i + 1])


def inversion_mutation(individual):
    rand = random.randint(0, int(INDIVIDUAL_SIZE * MUTATION_RATE))
    x = random.randint(0, rand)
    y = random.randint(x, INDIVIDUAL_SIZE)

    new_individual = []
    new_individual.extend(individual[y:])
    new_individual.extend(individual[x:y])
    new_individual.extend(individual[:x])

    return new_individual


def perform_mutation(population):
    for i in range(POPULATION_SIZE):
        population[i] = inversion_mutation(population[i])


def get_random_index(min: int, max: int) -> int:
    """Inclusive for both min and max"""
    return random.randint(min, max)


def tsa(population):
    scores = count_population_scores(population)

    for i in range(0, POPULATION_SIZE):
        population[i] = tournament_selection(population, scores)

    make_single_point_crossover(population)

    perform_mutation(population)

    return population


list_of_rows = load_data('berlin52.txt')
INDIVIDUAL_SIZE = int(list_of_rows[0][0])
POPULATION_SIZE = 250
MUTATION_PROBABILITY = 0.05
SELECTIVE_PRESSURE = 3
DISTANCE_MATRIX = create_distances_matrix(list_of_rows)
EPOCHS = 10000
MUTATION_RATE = 0.03

population = generate_population_array()
best_score = sys.maxsize
for i in range(EPOCHS):

    population = tsa(population)
    current_score = find_best_score(population)
    if current_score < best_score:
        best_score = current_score
    print(f'Generation: ', i + 1)
    print(f'Score: ', best_score)

print(f'Best score: ', best_score)