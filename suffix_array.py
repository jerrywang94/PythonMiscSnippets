from typing import Sequence


# Generate suffix array using SA-IS (Suffix Array - Induced Sorting); simple version, memory not optimized
def suffix_array(s: Sequence) -> list[int]:
    n = len(s)
    if n <= 2:
        indices = sorted([(c, i) for i, c in enumerate(s)])
        return [i[1] for i in indices]

    sl_array = [True] * n  # False for s, True for l
    char_count = {}

    # Generate counts of each character which will provide the boundaries and calculate sl mapping
    for i in range(n-1, -1, -1):
        char_count[s[i]] = char_count.setdefault(s[i], 0) + 1

        if i == n-1 or s[i] > s[i+1]:
            sl_array[i] = True
        elif s[i] < s[i+1]:
            sl_array[i] = False

        else:
            sl_array[i] = sl_array[i+1]

    char_set = sorted([c for c in char_count.keys()])
    # Needs a sort of the character space to place them in lexicographical order, so technically adds a O(clogc) term
    char_rank = {c: r for r, c in enumerate(char_set)}
    num_c = len(char_set)
    sa = [-1] * n

    # Base case: place the position of the suffix in the SA at the position of its rank in the character set
    if num_c == n:
        for i in range(n):
            sa[char_rank.get(s[i])] = i

        return sa

    # Generate the boundaries of each character bucket
    position_array = [0] * num_c
    cnt = 0
    for i in range(num_c):
        position_array[i] = cnt
        cnt += char_count[char_set[i]]

    # Find all LMS: store in a list within a dict with the char as the key
    char_lms = {}
    lms_blocks = {}
    prev_lms = None
    for i in range(1, n):
        if sl_array[i-1] and not sl_array[i]:
            char_lms.setdefault(s[i], []).append(i)
            if prev_lms is not None:
                lms_blocks[prev_lms] = i + 1  # Make end boundary exclusive index
            prev_lms = i

    lms_blocks[prev_lms] = n

    # First pass - place all LMS into the SA
    _first_pass_fill_lms(char_set=char_set, char_lms=char_lms,
                         position_array=position_array, char_count=char_count, sa=sa)

    # Second pass - induced sort #1
    _second_pass_forward_induced_sort(s=s, sa=sa, position_array=position_array, char_rank=char_rank, sl_array=sl_array)

    # Third pass - induced sort #2 in reverse
    _third_pass_reverse_induced_sort(s=s, sa=sa, position_array=position_array, sl_array=sl_array, char_rank=char_rank)

    # Number the LMS, then recurse
    reduced_lms = [0] * len(lms_blocks)
    lms_block_mapping = {}
    prev_lms_block = None
    curr_number = 0
    for i in range(n):
        if sa[i] in lms_blocks.keys():
            # Handle the last LMS containing sentinel
            if lms_blocks[sa[i]] == n:
                lms_block_mapping[sa[i]] = curr_number
                curr_number += 1
                continue

            if prev_lms_block is None:
                lms_block_mapping[sa[i]] = curr_number
                prev_lms_block = (sa[i], lms_blocks[sa[i]])
                continue
            if s[sa[i]:lms_blocks[sa[i]]] == s[prev_lms_block[0]:prev_lms_block[1]]:
                lms_block_mapping[sa[i]] = curr_number
            else:
                curr_number += 1
                lms_block_mapping[sa[i]] = curr_number
                prev_lms_block = (sa[i], lms_blocks[sa[i]])

    recursion_correspondence = {}  # Need to map lms_block -> position in recursion array correspondence
    j = 0
    for i in range(n):
        if i in lms_block_mapping.keys():
            reduced_lms[j] = lms_block_mapping[i]
            recursion_correspondence[j] = i
            j += 1

    sorted_lms_blocks = suffix_array(reduced_lms)

    # Sort the LMS blocks
    sorted_lms = [0] * len(lms_blocks)
    for i in range(len(lms_blocks)):
        sorted_lms[i] = recursion_correspondence.get(sorted_lms_blocks[i])

    # Final pass
    sa = [-1] * n
    char_lms.clear()
    for lms in sorted_lms:
        char_lms.setdefault(s[lms], []).append(lms)

    _first_pass_fill_lms(char_set=char_set, char_lms=char_lms,
                         position_array=position_array, char_count=char_count, sa=sa)

    _second_pass_forward_induced_sort(s=s, sa=sa, position_array=position_array, char_rank=char_rank, sl_array=sl_array)

    _third_pass_reverse_induced_sort(s=s, sa=sa, position_array=position_array, sl_array=sl_array, char_rank=char_rank)

    return sa


def _first_pass_fill_lms(char_set: list, char_lms: dict, position_array: list, char_count: dict, sa: list):
    for i in range(len(char_set)):
        current_char = char_set[i]
        current_lms = char_lms.get(current_char, [])
        end = position_array[i] + char_count[current_char]
        n_lms = len(current_lms)

        for j in range(n_lms):
            sa[end - n_lms + j] = current_lms[j]


def _second_pass_forward_induced_sort(s: Sequence, sa: list, position_array: list, char_rank: dict, sl_array: list):
    # Since my implementation keeps the sentinel implicit, needs one explicit step to handle the sentinel at the start
    first_pass_pos = position_array.copy()  # Copy the original position array so we do not have to regenerate it later
    pre_sentinel_c = s[-1]
    sa[first_pass_pos[char_rank[pre_sentinel_c]]] = len(s) - 1
    first_pass_pos[char_rank[pre_sentinel_c]] += 1

    for i in range(len(s)):
        if sa[i] == -1:
            continue
        prev_ind = sa[i] - 1
        current_rank = char_rank[s[prev_ind]]
        if not sl_array[prev_ind]:
            continue
        sa[first_pass_pos[current_rank]] = prev_ind
        first_pass_pos[current_rank] += 1


def _third_pass_reverse_induced_sort(s: Sequence, sa: list, position_array: list, sl_array: list, char_rank: dict):
    second_pass_pos = position_array.copy()
    for i in reversed(range(len(s))):
        prev_ind = sa[i] - 1
        if sl_array[prev_ind]:
            continue
        current_rank = char_rank[s[prev_ind]]
        # Since we go in reverse and place items at the end of the bucket, we use the position of the
        # start of the bucket for the character in the next rank subtract one. Don't need to worry about the
        # character of the last rank since the nature of the SA means the last rank bucket only contains "L" suffixes.
        sa[second_pass_pos[current_rank+1]-1] = prev_ind
        second_pass_pos[current_rank + 1] -= 1


# Generates a longest common prefix array given a valid suffix array
def lcp_array(s: Sequence, sa: list[int]):
    n = len(s)
    lcp = [0] * (n-1)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    cnt = 0
    for i in range(n):
        if rank[i] == n-1:
            cnt = 0
            continue

        j = sa[rank[i] + 1]
        while i + cnt < n and j + cnt < n and s[i + cnt] == s[j + cnt]:
            cnt += 1

        lcp[rank[i]] = cnt
        if cnt > 0:
            cnt -= 1

    return lcp
