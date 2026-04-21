class Graph:
    def __init__(self):
        self.graph = {}

    def add_user(self, uid):
        if uid not in self.graph:
            self.graph[uid] = []

    def add_edge(self, u1, u2, score):
        self.graph[u1].append((u2, score))
        self.graph[u2].append((u1, score))

    def get_connections(self, uid):
        return self.graph.get(uid, [])
