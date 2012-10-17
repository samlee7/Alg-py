#!/usr/bin/env python2.7
#
# CS 141, Lab 5
# Closest Pair
# Sam Lee
############################

import sys
from operator import itemgetter
from math import sqrt
from random import random

def merge(P1,P2):
    k=0
    l=0
    while(l<len(P2)) or (k<len(P1)):
        if (l>=len(P2)) or (k<len(P1) and P1[k][1]<=P2[l][1]):
            yield P1[k]
            k=k+1
        else:
            yield P2[l]
            l=l+1

def dist(p1, p2):
	def sqr(x): return x*x
	return sqrt(sqr(p1[0]-p2[0]) + sqr(p1[1]-p2[1]))


# input: pts[], a list of points 
# return: d, a floating point number that is 
# the min dist between any two points
# computed using dist() function
def closest_pair(pts):
	# TODO your implementation here
	d = [dist(pts[0],pts[1]), (pts[0],pts[1])]
	
	def compare(P1,Q1):
		nd=dist(P1,Q1)
		if nd<d[0]:
			d[0]=nd
			d[1]=P1,Q1

	def recursive(pts):
		if len(pts)<=1:
			return pts
		hLength=len(pts)/2
		hLengthArray=pts[hLength][0]
		pts=list(merge(recursive(pts[:hLength]), recursive(pts[hLength:])))

		oRange=[p for p in pts if abs(p[0]-hLengthArray)<d[0]]
		for k in range(len(oRange)):
			for l in range(1,8):
				if k+l<len(oRange):
					compare(oRange[k],oRange[k+l])
		return pts

	pts.sort()
	recursive(pts)
	return d[0]
	
def slow_cp(pts):
	n = len(pts)
	if n<2: return 0
	d = dist(pts[0], pts[1])
	for i in range(n-1):
		for j in range(i+1, n):
			d = min(d, dist(pts[i], pts[j]))
	return d

pts=[]
for line in sys.stdin:
	x = float(line.split()[0])
	y = float(line.split()[1])
	pts.append((x,y))

# read pts from input
EPS=1.0e-6
d1 = closest_pair(pts)
#d2 = slow_cp(pts)
print d1, #d2
#assert (abs(d1-d2)<=EPS) or (abs(d1-d2)/max(d1,d2)<=EPS)
