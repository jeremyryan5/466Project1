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

def buildTransactionDatabaseFromCSV(csv): 
    t = [line.strip() for line in csv]
    t_sets = []
    for x in t:
        t_sets.append(set(x.split(",")))
    return t_sets

def buildTotalItemSet(transactionDatabase):
    totalItemSet = set()
    for x in transactionDatabase:
        for i in x:
            if i not in totalItemSet:
                totalItemSet.add(i)
    return totalItemSet

def computeSupport(k_tree_level, dataBase):
    for x in dataBase:
        for i in x:
            if i in k_tree_level

def apriory(dataBase, totalItemSet, min_sup):
    frequentItemSet = {}
    prefixTree = [[], []]
    for i in totalItemSet:
        prefixTree[1].append(TreeNode(set([i]), 0))
    k = 1
    while len(prefixTree[k]) > 0:
        computeSupport(prefixTree[k], dataBase)

def main():
   args = sys.argv[1:]

   if not args or len(args) != 3:
      print('usage: ./apriory.py CSV minsup minconf')
      sys.exit(1)

   csv_path = args[0]
   csv = open(csv_path, 'r')

   transactionDatabase = buildTransactionDatabaseFromCSV(csv)
   totalItemSet = buildTotalItemSet(transactionDatabase)
   apriory(transactionDatabase, totalItemSet, 0.25)
#    print(len(transactionDatabase))
#    apriory(csv, args[1])

if __name__ == '__main__':
   main()