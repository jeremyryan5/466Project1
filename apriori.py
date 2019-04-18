#!/usr/bin/python

"""
Jeremy Whorton
Garrett Wayne
CSC 466
4/9/19
"""

import sys
import re
import os
import itertools

class TreeNode:
    def __init__(self, s, support):
        self.s = s                          # a set
        self.support = support              # an int

    def __eq__(self, other):
        return (type(other) == TreeNode
                and self.s == other.s
                and self.support == other.support)

    def __repr__(self):
        return "TreeNode({!r}, {!r})".format(self.s, self.support)

# Builds an array of sets where each entry in the array is a line in the csv,
# a set of items it contains
def buildTransactionDatabaseFromCSV(csv): 
    t = [line.strip() for line in csv]
    t_sets = []
    for x in t:
        t_sets.append(set(x.split(",")))
    return t_sets

# Builds a set of all the items seen in the database
def buildTotalItemSet(transactionDatabase):
    totalItemSet = set()
    for x in transactionDatabase:
        for i in x:
            if i not in totalItemSet:
                totalItemSet.add(i)
    return totalItemSet

# Computes the support from the overall database for all nodes in a given k level
# in the prefix tree
def computeSupport(k_tree_level, k, dataBase):
    for itemset in dataBase:
        k_subsets = list(map(set, itertools.combinations(itemset, k)))
        for k_subset in k_subsets:
            for prefix_set_node in k_tree_level:
                if k_subset.issubset(prefix_set_node.s):
                    prefix_set_node.support += 1

# Extends the k-ith prefix tree level
def extendPrefixTree(k_tree_level):
    k_1 = []
    for i in range(len(k_tree_level)):
        for j in range(i + 1, len(k_tree_level)):
            siblingUnion = k_tree_level[i].s.union(k_tree_level[j].s)
            k_1.append(TreeNode(siblingUnion, 0))
    return k_1

# Prints the results of the array of tuples containing the frequent sets and their support
def print_results_min_sup(f, rel_min_sup):
    print "The most frequent item sets with relative minimum support of",rel_min_sup,"are as follows:\n"
    print '%-62s%-12s' % ("set:", "support:\n")
    for i in f:
        print '{%-62s%-12i' % (i[0] + '}', i[1])

# The apriory algorithm for minimum support
def apriory(dataBase, totalItemSet, rel_min_sup):
    size = len(dataBase)
    min_sup = rel_min_sup * size
    frequentItemSet = set()
    prefixTree = [[], []]
    for i in totalItemSet:
        prefixTree[1].append(TreeNode(set([i]), 0))
    k = 1
    while len(prefixTree[k]) > 0:
        computeSupport(prefixTree[k], k, dataBase)
        for prefix_set_node in prefixTree[k][:]:
            if prefix_set_node.support >= min_sup:
                frequentItemSet.add((', '.join(prefix_set_node.s), prefix_set_node.support))
            else:
                prefixTree[k].remove(prefix_set_node)
        prefixTree.append([])
        prefixTree[k + 1] = extendPrefixTree(prefixTree[k])
        k += 1
    print_results_min_sup(frequentItemSet, rel_min_sup)

def main():
   args = sys.argv[1:]

   if not args or len(args) != 3:
      print('usage: ./apriory.py CSV minsup minconf')
      sys.exit(1)

   csv_path = args[0]
   rel_min_sup = float(args[1])
   csv = open(csv_path, 'r')

   transactionDatabase = buildTransactionDatabaseFromCSV(csv)
   totalItemSet = buildTotalItemSet(transactionDatabase)
   apriory(transactionDatabase, totalItemSet, rel_min_sup)

if __name__ == '__main__':
   main()