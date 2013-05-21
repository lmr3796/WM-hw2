#! /usr/bin/env python

import sys

EPS=1e-6
d=0.85

conf = {}

class AdjacentGraph:
    def __init__(self, f):
        content = f.readlines()
        self.data = {}
        self.maxnode = int(content[0].split()[1])
        for line in content[1:]:
            (in_node, out_nodes) = line.split(':')
            # First number after : denotes the amount of outlinks
            self.data[int(in_node)] = tuple([int(x) for x in out_nodes.split()[1:]])
        return

    def adjacent(self, i, j):
        return (i in self.data) and (j in self.data[i])

class PageRank:
    def __init__(self):
        return

def main():
    with open(sys.argv[1]) as f:
        adj_map = AdjacentGraph(f)

    return 0

if __name__ == '__main__':
    exit(main())
