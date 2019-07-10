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
#isolating only the k-mer length and k-mer coverage
k_mer_leng = []
k_mer_cover = []
import re
with open(args.new_file, "r") as myfile:
    for line in myfile:
        #line = line.strip('\n')
        #print(line)
        pattern = '(>)([A-Z]+)_([0-9]+)_([a-z]+)_([0-9]+)_([a-z]+)_([0-9, .]+)' #want group 5 and 7
        result = re.search(pattern, line) #searches for my pattern in the line
        if result:
            k_mer_leng.append(float(result.group(5))) #isolates only the k_mer_leng and makes it a float - otherwise it loads in as a string
            k_mer_cover.append(float(result.group(7))) #isolates only the k_mer_cover

print(k_mer_leng)
