import unittest
from smu import *

nfa1ts = '@NFA 1 * 0\n'\
        '0 0 0\n'\
        '0 1 1\n'

sft1ts = '@Transducer 1 * 0\n'\
        '0 0 0 0\n'\
        '0 1 1 0\n'\
        '0 1 0 1\n'\
        '0 0 1 1\n'\
        '1 0 0 1\n'\
        '1 1 1 1\n'

ssft1ts = '@STransducer 1 * 0\n'\
        '0 any any 0\n'\
        '0 any diff 1\n'\
        '1 any any 1\n'

ssft2ts = '@STransducer 1 * 0\n'\
        '0 @s @s 0\n'\
        "0 @s @d 1\n"\
        '1 @s @s 1\n'


class SymbolicTransducerTestCase(unittest.TestCase):

    def testParseNFA1(self):
        nfa1 = fio.readOneFromString(nfa1ts)
        nfa1.makePNG('images/nfa1')
        self.assertTrue(isinstance(nfa1, NFA))

    def testParseSFT1(self):
        sft1 = fio.readOneFromString(sft1ts)
        sft1.makePNG('images/sft1')
        self.assertTrue(isinstance(sft1, SFT))

    def testParseSSFT1(self):
        ssft1 = fio.readOneFromString(ssft1ts)
        ssft1.makePNG('images/ssft1')
        self.assertTrue(isinstance(ssft1, SSFT))

    def testParseSSFT2(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        ssft2.makePNG('images/ssft2')
        self.assertTrue(isinstance(ssft2, SSFT))


        # t.productInput(a)
        # # does product construction between t and a
        # # but, when two transitions match it keeps both
        # # the input and output labels in the result
        # t.inIntersection(nfa)
        # # uses the above, but takes care of any empty
        # # input transitions and fixes final states
        # t.toOutNFA()
        # # returns NFA same as t but without the input labels
        # t.runOnNFA(a)

if __name__ == '__main__':
    unittest.main()

'''

'''

