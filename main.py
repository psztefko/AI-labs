import csv
import random
import sys
from typing import List


def load_data(path):
    list_of_rows = []
    with open(path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            list_of_rows.append(row)

    return list_of_rows


def create_distances_matrix(list_of_rows):
    matrix = [[None] * INDIVIDUAL_SIZE for _ in range(INDIVIDUAL_SIZE)]
    for i in range(INDIVIDUAL_SIZE):
        for j in range(INDIVIDUAL_SIZE):
            if j <= i:
                matrix[i][j] = int(list_of_rows[i + 1][j])
            else:
                matrix[i][j] = int(list_of_rows[j + 1][i])
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


def count_population_scores(population: List) -> List:
    scores = []
    for individual in population:
        sum = 0
        for i in range(INDIVIDUAL_SIZE - 1):
            sum += DISTANCE_MATRIX[individual[i]][individual[i + 1]]
        sum += DISTANCE_MATRIX[individual[-1]][individual[0]]
        scores.append(sum)

    return scores


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


def add_at_first_found_none(l: List[any], value: any) -> List[any]:
    """If there is None in the list, return list with value at first found None"""
    for i, ele in enumerate(l):
        if ele is None:
            l[i] = value
            return l


def crossover(individual1, individual2):

    a, b = random.sample(range(INDIVIDUAL_SIZE), 2)
    if a > b:
        a, b = b, a

    lefts = individual1[:a], individual2[:a]
    middles = individual1[a:b], individual2[a:b]
    rights = individual1[b:], individual2[b:]

    children = [[None] * INDIVIDUAL_SIZE, [None] * INDIVIDUAL_SIZE]
    for i, c in enumerate(children):
        c[a:b] = middles[i]

    work_lists = [rights[i] + lefts[i] + middles[i] for i in range(2)]
    work_lists.reverse()

    for i, child in enumerate(children):
        for j in range(INDIVIDUAL_SIZE):
            if work_lists[i][j] in child:
                continue
            else:
                add_at_first_found_none(child, work_lists[i][j])
    return individual1, individual2


def inversion_mutation(individual):

    x = random.randint(0, INDIVIDUAL_SIZE - 1)
    y = random.randint(0, INDIVIDUAL_SIZE)

    if x >= y:
        y = x + 1

    new_individual = []
    new_individual.extend(individual[y:])
    new_individual.extend(individual[x:y])
    new_individual.extend(individual[:x])

    return new_individual


def tsa(population):

    scores = count_population_scores(population)

    population = [tournament_selection(population, scores) for _ in range(POPULATION_SIZE)]

    for i in range(0, POPULATION_SIZE - 1, 2):
        if random.uniform(0, 1) > 0.75:
            temp_tuple = (crossover(population[i], population[i + 1]))
            population[i] = temp_tuple[0]
            population[i + 1] = temp_tuple[1]

    population = [inversion_mutation(individual) for individual in population]

    return population


list_of_rows = load_data('berlin52.txt')
INDIVIDUAL_SIZE = int(list_of_rows[0][0])
POPULATION_SIZE = 200
MUTATION_PROBABILITY = 0.05
SELECTIVE_PRESSURE = 5
DISTANCE_MATRIX = create_distances_matrix(list_of_rows)
EPOCHS = 10000

population = generate_population_array()

best_score = sys.maxsize
for i in range(EPOCHS):

    population = tsa(population)
    scores = count_population_scores(population)
    for score_index in range(len(scores)):
        if scores[score_index] < best_score:
            best_score = scores[score_index]

    print(f'Generation: ', i + 1)
    print(f'Score: ', best_score)

print(f'Best score: ', best_score)
