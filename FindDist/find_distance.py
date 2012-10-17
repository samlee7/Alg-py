#!/usr/bin/env python2.7
#
# CS 141 Sprint 2012
# Lab 7
##############################

class node:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.dist = 0
        return None

import sys
from heapq import *

graph = sys.stdin.readlines()
nrow = len(graph)
ncol = len(graph[0])-1

dist=[[-1]*ncol for i in range(nrow)]
seen=[[0]*ncol for i in range(nrow)]

def getcell(incr):
    if incr>0:
        for i in range(nrow):
            for j in range(ncol):
                if graph[i][j]!='#':
                    return (i,j)
    else:
        for i in range(nrow-1, 0, -1):
            for j in range(ncol-1, 0, -1):
                if (graph[i][j]!='#'):
                    return (i,j)
        
    return (-1,-1)

def find_distance(start, end):
    dist[start[0]][start[1]]=int(graph[start[0]][start[1]])
    Q=[]
    for i in range(nrow):
        for j in range(ncol):
            if graph[i][j]!='#':
                #print graph[i][j], i, j
                heappush(Q,(graph[i][j],node(i,j)))
    #heapify(Q)
    store=[]
    while Q:
        nodepop=heappop(Q)
        flag=0
        if(dist[nodepop[1].x][nodepop[1].y]==-1):
            heappush(store,(nodepop[0],node(nodepop[1].x,nodepop[1].y)))
            flag=1
        a=nodepop[1].x
        b=nodepop[1].y

        if (a-1>=0 and graph[a-1][b]!='#' and flag==0 and seen[a-1][b]==0):
            if(dist[a-1][b]==-1):
                dist[a-1][b]=int(dist[a][b])+int(graph[a-1][b])
            else:
                alt=int(dist[a][b])+int(graph[a-1][b])
                if(alt<int(dist[a-1][b])):
                    dist[a-1][b]=alt
        if(a+1<nrow):
            if (graph[a+1][b]!='#'  and flag==0 and seen[a+1][b]==0):
                if(dist[a+1][b]==-1):
                    dist[a+1][b]=int(dist[a][b])+int(graph[a+1][b])
                else:
                    alt=int(dist[a][b])+int(graph[a+1][b])
                    if(alt<int(dist[a+1][b])):
                        dist[a+1][b]=alt
        if(b-1>=0 and graph[a][b-1]!='#' and flag==0 and seen[a][b-1]==0):
            if(dist[a][b-1]==-1):
                dist[a][b-1]=int(dist[a][b])+int(graph[a][b-1])
            else:
                alt=int(dist[a][b])+int(graph[a][b-1])
                if(alt<int(dist[a][b-1])):
                    dist[a][b-1]=alt
        if(b+1<ncol):
            if (graph[a][b+1]!='#' and flag==0 and seen[a][b+1]==0):
                if(dist[a][b+1]==-1):
                    dist[a][b+1]=int(dist[a][b])+int(graph[a][b+1])
                else:
                    alt=int(dist[a][b])+int(graph[a][b+1])
                    if(alt<int(dist[a][b+1])):
                        dist[a][b+1]=alt

        if(flag==0):
            #print nodepop
            #print a,b
            seen[a][b]=1
            while store:
                storepop=heappop(store)
                heappush(Q,(storepop[0],node(storepop[1].x,storepop[1].y)))
                #heapify(Q)
    # your implementation here
    for item in dist:
        print item
    #for item in seen:
    #    print item
    return dist[end[0]][end[1]]

#print graph
#print seen
#print dist

start=getcell(+1); assert start[0]>=0 and start[1]>=0
end=getcell(-1);   assert end[0]>=0   and end[1]>=0
#print end[0], end[1]
find_distance(start,end)
print "shortest path distance:", dist[end[0]][end[1]]

