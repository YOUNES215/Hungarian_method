# implementation of the Hungarian methode by YOUNES215

# requires the numpy package


import numpy as np

def phase1(cout_input):
    cout = cout_input.copy()

    for line in cout:
        minimum = min(line)
        for i, element in enumerate(line):
            line[i] -= minimum

    for colonne in cout.T:
        minimum = min(colonne)
        for j, element in enumerate(colonne):
            colonne[j] -= minimum

    return cout


def phase2(cout_input):
    cout = cout_input.copy()

    solution_found = False

    while np.any(cout == 0):

        zero_mirror = (cout == 0)

        num_zeros_line = zero_mirror.sum(axis=1)
        num_zeros_column = zero_mirror.sum(axis=0)

        valid = np.where(num_zeros_line > 0)[0]
        indices = valid[np.where(num_zeros_line[valid] == min(num_zeros_line[valid]))[0]]

        zero_barr = []
        for i in indices:
            for j in range(cout.shape[1]):
                if zero_mirror[i, j] == True:
                    zero_line = num_zeros_line[i] - 1
                    zero_colomn = num_zeros_column[j] - 1
                    zero_barr.append((zero_line + zero_colomn, i, j))

        _, x, y = min(zero_barr, key=lambda x: x[0])

        for i in range(cout.shape[0]):
            for j in range(cout.shape[1]):
                if cout[i, j] == 0:
                    if i == x and j == y:
                        cout[i, j] = -1
                    elif i == x or j == y:
                        cout[i, j] = -2

    if np.all(np.sum(cout == -1, axis=1) == 1) and \
            np.all(np.isin(np.argmax(cout == -1, axis=1), \
                           np.unique(np.argmax(cout == -1, axis=1)))):
        solution_found = True

    return cout, solution_found


def phase3(cout_input):
    cout = cout_input.copy()

    marked_lines = []
    marked_cols = []

    marked_lines = np.where(np.all(cout != -1, axis=1))[0].tolist()

    possible = True

    while possible:
        possible = False
        for line in cout[marked_lines]:
            for j, element in enumerate(line):
                if element == -2 and j not in marked_cols:
                    marked_cols.append(j)
                    possible = True
        for column in cout.T[marked_cols]:
            for i, element in enumerate(column):
                if element == -1 and i not in marked_lines:
                    marked_lines.append(i)
                    possible = True

    return cout, marked_lines, marked_cols


def phase4(cout_input, marked_lines, marked_cols):
    cout = cout_input.copy()

    cout[cout == -1] = 0
    cout[cout == -2] = 0

    dashed_lines = [i for i in range(cout.shape[0]) if i not in marked_lines]
    dashed_cols = sorted(marked_cols)

    non_dashed_lines = sorted(marked_lines)
    non_dashed_cols = [j for j in range(cout.shape[1]) if j not in marked_cols]

    if not non_dashed_lines or not non_dashed_cols:
        minimum = 0
    else:
        minimum = np.min(cout[np.ix_(non_dashed_lines, non_dashed_cols)])

    for i in range(cout.shape[0]):
        for j in range(cout.shape[1]):
            if i in non_dashed_lines and j in non_dashed_cols:
                cout[i][j] -= minimum
            elif i in dashed_lines and j in dashed_cols:
                cout[i][j] += minimum

    return cout


def phase5(cout_input, cout_initial):
    cout = cout_input.copy()

    cout_verification, solution_found = phase2(cout)

    if solution_found:
        solution = np.vstack(np.where(cout_verification == -1)) + 1
        solution_sum = np.sum(cout_initial[(cout_verification == -1)])

    else:
        solution = np.empty(0)
        solution_sum = None

    return cout, solution, solution_sum


def konig(init):
    cout_initial = np.array(init)
    cout = cout_initial.copy()

    solution = np.empty(0)
    solution_sum = 0

    cout = phase1(cout)
    cout, solution_found = phase2(cout)

    if solution_found:
        cout, solution, solution_sum = phase5(cout, cout_initial)
    else:
        while not solution.any():
            cout, solution_found = phase2(cout)
            cout, marked_lines, marked_cols = phase3(cout)
            cout = phase4(cout, marked_lines, marked_cols)
            cout, solution, solution_sum = phase5(cout, cout_initial)

    return cout, solution, solution_sum

# example:

# initial matrix:
cout_initial = [[ 86, 108, 100, 86,  87],
                [ 87, 105, 106, 86, 101],
                [ 88, 107,  98, 86,  92],
                [ 93, 110,  96, 93,  89],
                [106, 105,  97, 96, 103]]

cout_initial = np.array(cout_initial)

_, sol, sol_sum = konig(cout_initial)

print("the solution is:")
print(sol)
print("the sum of the solution is: " + str(sol_sum))
