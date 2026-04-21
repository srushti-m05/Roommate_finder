class Node:
    def __init__(self, user):
        self.user = user
        self.next = None

class UserList:
    def __init__(self):
        self.head = None

    def add(self, user):
        if not self.head:
            self.head = Node(user)
            return
        t = self.head
        while t.next:
            t = t.next
        t.next = Node(user)

    def to_list(self):
        users = []
        t = self.head
        while t:
            users.append(t.user)
            t = t.next
        return users
