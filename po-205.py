#!/usr/bin/env python3

"""
Charles McEachern

https://www.hackerrank.com/contests/projecteuler/challenges/euler205
"""

import collections
import fractions
import math

# ######################################################################

MODULUS = 1012924417

def main():
    ncases = int( input() )
    [ solve_case() for _ in range(ncases) ]
    return

# ######################################################################

def solve_case():
    np, sp, nc, sc = [ int(x) for x in input().split() ]
    # If Pete has zero dice, he never wins.
    if np == 0:
        print(0)
        return
    # Figure out the number of ways for Pete to roll exactly X.
    prolls = []
    for p in range(np*sp+1):
        prolls.append( ways_to_roll(p, np, sp) )
    # Figure out the number of ways for Colin to roll less than X.
    crolls = [0]
    for c in range(nc*sc+1):
        crolls.append( crolls[-1] + ways_to_roll(c, nc, sc) )
    # Total number of outcomes is sp**np * sc**nc
    total = (sp**np) * (sc**nc)
    # Figure out how many of those have p > c.
    pwins = 0
    for i, p in enumerate(prolls):
        # For each number Pete can roll, how many ways are there for him
        # to roll it, and how many of Colin's rolls does he beat?
        pwins += p*crolls[i]
    # Report the fraction.
    return report(pwins, total)

# ----------------------------------------------------------------------

def report(p, q):
    gcd = fractions.gcd(p, q)
    miq = modinv(q//gcd, MODULUS)
    return print( ( p//gcd * miq ) % MODULUS )

# ######################################################################

def ways_to_roll(pips, ndice, nsides):
    '''Accept integers P, N, S. Return the number of ways to roll P pips
    on NdS.
    '''
    if pips < ndice or pips > ndice*nsides:
        return 0
    # Figure out all the different arrangements of pips that can get us
    # to the target number. Then, for each arrangement of pips, figure
    # out how many ways it can be rolled.
    ways = 0
    for part in partitions(pips, ndice, nsides):
        # The number of ways to roll (1, 1, 1, 4, 7, 7) on six dice is
        # 7!/(3! 1! 2!).
        tallies = collections.defaultdict(int)
        for p in part:
            tallies[p] += 1
        denoms = sorted( tallies.values() )
        choices = choose(ndice, *denoms)
        ways += choices
    return ways

# ######################################################################

def partitions(pips, ndice, nsides):
    '''Accepts three integer arguments: P, N, S. Determine all possible
    ways to roll P pips between N dice with S sides each. Return a set
    of tuples.
    '''
    # Start with the minimum case: all dice roll 1.
    parts = { tuple( [1]*ndice ) }
    # Bifurcate all ways of rolling 4 to all ways of rolling 5, etc,
    # until we get to our target.
    for _ in range(pips - ndice):
        parts = increment_partitions(parts, ndice, nsides)
    return parts

# ----------------------------------------------------------------------

def increment_partitions(parts, ndice, nsides):
    new_parts = set()
    # Each time we increment, find all the arrangements that roll 1
    # more pip. So (1, 1, 2) turns into (2, 1, 2), (1, 2, 2), and
    # (1, 1, 3).
    for part in parts:
        for i in range(ndice):
            tmp = list(part)
            tmp[i] += 1
            # Throw away anything that has a d6 rolling 7.
            if tmp[i] <= nsides:
                # Store as a set of sorted tuples to collapse (1, 2, 2)
                # and (2, 1, 2).
                new_parts.add( tuple( sorted(tmp) ) )
    return new_parts

# ######################################################################

def choose(n, *args):
    numerator = math.factorial(n)
    denominator = 1
    for k in args:
        denominator *= math.factorial(k)
    return numerator//denominator

# ######################################################################

def modinv(a, m):
    # Extended Euclidian Algorithm for modular inverses.
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

# ----------------------------------------------------------------------

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# ######################################################################

if __name__ == '__main__':
    main()
