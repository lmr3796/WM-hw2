#! /usr/bin/env python

import sys, copy

EPS=1e-6
d=0.85

class AdjacentGraph:
    def __init__(self, f):
        content = f.readlines()
        self.link = {}
        self.maxnode = int(content[0].split()[1])
        for line in content[1:]:
            if len(line.strip().split(':')) < 2:    # Avoid trailing empty line
                continue
            (in_node, out_nodes) = line.strip().split(':')
            # First number after : denotes the amount of outlinks
            self.link[int(in_node)] = tuple([int(x) for x in out_nodes.split()[1:]])
        return

    def no_out_link(self, i):
        return i in self.link

class PageRank:
    def __init__(self, maxnode):
        self.maxnode = maxnode
        # 1-based index
        self.prestige = [1.0 / maxnode] * (maxnode + 1)
        self.prestige[0] = 0.0
        self.prestige = numpy.array(self.prestige)
        return

    def __str__(self):
        return ''.join(['%d:%f\n' % (i, rank) for i, rank in enumerate(self.prestige) if i != 0])


    @staticmethod
    # Euclidean distance between their prestige
    def distance(a, b):
        return reduce(lambda x, y: x + y**2, a.prestige - b.prestige) ** 0.5


    # Transition
    def __rmul__(self, A):
        assert A.maxnode == self.maxnode
        # Initiate with the 1-d for random surfing
        new_prestige = numpy([1-d] * (self.maxnode + 1))
        for i in range(1, len(new_prestige)):
            if A.no_out_link(i):    # Share prestige to every one
                new_prestige += d * self.prestige[i] / self.maxnode
            else:
                for j in A.link[i]: # Share prestige to linked ones
                    new_prestige[j] += d * self.prestige[i] / len(A.link[i])

        # Return a new PageRank instance
        result = PageRank(self.maxnode)
        result.prestige = new_prestige
        return result 

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            A = AdjacentGraph(f)
    else:
        A = AdjacentGraph(sys.stdin)

    # Transit until converge
    curr_rank = PageRank(A.maxnode)
    next_rank = curr_rank(A * curr_rank)
    while PageRank.distance(curr_rank, next_rank) > EPS:
        curr_rank = next_rank
        next_rank = curr_rank(A * curr_rank)
    curr_rank = next_rank

    return 0

if __name__ == '__main__':
    exit(main())
