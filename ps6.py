#! /usr/bin/env python3
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
kmer_length = 49
#K-mer length: For the value of k chosen in the assembly, a measure of how many k-mers overlap (by 1 bp each overlap) to give this length
#want to convert k_mer_leng to actual physical length of the contig
#to convert do kmer_length-1 + k_mer_leng[index]
index1=0
add_on = kmer_length - 1
for i in k_mer_leng:
    k_mer_leng[index1]=i+add_on
    index1+=1
#now k_mer_leng list has the actual lengths of my contigs!

#contig number is just the number of reads in my fasta file
contig_count = len(k_mer_leng)
#max contig lengths
max_contig_length = max(k_mer_leng)
#Mean contig length
mean_contig_length = sum(k_mer_leng)/contig_count
#total length of genome across all contigs
total_genome_length = sum(k_mer_leng)
#expected coverage
coverage_array = []
index2=0
for i in k_mer_leng:
    cov = (k_mer_cover[index2] * i) / (i - kmer_length + 1)
    coverage_array.append(cov)
    index2+=1
mean_depth_coverage = sum(coverage_array)/contig_count
#calculating the N50
#need to sort my k_ner_leng list so the biggest value is first
k_mer_leng.sort(reverse= True)
#Need to know where 50% of the assembly is
Half_genome_leng = total_genome_length / 2
#the N50 is at the spot where the mysum value goes from being less than half the genome length to being greater than it
mysum=0
for i in k_mer_leng:
    mysum+=i
    if mysum < Half_genome_leng:
        pass
    #breaks the loop as soon as the N50 is found
    elif mysum > Half_genome_leng:
        N50 = i
        break
#Putting my contigs in dictionaries based on bins
contig_bins = {}
for i in k_mer_leng:
    #rounds the number down
    bin_id = round(i, -2)
    if bin_id in contig_bins:
        contig_bins[bin_id]+=1
    elif bin_id not in contig_bins:
        contig_bins[bin_id]=1
#sorting my dictionary and make it so I can print it out
import operator
#sorted my kmers - it became a tuple after sorting it
sort_contig_bins = sorted(contig_bins.items(), key=operator.itemgetter(0), reverse=False)

print("my coverage is", mean_depth_coverage)
print("the max contig length is", max_contig_length)
print("there are", contig_count, "contigs")
print("the mean contig length is", mean_contig_length)
print("the total sum of the genome is", total_genome_length)
print('the N50 is', N50)
print("# Contig Length", "\t", "Number of Contigs in this Category")
index=0
for i in sort_contig_bins:
    print(sort_contig_bins[index][0], "\t", sort_contig_bins[index][1])
    index+=1
