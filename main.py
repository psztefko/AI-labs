import csv



def load_data(path):
    list_of_rows = []
    with open(path, newline='') as file:
        csv_reader = csv.reader(file, delimiter=' ')
        for row in csv_reader:
            list_of_rows.append(row)
            #print(row)

    return list_of_rows

list_of_rows = load_data('test.txt')

first_row = list_of_rows[0][0]


def create_matrix(list_of_rows):
    size = int(list_of_rows[0][0])
    matrix = [[None] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if j <= i:
                matrix[i][j] = list_of_rows[i + 1][j]
            else:
                matrix[i][j] = list_of_rows[j + 1][i]
    return matrix

matrix = create_matrix(list_of_rows)

print(matrix)