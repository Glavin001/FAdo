'''#!/usr/bin/python'''

import fl
import fio
from fa import *
from reex import *
from transducers import *
from common import *
import codes
#from IPython.core.display import Image


def rex2NFA(r):    
    # r is a regular expression (a string); returns NFA accepting L(r). 
    # Example: a = rex2NFA('0*01')
    return str2regexp(r).toNFA().renameStates()


def makeMin(a):    
    # makes a minimal DFA copy of a; could be very slow
    # Example: ma = makeMin(a)
    return a.toDFA().minimal().trim().renameStates()


def words2NFA(lst):
    '''
    lst is a list of strings. 
    the function creates an NFA accepting exactly these strings
    It returns the the NFA
    '''
    aut = fl.FL(lst).trieFA().toNFA()
    return aut


def intersect(a, b):
# returns the intersection automaton of the two given ones
    a1 = a
    b1 = b
    if a.epsilonP(): a1 = a.dup().elimEpsilon()
    if b.epsilonP(): b1 = b.dup().elimEpsilon()
    c = a1 & b1
    lst = []
    for s in c.States:
        if s.find("'@empty_set'") >= 0: lst.append(c.stateIndex(s))
    c.deleteStates(lst)
    return c

