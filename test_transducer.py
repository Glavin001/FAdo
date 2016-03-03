from smu import *

# string describing transducer that inserts and/or deletes
# up to 3 symbols in the input word. Alpahbet = {a, b}
s = '@Transducer 0 1 2 3 * 0\n'\
 '0 a a 0\n'\
 '0 b b 0\n'\
 '0 @epsilon a 1\n'\
 '0 @epsilon b 1\n'\
 '0 a @epsilon 1\n'\
 '0 b @epsilon 1\n'\
 '1 a a 1\n'\
 '1 b b 1\n'\
 '1 @epsilon a 2\n'\
 '1 @epsilon b 2\n'\
 '1 a @epsilon 2\n'\
 '1 b @epsilon 2\n'\
 '2 a a 2\n'\
 '2 b b 2\n'\
 '2 @epsilon a 3\n'\
 '2 @epsilon b 3\n'\
 '2 a @epsilon 3\n'\
 '2 b @epsilon 3\n'\
 '3 a a 3\n'\
 '3 b b 3\n'

# string describing transducer that returns any possibl
# suffix of the input word. Alphabet = {0, 1}
s = '@Transducer 1 2 * 1\n'\
 '1 0 @epsilon 1\n'\
 '1 1 @epsilon 1\n'\
 '1 0 0 2\n'\
 '1 1 1 2\n'\
 '2 0 0 2\n'\
 '2 1 1 2\n'

print
print 'The program reads a string, and prints all strings resulting by'
print 'applying a transducer to the given string.'
print

t = fio.readOneFromString (s)
print 'The input alphabet of the transducer is:'
for s in t.Sigma: print s,
print
while True:
    w = raw_input('\nEnter string> ')
    print '--> '
    a = words2NFA ([w])
    b = t.runOnNFA(a).elimEpsilon().trim()
    print b.enumNFA(len(w))
  
print
raw_input('Press <enter> to terminate the program...')
