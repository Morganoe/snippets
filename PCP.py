#! /usr/bin/env python3
#
# Author: Morgan Eckenroth
#
# Greedy implementation of the Post Correspondance Problem
# as described in Sipser's Introduction to the Theory of 
# Computation, 3rd edition.
#
# Program is written to work in conjunction with the Theorem
# stating the the PCP is semideciable (can only accept an 
# accepting input)
#
# Algorithm is as follows:
# 3-tape NTM N = "on input <P> on tape #1:
#                 1) Set tape #2 and tape #3 to empty tapes.
#                 2) Nondeterministically pick a domino on tape #1 [u/v]
#                 3) Copy at the end of tape #2 u, and tape #3 v
#                 4) If tape #2 == tape #3 then accept, else goto 2. "


def delta(lst,q,a):
    if lst == []:
        return []
    else:
        if lst[0][0:2] ==  [q, a]:
            return lst[0][2:]
        else:
            return delta(lst[1:],q,a)

class TM:
    def __init__(self, language):
        self.tapeset = [TapeHead(right = list(language)), TapeHead(), TapeHead()]

class TapeHead:
    def __init__(self, left = [], head = '_', right = []):
        self.left = left
        self.head = head
        self.right = right
        self.units = []

    def __str__(self):
        return str(self.left) + ", " + str(self.head) + ", " + str(self.right)
    
    def __repr__(self):
        return str(self.left) + ", " + str(self.head) + ", " + str(self.right)

    def getTapeString(self):
        return "".join(self.left) + self.head + "".join(self.right)
    
    def getUnits(self, other):
        ret = []
        for i in range(len(self.units)):
            ret.append([self.units[i], other.units[i]])
        return ret

def moveRight(tapehead):
    if tapehead.right == []:
        return TapeHead(tapehead.left + [tapehead.head], "_", [])
    else:
        return TapeHead(tapehead.left + [tapehead.head], tapehead.right[0], tapehead.right[1:])

def moveLeft(taphead):
    if tapehead.left == []:
        return TapeHead([], tapehead.head, tapehead.right)
    else:
        return TapeHead(tapehead.left[:-1], tapehead.left[-1], [tapehead.head] + tapehead.right)

def replace(tapehead, b):
    return TapeHead(tapehead.left, b , tapehead.right)


def oneStepNTM(tapeset, w):
    ret = [None] * len(tapeset)
    ret[1] = moveRight(replace(tapeset[1], w[0]))
    ret[2] = moveRight(replace(tapeset[2], w[1]))

    # Keep track of tree branches steps in tape.
    ret[1].units.extend(tapeset[1].units)
    ret[1].units.append(w[0])
    ret[2].units.extend(tapeset[2].units)
    ret[2].units.append(w[1])
    return ret

from multiprocessing.dummy import Pool
import itertools
def simulateNTM(tm, P):
    working_tapes = [tm.tapeset]
    while True:
        temp = []
        for t in working_tapes:
            pool = Pool(len(P))
            results = pool.starmap(oneStepNTM, zip(itertools.repeat(t), P))
            pool.close()
            for i in results:
                if i[1].getTapeString() == i[2].getTapeString():
                    print(i[1].getTapeString())
                    print(i[2].getTapeString())
                    print(i[1].getUnits(i[2]))
                    return True
            temp.extend(results)
        working_tapes = temp

if __name__ == "__main__":
    lang = [['b','ca'],['a','ab'],['ca','a'],['abc','c']]
    #lang = [['b','ca'],['a','ab'],['ca','a']]  # Loops forever
    tm = TM(lang)
    simulateNTM(tm, lang)
