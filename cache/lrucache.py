import requests


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None
        self.size = val.__sizeof__()


class ImageLRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.available = capacity
        self.head = None
        self.tail = None
        self.map = {}

    def insert_head(self, node):
        node.next = self.head
        node.prev = None
        self.head = node
        if self.head.next:
            self.head.next.prev = self.head
        if self.tail is None:
            self.tail = self.head
        self.map[node.key] = self.head
        self.available -= node.size

    def insert(self, url):
        if url in self.map:
            node = self.remove(url)
            self.insert_head(node)
            print(url.strip("\n") + " CACHED " + str(node.size) +
                  " AVAILABLE " + str(self.available))
            return
        content = self.download(url)
        node = Node(url, content)
        if node.size > self.capacity:
            raise ValueError("image too large")
        if self.available < node.size:
            while self.available < node.size:
                self.remove_tail()

        self.insert_head(node)
        print(url.strip("\n") + " DOWNLOADED " + str(self.map[url].size) + " AVAILABLE " + str(self.available))

    def remove_tail(self):
        if self.tail is None:
            raise ValueError("no tail found")
        node = self.tail
        self.map.pop(self.tail.key)
        self.available += node.size
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None

        return node

    def remove(self, url):
        if url not in self.map:
            raise KeyError("trying to remove something that is not present")
        node = self.map[url]
        if node == self.tail:
            return self.remove_tail()
        self.available += node.size
        self.map.pop(url)
        if node == self.head:
            self.head = self.head.next
            self.head.prev = None
            return node
        node.prev.next = node.next
        node.next.prev = node.prev

        return node

    @staticmethod
    def download(url):
        r = requests.get(url)
        r.raise_for_status()
        return r.content
