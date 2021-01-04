# Python3 program to print DFS traversal
# from a given given graph
from collections import defaultdict

import numpy as np


# This class represents a directed graph using
# adjacency list representation

#generating groups of disconected graphs from intersection matrix
class Graph:

    # Constructor
    def __init__(self):

        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # A function used by DFS
    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        # and print it
        visited.add(v)

        # Recur for all the vertices
        # adjacent to this vertex
        for neighbour in self.graph[v]:
            if neighbour not in visited:
                self.DFSUtil(neighbour, visited)

    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v):

        # Create a set to store visited vertices
        visited = set()

        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, visited)
        return frozenset(visited)


def generate_groups(intersection_mtx):
    g = Graph()
    a = np.array(intersection_mtx)
    np.fill_diagonal(a, 0)
    for row_idx, row in enumerate(a):
        for col_idx, col in enumerate(row):
            if a[row_idx][col_idx] != 0:
                g.addEdge(row_idx, col_idx)
    k = set()
    for idx, _ in enumerate(a):
        k.add(g.DFS(idx))
    return [list(x) for x in k]


a = [[1.0, 0.09090909090909091, 0.09090909090909091, 0, 0, 0],
     [0.09090909090909091, 1.0, 0, 0, 0, 0],
     [0.09090909090909091, 0, 1.0, 0, 0, 0],
     [0, 0, 0, 1.0, 0.09090909090909091, 0.058823529411764705],
     [0, 0, 0, 0.09090909090909091, 1.0, 0.07462686567164178],
     [0, 0, 0, 0.058823529411764705, 0.07462686567164178, 1.0]]
print(generate_groups(a))
