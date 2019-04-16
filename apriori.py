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

def main():
   args = sys.argv[1:]

   if not args or len(args) != 3:
      print('usage: ./apriory.py CSV minsup minconf')
      sys.exit(1)

   csvPath = args[0]

if __name__ == '__main__':
   main()