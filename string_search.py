# KMP string search
def string_search(text: str, s: str) -> list[int]:
    res = []
    backtrack = -1

    p = _build_prefix_table(s)
 
    for i in range(len(text)):
        while backtrack >= 0 and text[i] != s[backtrack + 1]:
            backtrack = p[backtrack]
        if text[i] == s[backtrack + 1]:
            backtrack += 1
        if backtrack == len(s) - 1:
            res.append(i - backtrack)
            backtrack = p[backtrack]
    return res


def _build_prefix_table(s: str) -> list[int]:
    len_s = len(s)
    p = [-1] * len_s
    backtrack = -1
    for i in range(1, len_s):
        while backtrack >= 0 and s[i] != s[backtrack + 1]:
            backtrack = p[backtrack]
        if s[i] == s[backtrack + 1]:
            backtrack += 1
        p[i] = backtrack
    return p
