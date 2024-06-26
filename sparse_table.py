from typing import Callable

"""
Sparse Table - builds a sparse table based on the given values and desired function (a callable that takes 2 params).
Function needs to be associative and can be specified to be idempotent or not. For example, RMQ (min) is idempotent
whereas Addition is not. Behaviour is the same either way, but the former is more efficient in time complexity.
"""


class SparseTable:
    def __init__(self, values: list, func: Callable, is_func_idempotent: bool = False):
        self._n = len(values)
        self._k = self._n.bit_length() - 1
        self._st = [[values[i] for i in range(self._n)] for _ in range(self._k + 1)]
        self._func = func
        self._idempotent = is_func_idempotent
        self._initialize_st()

    def _initialize_st(self):
        prev_power = 1
        curr_power = 2
        for i in range(1, self._k + 1):
            for j in range(self._n - curr_power + 1):
                self._st[i][j] = self._func(self._st[i - 1][j], self._st[i - 1][j + prev_power])

            prev_power = curr_power
            curr_power *= 2  # Assuming this is less than 30-bit, this is more optimized in CPython than bit-shifting

    # l and r are inclusive indices
    def query(self, l: int, r: int):
        if l == r:
            return self._st[0][l]

        query_size = (r - l + 1).bit_length()
        power = 1 << (query_size - 1)  # Using pow function is likely faster here, but this avoids extra func/import

        if self._idempotent:
            return self._func(self._st[query_size - 1][l], self._st[query_size - 1][r - power + 1])

        if l + power - 1 == r:
            return self._st[query_size - 1][l]
        else:
            return self._func(self._st[query_size - 1][l], self.query(l + power, r))
