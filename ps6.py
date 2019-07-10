#! /usr/bin/env python2
# file = "contigs.fa"
#
#setting up argparse -
import argparse

parser=argparse.ArgumentParser("A program to have fun with Kmers")
parser.add_argument("-f", "--file", help="the name of the file to pass through", required=True)
parser.add_argument("-g", "--new_file", help="the name of the file where the contigs go", required=True)
args = parser.parse_args()

#Reading in the file -> then puts only the lines that have the sequence ID into a new file
with open(args.file, "r") as fh:
    for line in fh:
        line = line.strip("/n")
        if line.startswith('>'):
            with open(args.new_file, "a") as filed:
                filed.write(line)
