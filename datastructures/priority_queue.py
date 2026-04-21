import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, score, user):
        heapq.heappush(self.heap, (-score, user))

    def pop(self):
        return heapq.heappop(self.heap)

    def empty(self):
        return len(self.heap) == 0
