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
from itertools import chain, combinations

class TreeNode:
    def __init__(self, s, parent):
        self.s = s                          # a set
        self.support = 0                    # an int
        self.children = []                  # list of children
        self.parent = parent                # Tree node referencing parent

    def __eq__(self, other):
        return (type(other) == TreeNode
                and self.s == other.s
                and self.support == other.support)

    def __repr__(self):
        return "TreeNode({!r}, {!r}, {!r})".format(self.s, self.support, self.children)

def powset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_power_set(s):
  power_set=[[]]
  for elem in s:
    # iterate over the sub sets so far
    for sub_set in power_set:
      # add a new subset consisting of the subset at hand added elem
      power_set = power_set + [list(sub_set)+[elem]]
  return power_set[1:-1]

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

def computeSupport(itemSets, database):
    for transaction in database:
        for itemSet in itemSets:
            if itemSet.s.issubset(transaction):
                itemSet.support += 1

def extendPrefixTree(level):
    nextLevel = []
    for leaf in level:
        flag = False
        # getSiblings -> list of all it's siblings ie parents chilren
        siblings = leaf.parent.children
        # getlocation of leaf in sibling list
        leafIdx = siblings.index(leaf)
        # for location +1 to end of sibling list
        for i in range(leafIdx+1, len(siblings)):
            # union leaf with sibling
            sibUnion = leaf.s.union(siblings[i].s)
            # powersets of union
            powersets = powset(sibUnion)
            # for each set of powerset
            for powerset in powersets:
                if len(powerset) == len(sibUnion) - 1:
                    if powerset not in level:
                        flag = True
            if flag:
                # add union as child of leaf
                leaf.children.append(TreeNode(set(sibUnion), leaf))
        tempLeaf = leaf
        while len(leaf.children) == 0:
            # remove leave
            if leaf.parent == None:
                return []
            leaf.parent.children.remove(leaf)
            leaf = leaf.parent
        for child in tempLeaf.children:
            nextLevel.append(child)
    return nextLevel

def apriori(database, itemSet, minsup):
    freqItemSet = []
    tree = TreeNode(set(), None)
    for item in itemSet:
        tree.children.append(TreeNode(set([item]), tree))
    level = tree.children
    while(len(level) > 0):
        computeSupport(level, database)
        for leaf in level[:]:
            #print(leaf)
            if leaf.support >= minsup:
                freqItemSet.append((leaf.s, leaf.support))
            else:
                level.remove(leaf)
        level = extendPrefixTree(level)
    return freqItemSet

def sup(inSet, itemSet):
    for item in itemSet:
        temp = list(item[0])
        if temp == inSet:
            return item[1]
    return sys.maxsize

def print_rule(predictor, result, confidence):
    res = list(result)
    for pred in predictor:
        res.remove(pred)
    predictor = "{" + ', '.join(predictor) + "}"
    result = "{" + ', '.join(res) + "}"
    print('{:15s} --> {:10s} Confidence: {:.02f}'.format(predictor, result, confidence))

def remove_subsets(item, inList):
    subsets = get_power_set(item)
    for subset in subsets:
        if subset in inList:
            inList.remove(subset)
    return inList

def generate_rules(itemSet, min_conf):
    for z in itemSet:
        if len(z[0]) >= 2:
            a = get_power_set(z[0])
            while len(a) > 0:
                x = []
                for item in a:
                    if len(item) > len(x):
                        x = item
                a.remove(x)
                support = sup(x, itemSet)
                conf = z[1]/support
                if conf > min_conf:
                    #print(x, "->", z[0])
                    print_rule(x, z[0], conf)
                    pass
                else:
                    a = remove_subsets(x, a)
                

def print_results_min_sup(itemSet, min_sup):
    print ("The most frequent item sets with a minimum support of %.02f are as follows:\n" % min_sup)
    print ('%-62s%-12s' % ("set:", "support:\n"))
    for i in itemSet:
        print ('{%-62s%-12i' % (', '.join(i[0]) + '}', i[1]))

def main():
   args = sys.argv[1:]

   if not args or len(args) != 3:
      print('usage: ./apriory.py CSV minsup minconf')
      sys.exit(1)

   csv_path = args[0]
   csv = open(csv_path, 'r')

   transactionDatabase = buildTransactionDatabaseFromCSV(csv)
   totalItemSet = sorted(buildTotalItemSet(transactionDatabase))

   min_sup = float(args[1])*len(transactionDatabase)
   min_conf = float(args[2])

   itemSet = apriori(transactionDatabase, totalItemSet, min_sup)
   #print_results_min_sup(itemSet, min_sup)

   rules = generate_rules(itemSet, min_conf)

if __name__ == '__main__':
   main()