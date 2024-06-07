import disjoint_set
import heapq


# Minimum spanning tree


# Kruskal
def kruskal_mst(adj_list: list[list[tuple[int, float]]]) -> list[(int, int)]:
    n = len(adj_list)
    djs = disjoint_set.DisjointSet()
    mst = []
    for i in range(n):
        djs.make_set(i)
    edges = []
    for i, l in enumerate(adj_list):
        for item in l:
            edges.append((item[1], i, item[0]))
    edges.sort()
    for edge in edges:
        if djs.find(edge[1]) != djs.find(edge[2]):
            mst.append((edge[1], edge[2]))
            djs.union(edge[1], edge[2])

    return mst


# Prim's
def prim_mst(adj_list: list[list[tuple[int, float]]]) -> list[(int, int)]:
    n = len(adj_list)
    key_parent = [(0.0, 0, 0)]  # key, parent index, current index
    cost = [float("inf")] * n
    mst = []
    seen = [False] * n
    seen[0] = True
    cost[0] = 0.0

    while len(mst) < n-1:
        print("--")
        print(key_parent)
        curr = heapq.heappop(key_parent)
        if curr[1] != curr[2]:
            if not seen[curr[2]]:
                mst.append((curr[1], curr[2]))
            else:
                continue
        seen[curr[2]] = True

        for item in adj_list[curr[2]]:
            if not seen[item[0]] and item[1] < cost[item[0]]:
                heapq.heappush(key_parent, (item[1], curr[2], item[0]))

    return mst
