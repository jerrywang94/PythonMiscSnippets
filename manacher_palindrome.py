# find_longest_palindrome: Returns the start, end indices of the longest palindrome in the string.
# Returns (0, 0) if string is empty or there are no palindromes found.
def find_longest_palindrome(s: str) -> tuple[int, int]:
    if len(s) < 2:
        return 0, 0

    all_palindromes = [_convert_to_indices(p, r) for p, r in enumerate(_manacher(s)) if r > 1]
    longest_len = 0
    best_candidate = (0, 0)
    for x0, x1 in all_palindromes:
        if x1 - x0 > longest_len:
            longest_len = x1 - x0
            best_candidate = (x0, x1)
    return best_candidate


# Runs Manacher's algorithm to output a result array where each entry is the radius of the longest
# possible palindrome centered at that position inclusive of the center character. This results
# array is a modified array representing the original string padded with implicit special characters in
# between each character of the original string to accommodate for even-length palindromes.
def _manacher(s: str) -> list[int]:
    total_len = (2 * len(s) - 1)
    res = [1] * total_len
    cursor = 0
    curr_radius = 1

    while cursor < total_len:

        while cursor - curr_radius >= 0 and cursor + curr_radius < total_len:
            if ((cursor - curr_radius) % 2 == 1 or
                    s[(cursor - curr_radius) // 2] == s[(cursor + curr_radius) // 2]):
                curr_radius += 1
            else:
                break

        res[cursor] = curr_radius

        for i in range(1, curr_radius):
            mirrored_radius = res[cursor - i]

            if i + mirrored_radius < curr_radius:
                res[cursor + i] = mirrored_radius
            elif i + mirrored_radius == curr_radius:
                cursor += i
                curr_radius = mirrored_radius
                break
            else:
                res[cursor + i] = curr_radius - i
        else:
            cursor += curr_radius
            curr_radius = 1

    return res


# Convert the position and radius from an interim result array into indices of the original string
def _convert_to_indices(pos: int, radius: int) -> tuple[int, int]:
    left = pos - radius + 1
    right = pos + radius - 1
    return -(left // -2), right // 2
