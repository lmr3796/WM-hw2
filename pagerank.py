#! /usr/bin/env python

import sys
import copy
import numpy

config = {}
config['EPS'] = 1e-6
config['Damping'] = 0.85

log_file = sys.stderr

class AdjacentGraph:
    def __init__(self, maxnode, outlink):
        self.outlink = copy.deepcopy(outlink)
        self.maxnode = maxnode
        self.no_outlink = tuple([i for i in range(1, self.maxnode + 1) if i not in self.outlink])

    @classmethod
    def fromfile(cls, f):
        print >> sys.stderr, "Building adjacent graph...",
        content = f.readlines()
        outlink = {}
        maxnode = int(content[0].split()[1])
        for line in content[1:]:
            if len(line.strip().split(':')) < 2:    # Avoid trailing empty line
                continue
            (in_node, out_nodes) = line.strip().split(':')
            # First number after : denotes the amount of outoutlinks
            outlink[int(in_node)] = set([int(x) for x in out_nodes.split()[1:]])
        print >> sys.stderr, "done."
        return AdjacentGraph(maxnode, outlink)

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
        d = reduce(lambda x, y: x + y**2, a.prestige - b.prestige, 0) ** 0.5
        return d

    # Transition
    def __rmul__(self, A):
        assert A.maxnode == self.maxnode
        # Initiate with the 1-d for random surfing
        default_prestige = 1 - config['Damping']

        # Share prestige of those who have no outlinks to all node
        default_prestige += config['Damping'] * sum([self.prestige[i] for i in A.no_outlink]) / self.maxnode
        new_prestige = numpy.array([default_prestige] * (self.maxnode + 1))

        # Share prestige to outlinked ones
        for i in A.outlink:
            shared_prestige = config['Damping'] * self.prestige[i] / len(A.outlink[i])
            for j in A.outlink[i]:
                new_prestige[j] += shared_prestige


        # Return a new PageRank instance
        result = PageRank(self.maxnode)
        result.prestige = new_prestige
        return result 


# Compute pagerank from adjacency
def compute_pagerank(A):
    print >> sys.stderr, "Computing PageRank...."
    # Transit until converge
    i = 0
    curr_rank = PageRank(A.maxnode)
    next_rank = A * curr_rank
    distance = PageRank.distance(curr_rank, next_rank)
    while distance > config['EPS']:
        i += 1
        if i % 10 == 0:
            print >> sys.stderr, "Iteration %d: distance = %f" % (i, distance)
        curr_rank = next_rank
        next_rank = A * curr_rank
        distance = PageRank.distance(curr_rank, next_rank)
    curr_rank = next_rank
    return curr_rank


def main():
    if len(sys.argv) > 1 :
        with open(sys.argv[-1]) as f:
            print >> sys.stderr, 'Loading graph file %s...' % sys.argv[-1]
            A = AdjacentGraph.fromfile(f)
    else:
        print >> sys.stderr, 'Loading graph file from stdin...'
        A = AdjacentGraph.fromfile(sys.stdin)

    pagerank = compute_pagerank(A)
    print pagerank

    return 0

if __name__ == '__main__':
    exit(main())
