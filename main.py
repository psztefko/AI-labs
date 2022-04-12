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


# def count_population_scores(population) -> List:
#     scores_array = []
#     for i in range(POPULATION_SIZE):
#         sum = 0
#         for j in range(INDIVIDUAL_SIZE):
#             index = population[i % INDIVIDUAL_SIZE][j]
#             sum += DISTANCE_MATRIX[i % INDIVIDUAL_SIZE][index]
#         scores_array.append(sum)
#     return scores_array
#
#
# def find_best_score(population):
#     best_score = sys.maxsize
#
#     for i in range(POPULATION_SIZE):
#         tempScore = 0
#         for j in range(INDIVIDUAL_SIZE):
#             index = population[i % INDIVIDUAL_SIZE][j]
#             tempScore += DISTANCE_MATRIX[i % INDIVIDUAL_SIZE][index]
#         if tempScore < best_score:
#             best_score = tempScore
#
#     return best_score


def count_population_scores(population):
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


def tsa(population):
    scores = count_population_scores(population)

    # for i in range(0, POPULATION_SIZE):
    #     population[i] = tournament_selection(population, scores)



    tournament_winners = [tournament_selection(population, scores) for _ in range(POPULATION_SIZE)]


    for i in range(0, len(population) - 1, 2):
        temp_tuple = (crossover(tournament_winners[i], tournament_winners[i + 1]))
        population[i] = temp_tuple[0]
        population[i + 1] = temp_tuple[1]



    #make_single_point_crossover(population)
    perform_mutation(population)

    return population


list_of_rows = load_data('berlin52.txt')
INDIVIDUAL_SIZE = int(list_of_rows[0][0])
POPULATION_SIZE = 200
MUTATION_PROBABILITY = 0.05
MUTATION_RATE = 0.03
SELECTIVE_PRESSURE = 20
DISTANCE_MATRIX = create_distances_matrix(list_of_rows)
EPOCHS = 1000


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

    # print(f'Osobnik: ', population[i])
    # print(f'Długość: ', len(population[i]))

print(f'Best score: ', best_score)


# if(len(set(individual)) == len(individual)):
#    print("All elements are unique.")
# else:
#    print("All elements are not unique.")