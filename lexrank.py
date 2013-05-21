#! /usr/bin/env python

import sys
import math
import pagerank

from collections import defaultdict

T=0.1
DEFAULT_IDF=math.log(40252.0)


def similarity(a, b):
    inner_product = reduce(lambda v, w: v + a[w] * b[w], a, 0.0)
    len_a = reduce(lambda v, x: v + x**2, a.values(), 0) ** 0.5
    len_b = reduce(lambda v, x: v + x**2, b.values(), 0) ** 0.5
    sim = inner_product / len_a / len_b
    return sim


def parse_sentence(sentence, idf):
    v = defaultdict(float)
    for w in sentence.strip().split():
        v[w] += 1.0 * idf[w]
    return v


def main():
    with open(sys.argv[1]) as f:
        idf = defaultdict(lambda :DEFAULT_IDF) 
        for line in f.readlines():
            (w, value) = line.strip().split()
            idf[w] = float(value)
    if len(sys.argv) > 2 :
        with open(sys.argv[-1]) as f:
            sentence_list = f.readlines()
    else:
        sentence_list = sys.stdin.readlines()

    sentence_vector_list = [parse_sentence(s, idf) for s in sentence_list]
    outlink = defaultdict(set)
    for i in range(len(sentence_vector_list)):
        for j in range(len(sentence_vector_list)):
            if i == j:
                continue
            if similarity(sentence_vector_list[i], sentence_vector_list[j]) > T:
                outlink[i+1].add(j+1)
                outlink[j+1].add(i+1)
    for k, v in outlink.iteritems():
        print k, v
    return 0

if __name__ == '__main__':
    exit(main())
