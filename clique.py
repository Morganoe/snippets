#! /usr/bin/env python3

# Author: Morgan Eckenroth
#
# Naive implementation of a Clique finder for arbitrary graphs.
# 
# Algorithm:
#   Find all 3-cycles in graph
#   Use single-edge building to construct all possible cliques

# Generic graph using adjacency list implementation
class Graph(object):
    def __init__(self):
        self.adj = dict()
        self.nodes = list()

    def __str__(self):
        s = "{\n"
        for i in self.adj:
            s += str(i) + " : "
            s += str(self.adj[i])
            s += "\n"
        s += "}"
        return str(s)

    def __repr__(self):
        s = "{\n"
        for i in self.adj:
            s += str(self.adj[i])
            s += "\n"
        s += "}"
        return str(s)

    def add_edge(self, a, b):
        if a not in self.adj:
            self.adj[a] = [b]
        else:
            self.adj[a].append(b)
        
        if b not in self.adj:
            self.adj[b] = [a]
        else:
            self.adj[b].append(a)

        if a not in self.nodes:
            self.nodes.append(a)

        if b not in self.nodes:
            self.nodes.append(b)

# Find all 3-cycles in graph
def find_3cycles(G):
    visited = set()
    for a in G.adj:
        for b in G.adj[a]:
            if b in visited:
                continue
            for c in G.adj[b]:
                if c in visited:
                    continue
                if a in G.adj[c]:
                    yield(set([a, b, c]))
        visited.add(a)
    
def remove_duplicates(a):
    seen = list()
    for x in a:
        if x not in seen:
            yield list(x)
            seen.append(x)

import copy
def is_clique(G, clique):
    for i in clique:
        edges = copy.deepcopy(clique)
        edges.remove(i)
        for j in edges:
            if j not in G.adj[i]:
                return False
    return True


def find_cliques(G):
    C = list(remove_duplicates(list(find_3cycles(G))))
    ret = list()
    q = list()
    visited = list()
    for cycle in C:
        ret.append(cycle)
        for node in cycle:
            q.extend(G.adj[node])
            while len(q) > 0:
                curr = q.pop(-1)
                if curr not in visited:
                    if is_clique(G, cycle + [curr]):
                        ret.append(cycle + [curr])
                        q.extend(G.adj[curr])
                    visited += [curr]
            visited = list()
            q = list()
    
    # Post processing
    temp = [set(x) for x in ret]
    ret = list(remove_duplicates(temp))
    return ret


def print_cliques(c):
    s = "[\n"
    for i in c:
        s += "  "
        s += str(i)
        s += "\n"
    s += "]"
    print(s)



g = Graph()
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,4)
g.add_edge(2,3)
g.add_edge(2,4)
g.add_edge(3,4)
g.add_edge(2,5)
g.add_edge(4,5)
g.add_edge(5,6)
g.add_edge(5,7)
g.add_edge(6,7)
cliques = find_cliques(g)
print_cliques(cliques)
