import itertools
from pathlib import Path
import sys

import numpy as np


def is_correct(arr, *, auxiliary):
    # let V be a set of elements from 1 to 2n

    # each pair of elements from V is contained in exactly one cell
    all_pairs = set()
    for row, col in constants.row_col_iter:
        pair = arr[row, col]
        all_pairs.add(tuple(sorted(pair)))
    if all_pairs != constants.all_pairs:
        return False

    # all pairs satisfy starter requirement
    for row, col in constants.row_col_iter:
        first_number, second_number = arr[row, col]
        difference = (second_number - first_number) % constants.modulo
        if difference != row + 1:
            return False

    # each column consists of all elements of V
    for col in constants.columns:
        col_numbers = set(itertools.chain.from_iterable(arr[:, col]))
        if col_numbers != constants.all_numbers:
            return False

    # each element is contained at most two times in each row
    for row in constants.rows:
        row_numbers = list(itertools.chain.from_iterable(arr[row, :]))
        counters = [row_numbers.count(i) for i in constants.all_numbers]
        if max(counters) > 2:
            return False
    return True


class Constants:
    def __init__(self, N):
        self.N = N
        self.modulo = 2 * N + 1
        self.n_teams = 2 * N
        # number 4 is taken from config.py
        # self.string = f'S{self.n_teams:04d}'
        self.string = f'SBTD{self.N:04d}'
        self.all_numbers = set(range(1, self.modulo))
        self.array_shape = (N, 2 * N - 1)
        self.columns = range(2 * N - 1)
        self.rows = range(N)
        self.row_col_iter = tuple(itertools.product(self.rows, self.columns))
        self.all_pairs = set(itertools.combinations(self.all_numbers, r = 2))
        return None


try:
    max_N = int(sys.argv[1])
except Exception:
    max_N = 54
possible_N_values = [val for val in range(4, max_N + 1) if val != 5]
for N in possible_N_values:
    constants = Constants(N)
    folder = Path() / constants.string
    solution_files = list(folder.iterdir())
    for file in solution_files:
        with open(file, 'r') as f:
            data = f.readlines()
        arr = np.empty(constants.array_shape, dtype = tuple)
        for i, line in enumerate(data):
            for char in ['(', ')', '[', ']']:
                line = line.replace(char, '')
            values = [int(x) for x in line.split(',')]
            arr[i] = list(zip(values[0::2], values[1::2]))
        if not is_correct(arr, auxiliary = constants):
            raise ValueError(f'A wrong solution\n{arr}')
    n_solutions = len(solution_files)
    if n_solutions != 0:
        print(f'SBTD({N:2d}): {n_solutions:4d} solution(s).')
    else:
        print(f'SBTD({N:2d}): No solutions found.')
print('\nNo errors raised, hence all solutions found are correct.')
