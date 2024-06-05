from functools import cmp_to_key

# Convex Hull Algorithms


# Graham scan
def graham_scan(points: list[tuple[float, float]]) -> list[tuple]:
    if len(points) < 4:
        return points

    p = [(x[1], x[0], i) for i, x in enumerate(points)]
    starting_point_index = min(p)[2]
    starting_point = points[starting_point_index]

    hull = [points[starting_point_index]]
    candidates = points
    candidates.pop(starting_point_index)

    candidates.sort(key=cmp_to_key(lambda x, y: _polar_sort(starting_point, x, y)))
    hull.append(candidates[0])
    hull.append(candidates[1])

    for c in candidates[2:]:
        while _polar_sort(hull[-2], hull[-1], c) == 1:
            hull.pop()
        hull.append(c)

    return hull


def jarvis_march(points: list[tuple[float, float]]) -> list[tuple]:
    if len(points) < 4:
        return points

    starting_point = min(points)

    bottom = [starting_point]
    point_added = True
    while point_added:
        candidate = None
        point_added = False
        for p in points:
            if p == bottom[-1] or p[0] < bottom[-1][0]:
                continue

            if not candidate or _polar_sort(bottom[-1], candidate, p) == 1:
                candidate = p
                point_added = True
        if candidate:
            bottom.append(candidate)

    top = [bottom[-1]]
    point_added = True
    while point_added:
        candidate = None
        point_added = False
        for p in points:
            if p == top[-1] or p[0] > top[-1][0]:
                continue

            if not candidate or _polar_sort(top[-1], candidate, p) == 1:
                candidate = p
                point_added = True
        if candidate:
            top.append(candidate)

    return bottom[:-1] + top[:-1]


def _polar_sort(p_origin, x, y):
    v1 = x[0] - p_origin[0], x[1] - p_origin[1]
    v2 = y[0] - p_origin[0], y[1] - p_origin[1]

    x_product = v1[0] * v2[1] - v1[1] * v2[0]
    if x_product == 0:
        return -1 if v1[0] * v1[0] + v1[1] * v1[1] < v2[0] * v2[0] + v2[1] * v2[1] else 1
    else:
        return -1 if x_product > 0 else 1
