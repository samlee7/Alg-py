#!/usr/bin/env python2.7
#
# CS 141 Spring 2012
#
################################

import sys, random, timeit
from math import sqrt

BASE=256
CAP=1024

def gcd(a, b):
    while b>0:
        r=a%b; a=b; b=r
    return a

# return (g,x,y) 
# such that a*x + b*y = g
def extgcd(a, b):
    if b==0: return (a, 1, 0)
    g, xx, yy = extgcd(b, a%b)
    q=a/b
    return (g, yy, xx-q*yy)

# return the multiplicative inverse of a modulo p
# assume gcd(a,p)=1
def inv(a, p):
    g,x,y = extgcd(a,p)
    x=x%p
    if x<0: x+=p
    return x
    
# Miller-Rabin primality test
# source
# http://en.literateprograms.org/Miller-Rabin_primality_test_%28Python%29#chunk%20use:Miller-Rabin
def is_prime(n):
    d = n-1; s=0
    while d%2==0:
        d >>= 1; s += 1
    for repeat in xrange(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, s, d, n):
            return False
    return True

def miller_rabin_pass(a, s, d, n):
    a_to_power = pow(a, d, n)
    if a_to_power == 1: return True
    for i in xrange(s-1):
        if a_to_power == n-1: return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n-1

def generate_random_prime(approx_bits):
    candidate = 4; modulus = 2
    if approx_bits == 0: approx_bits = 1
    modulus = pow(2, approx_bits)

    while True:
        candidate = random.randrange(modulus) + modulus
        if is_prime(candidate): 
            return candidate


# generate a random integer in 2..modulus-1
# among those having a multiplicative inverse mod modulus
def generate_random_invertible(modulus):
    candidate=1
    while True:
        candidate = random.randrange(1,modulus-1)+1
        if gcd(candidate, modulus)==1:
            return candidate


# generates an RSA key with n-bit modulus N
# return [p, q, N, e, d]
def gen_key(number_of_bits):
    p = generate_random_prime(number_of_bits/2)
    q = generate_random_prime(number_of_bits/2)
    e = generate_random_invertible(number_of_bits)

    while(p==q):
        q = generate_random_prime(number_of_bits/2)

    N=p*q
    phi=(q-1)*(p-1)

    while(gcd(e,phi)!=1):
        e=generate_random_invertible(number_of_bits)

    d=inv(e,phi)

    return [p,q,N,e,d]	
    pass


def rsa_encrypt(x, e, N):
    ret = []

    for i in x:
        c=pow(i,e,N)
        ret.append(c)

    return ret
    pass

def rsa_decrypt(x, d, N):
    ret = []

    for i in x:
        m=pow(i,d,N)
        ret.append(m)

    return ret
    pass

def rsa_break(e, N):
    for i in xrange(1, int(sqrt(N))):
        if(N%i==0):
            factor1=i
    factor2 = N/factor1
    phi=(factor1-1)*(factor2-1)
	
    return inv(e,phi)
    pass

def text_to_numbers(N, str):
    ret = []
    l = len(str)
    p = 0; x = 0
    while p<l:
        x = x*BASE + ord(str[p])
        p += 1
        if x*BASE >= N: 
            ret.append(x)
            x = 0
    return ret

def parse(N, num):
    ret=[]
    while num>0:
        ret.append(num % BASE)
        num/=BASE
    ret.reverse()
    return ret
    
def numbers_to_text(N, l):
    strlst=[]
    for num in l:
        strlst.extend(parse(N, num))
    return ''.join([chr(num) for num in strlst])

# test code
if __name__=='__main__':

    # test text_to_numbers()
    # and numbers_to_text()
    N=1024
    message='computer science'
    bits=40
    
    print ("message to encrypt \"" + message + "\"")
    x = text_to_numbers(CAP, message)
    print ("text to num conversion: " + str(x))

    key=gen_key(bits)
    p=key[0]
    print ("p: " +str(p))
    q=key[1]
    print ("q: " +str(q))
    N=key[2]
    print ("N: " +str(N))
    e=key[3]
    print ("e: " +str(e))
    d=key[4]
    print ("d: " +str(d))


    cc = rsa_encrypt(x,e,N)
    print ("encrypted message: " + str(cc))

    dd = rsa_decrypt(cc,d,N)
    print ("decrypted message: " + str(dd))

    print("rsa break: "+str(rsa_break(e, N)))
    t=timeit.Timer(lambda: rsa_break(e, N))
    print str(t.timeit(1)) + " seconds"

    origm = numbers_to_text(CAP, dd)

    print ("original message is: \"" + origm + "\"")
