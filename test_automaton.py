#!/usr/bin/python

from fa import *
from fio import readOneFromFile

print
print 'The program reads an automaton (in FAdo syntax) from a given file,'
print 'and then it keeps reading strings and tells whether each string is'
print 'accepted by the automaton. The program terminates if a given string'
print 'contains a symbols that is not in the alphabt of the automaton. '
print

fname = raw_input('\nEnter name of file containing the automaton: ')
A = readOneFromFile(fname)

print 'The alphabet of the automaton is:'
for s in A.Sigma: print s,
print
while True:
    w = raw_input('\nEnter string> ')
    print '--> ',
    ok = True
    for s in w:
        if s not in A.Sigma:
            ok = False
            break
    if not ok:
        print 'the string contains '+s+', which is not in the alphabet.'
        break
    else:
        print A.evalWordP(w)
print
raw_input('Press <enter> to terminate the program...')
