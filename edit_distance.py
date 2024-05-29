from typing import Sequence


def edit_distance(a: Sequence, b: Sequence) -> int:
    a_len = len(a)
    b_len = len(b)

    if a_len == 0 or b_len == 0:
        return max(a_len, b_len)

    # Reduces memory footprint to the shorter of the two sequences
    if a_len < b_len:
        return edit_distance(b, a)

    m0 = [x for x in range(b_len+1)]
    m1 = [0] * (b_len+1)

    for i in range(1, a_len+1):
        m1[0] = i

        for j in range(1, b_len+1):
            sub_cost = 0 if a[i-1] == b[j-1] else 1
            m1[j] = min(m1[j-1]+1, m0[j]+1, m0[j-1] + sub_cost)

        m0 = m1[::]

    return m1[-1]
