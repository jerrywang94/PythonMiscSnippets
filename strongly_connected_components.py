# Strongly Connected Components


# Kosaraju's algorithm
def kosaraju_scc(adj_list: list[list[int]]) -> list[int]:
    n = len(adj_list)
    visited = [False] * n
    inorder = []
    assignments = [-1] * n
    transpose = [[] for _ in range(n)]

    def traverse(u: int):
        if visited[u]:
            return
        visited[u] = True
        for n in adj_list[u]:
            transpose[n].append(u)
            traverse(n)
        inorder.append(u)

    def assign_root(u: int, root: int):
        if assignments[u] != -1:
            return
        assignments[u] = root
        for n in transpose[u]:
            assign_root(n, root)

    for i in range(n):
        traverse(i)

    for node in inorder[::-1]:
        assign_root(node, node)

    return assignments


# Tarjan's algorithm
def tarjan_scc(adj_list: list[list[int]]) -> list[int]:
    n = len(adj_list)
    index = 0
    state = [(-1, -1, False) for _ in range(n)]  # index, lowest ancestor, on stack
    st = []
    scc = []

    def dfs(v: int):
        nonlocal index
        state[v] = (index, index, True)
        index += 1
        st.append(v)

        for s in adj_list[v]:
            if state[s][0] == -1:
                dfs(s)
                state[v] = (state[v][0], min(state[v][1], state[s][1]), state[v][2])
            elif state[s][2]:
                state[v] = (state[v][0], min(state[v][1], state[s][1]), state[v][2])

        if state[v][1] == state[v][0]:
            new_scc = []
            curr = -1
            while curr != v:
                curr = st.pop()
                state[curr] = (state[curr][0], state[curr][1], False)
                new_scc.append(curr)
            scc.append(new_scc)

    for i in range(n):
        if state[i][0] == -1:
            dfs(i)
    return scc
