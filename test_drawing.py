from smu import *

# string describing transducer that inserts and/or deletes
# up to 3 symbols in the input word. Alpahbet = {a, b}
r = '@Transducer 0 1 2 3 * 0\n'\
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
print 'The program reads an automaton or transducer from a string'
print 'and then saves a picture of the machine in a file.'
print

t = fio.readOneFromString (s)
t.makePNG('zt_suffix')
  
print
raw_input('Press <enter> to terminate the program...')
