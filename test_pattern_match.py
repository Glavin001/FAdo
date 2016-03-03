from smu import *


print
print 'The program reads repeatedly a text and a shorter pattern'
print 'and tells whether the text contains the pattern.'

while True:
    txt = raw_input('\nEnter text> ')
    p = raw_input('Enter pattern> ')
    alph = [c for c in txt+p]
    infix = infixTransducer(alph)
    txtinfix = infix.runOnWord(txt)
    # the next line is necessary in case p contains characters not in txt
    for c in p: txtinfix.Sigma.add(c)
    print '---> ', txtinfix.evalWordP(p)

  
