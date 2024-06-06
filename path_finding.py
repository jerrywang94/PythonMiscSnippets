import heapq
from typing import Callable


# Path Finding Algorithms


# Dijkstra's Shortest Path
def dijkstra_shortest_path(adj_list: list[list[tuple[int, float]]], start: int, end: int) -> tuple[float, list[int]]:
    prev = [-1] * len(adj_list)
    seen = [(False, 0.0)] * len(adj_list)
    pq = [(0.0, start, -1)]  # Each item is (current_distance, current_node_index, previous_node_index)

    while True:
        curr = heapq.heappop(pq)
        curr_dist = curr[0]
        curr_index = curr[1]
        prev_node = curr[2]

        # Not using a structure like fib heap that allows easy modification of existing item pri; account for duplicates
        if seen[curr_index][0]:
            continue

        seen[curr_index] = (True, curr_dist)
        prev[curr_index] = prev_node

        if curr_index == end:
            break

        for n_node in adj_list[curr_index]:
            if seen[n_node[0]][0]:
                continue

            heapq.heappush(pq, (n_node[1] + curr_dist, n_node[0], curr_index))

    path = []
    pos = end
    while pos != -1:
        path.append(pos)
        pos = prev[pos]

    return seen[end][1], path[::-1]


# Bellman-ford
def bellman_ford(vertices: list[int], edges: list[(int, int, float)], source: int) -> (tuple[None, None] |
                                                                                       tuple[list[float], list[int]]):
    distance = [float("inf")] * len(vertices)
    prev = [-1] * len(vertices)

    distance[source] = 0
    prev[source] = source

    for _ in range(len(vertices) - 1):
        for edge in edges:
            if distance[edge[0]] + edge[2] < distance[edge[1]]:
                distance[edge[1]] = distance[edge[0]] + edge[2]
                prev[edge[1]] = edge[0]

    for edge in edges:
        if distance[edge[0]] + edge[2] < distance[edge[1]]:
            return None, None

    return distance, prev


# A*
def a_star(adj_list: list[list[tuple[int, float]]], start: int, end: int, h: Callable[[int], float]) \
        -> tuple[float, list[int]]:
    prev = [-1] * len(adj_list)
    seen = [(False, 0.0)] * len(adj_list)
    pq = [(0.0, 0.0, start, -1)]  # Each item is (f = d + h, d, current_node_index, previous_node_index)

    while True:
        curr = heapq.heappop(pq)
        curr_dist = curr[1]
        curr_index = curr[2]
        prev_node = curr[3]

        # Not using a structure like fib heap that allows easy modification of existing item pri; account for duplicates
        if seen[curr_index][0]:
            continue

        seen[curr_index] = (True, curr_dist)
        prev[curr_index] = prev_node

        if curr_index == end:
            break

        for n_node in adj_list[curr_index]:
            if seen[n_node[0]][0]:
                continue

            heapq.heappush(pq, (n_node[1] + curr_dist + h(n_node[0]), n_node[1] + curr_dist, n_node[0], curr_index))

    path = []
    pos = end
    while pos != -1:
        path.append(pos)
        pos = prev[pos]

    return seen[end][1], path[::-1]


# Johnson's all shortest-paths
def johnson_all_path(adj_list: list[list[tuple[int, float]]]) -> None | list[list[(float, list[int])]]:
    n = len(adj_list)
    vertices = [i for i in range(n + 1)]  # last element is new node q indexed at n
    edges = [(n, i, 0.0) for i in range(n)]
    for i, l in enumerate(adj_list):
        for item in l:
            edges.append((i, item[0], item[1]))

    bf_dist, _ = bellman_ford(vertices, edges, n)
    if bf_dist is None:
        return None

    reweighed = [[] for _ in range(n)]
    for i, l in enumerate(adj_list):
        for item in l:
            reweighed[i].append((item[0], item[1] + bf_dist[i] - bf_dist[item[0]]))

    results = [[(0.0, []) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p = dijkstra_shortest_path(reweighed, i, j)
            results[i][j] = (p[0] + bf_dist[j] - bf_dist[i], p[1])
    return results


# Floyd-Warshall all shortest-paths
def floyd_warshall(adj_list: list[list[tuple[int, float]]]) -> None | list[list[(float, int)]]:
    n = len(adj_list)
    d = [[float("inf") if i != j else 0 for j in range(n)] for i in range(n)]
    prev = [[i for _ in range(n)] for i in range(n)]
    for i, l in enumerate(adj_list):
        for item in l:
            d[i][item[0]] = item[1]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    prev[i][j] = prev[k][j]

                if i == j and d[i][j] < 0:
                    return None

    return [[(d[i][j], prev[i][j]) for j in range(n)] for i in range(n)]
