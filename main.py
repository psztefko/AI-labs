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


def tournament_selection(population, scores, selection_pressure=3) -> List:
    best_individual = []
    best_score = sys.maxsize

    random_indexes = random.sample(
        range(0, POPULATION_SIZE), selection_pressure)

    for index in random_indexes:
        if scores[index] < best_score:
            best_individual = population[index]

    return best_individual


def crossover(individual1, individual2):

    p1 = individual1
    p2 = individual2

    cxpoint1 = random.randint(0, INDIVIDUAL_SIZE)
    cxpoint2 = random.randint(0, INDIVIDUAL_SIZE - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # Swap the two cx points
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        # Keep track of the selected values
        temp1 = individual1[i]
        temp2 = individual2[i]
        # Swap the matched value
        individual1[i], individual1[p1[temp2]] = temp2, temp1
        individual2[i], individual2[p2[temp1]] = temp1, temp2
        # Position bookkeeping
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return individual1, individual2


def single_point_crossover(individualA: List, individualB: List):
    x = random.randint(0, INDIVIDUAL_SIZE)

    new_individualA = individualA[:x] + individualB[x:]
    new_individualB = individualB[:x] + individualA[x:]

    return new_individualA, new_individualB


def makeSinglePointCrossover(population: List):
    for i in range(0, INDIVIDUAL_SIZE - 1, 2):
        population[i], population[i +
                                  1] = single_point_crossover(population[i], population[i+1])


def perform_mutation(individual, mutation_rate=0.3):
    if random.random() < MUTATION_RATE:
        subversion_indexes = random.sample(
            range(0, INDIVIDUAL_SIZE), 2)
        individual[subversion_indexes[0]], individual[subversion_indexes[1]] = individual[subversion_indexes[1]], individual[subversion_indexes[0]]

    return individual


def tsa(population):
    scores = count_population_scores(population)

    for i in range(0, POPULATION_SIZE):
        population[i] = tournament_selection(population, scores)

    makeSinglePointCrossover(population)

    for i in range(0, POPULATION_SIZE):
        population[i] = perform_mutation(population[i])

    return population


list_of_rows = load_data('berlin52.txt')
INDIVIDUAL_SIZE = int(list_of_rows[0][0])
POPULATION_SIZE = 200
MUTATION_RATE = 0.6
SELECTION_PRESSURE = 3
DISTANCE_MATRIX = create_distances_matrix(list_of_rows)

population = generate_population_array()

for i in range(100):

    population = tsa(population)

    print(f'Generation: ', i + 1)
    print(f'Score: ', find_best_score(population))