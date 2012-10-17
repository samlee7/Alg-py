#!/usr/bin/env python2.7
#Sam Lee
#SID: 860957929
#Project 2 DNA search
#CS 141 Spring 2012
###########################

import sys
from math import sqrt
###########################

database = sys.argv[1]
query = sys.argv[2]
numberOfSeq = sys.argv[3]
alignment = sys.argv[4]

class node:
    def __init__(self, description,similarScore, str1, str2):
        self.description = description
        self.similarScore = similarScore
        self.str1 = str1
        self.str2 = str2
        return None



def score(a,b):
    if (a == 'A' and b == 'A'): return 1.0;
    if (a == 'G' and b == 'G'): return 1.0;
    if (a == 'C' and b == 'C'): return 1.0;
    if (a == 'T' and b == 'T'): return 1.0;
    if (a == 'A' and b == 'G') or ( a == 'G' and b == 'A'): return -0.1;
    if (a == 'A' and b == 'C') or ( a == 'C' and b == 'A'): return -0.1;
    if (a == 'A' and b == 'T') or ( a == 'T' and b == 'A'): return -0.15;
    if (a == 'C' and b == 'G') or ( a == 'G' and b == 'C'): return -0.15;
    if (a == 'T' and b == 'G') or ( a == 'G' and b == 'T'): return -0.1;
    if (a == 'C' and b == 'G') or ( a == 'G' and b == 'C'): return -0.15;
    if (a == 'C' and b == 'T') or ( a == 'T' and b == 'C'): return -0.1;


#open the database file
infile = open(database)
graph = infile.readlines()

#open the query file
oQuery = open(query)
word = oQuery.readlines()

#set num of sequence
amount = int(numberOfSeq)

string1 = word[0][0:len(word[0])-1]
column = len(string1)+1

#create the matrix that fills the table to find the similarScore value of the string
def computesimilarity(row,wordIn):
    a = [[0]*row for x in xrange(column)]

    #Initialization
    for each in range(row): a[0][each] = round(each*(-0.2),2)
    for each in range(column): a[each][0] = round(each*(-0.2),2)

    for i in range(1,column):
        for j in range(1,row):
            left = a[i][j-1] - 0.2
            top = a[i-1][j] - 0.2
            diag = a[i-1][j-1] + score(string1[i-1],wordIn[j-1])
            a[i][j] = round(max(top, left, diag),2)
    
    #The compute similarity part ends here
	#Start constructing alignments
    #vertical value string1 and horizontal value string2
    i = column-1
    j = row-1
    newstr1 = ""
    newstr2 = ""

    while i != 0 and j != 0:
        left = round(a[i][j-1],2)
        top = round(a[i-1][j],2)
        diag = round(a[i-1][j-1],2)
        check = round(max(top,left,diag),2)
        if check == left:
            newstr1 = newstr1+'-'
            newstr2 = newstr2+wordIn[j-1]
            i = i
            j = j-1
        elif check == top:
            newstr1 = newstr1+string1[i-1]
            newstr2 = newstr2+'-'
            i = i-1
            j = j
        else:
            newstr1 = newstr1+string1[i-1]
            newstr2 = newstr2+wordIn[j-1]
            i = i-1
            j = j-1

    newstr1 = newstr1[::-1]
    newstr2 = newstr2[::-1]

    return a[column-1][row-1],newstr1,newstr2

#lists to be used
dnaList = []
values = []
sorted = []
index = 0


while index < len(graph):
    if index == 0 or index%2 == 0:
        description = graph[index][1:len(graph[index])-1]
        index = index+1
    
    phrase = graph[index][0:len(graph[index])-1]
    similarity,str1,str2 = computesimilarity(len(phrase)+1,phrase)
    dnaList.append(node(description,similarity,str1,str2))
    index = index+1


def heap_sort(sortThis):
    first = 0
    last = len(sortThis) - 1
    create_heap(sortThis, first, last)
    for i in range(last, first, -1):
        sortThis[i].similarScore, sortThis[first].similarScore = sortThis[first].similarScore, sortThis[i].similarScore # swap
        establish_heap_property (sortThis, first, i - 1)

# create heap (used by heap_sort)
def create_heap(sortThis, first, last):
    i = last/2
    while i >= first:
        establish_heap_property(sortThis, i, last)
        i -= 1

# establish heap property (used by create_heap)
def establish_heap_property(sortThis, first, last):
    while 2 * first + 1 <= last:
        k = 2 * first + 1
        if k < last and sortThis[k].similarScore < sortThis[k + 1].similarScore:
            k += 1
        if sortThis[first].similarScore >= sortThis[k].similarScore:
            break
        sortThis[first].similarScore, sortThis[k].similarScore = sortThis[k].similarScore, sortThis[first].similarScore # swap
        first = k

#heap sort the dna list then reverse the list
heap_sort(dnaList)
dnaList.reverse()

#number is to keep track of current no.  currentLoc keep tracks of location in the array.
number = 1
currentLoc= 0

#Print the solution alignment 0
print "\n"
for i in dnaList:
    print number,"*",i.similarScore,"*",i.description
	#print the solution alignment 1
    if alignment == '1':
        print "\n"
        length = len(dnaList[currentLoc].str1)-1
        #loc value is used to keep track of only printing 80 characters per line  
        loc = 0
           
        while loc < length:
            if loc < length:
                print dnaList[currentLoc].str1[loc:loc+79]
                print dnaList[currentLoc].str2[loc:loc+79]
                loc = loc+79
                print "\n",
        currentLoc+=1
        number +=1
        amount +=1

        print "====================================================================================================","\n"

