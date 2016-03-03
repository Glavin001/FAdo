import unittest
from smu import *
from datetime import datetime

nfa1ts = '@NFA 1 * 0\n'\
        '0 0 0\n'\
        '0 1 1\n'

nfa2ts = '@NFA 1 * 0\n'\
        '0 0 0\n'\
        '0 1 0\n'\
        '0 2 0\n'\
        '0 1 1\n'

sft1ts = '@Transducer 1 * 0\n'\
        '0 0 0 0\n'\
        '0 1 1 0\n'\
        '0 1 0 1\n'\
        '0 0 1 1\n'\
        '1 0 0 1\n'\
        '1 1 1 1\n'

sft2ts = '@Transducer 1 * 0\n'\
        '0 0 0 0\n'\
        '0 1 1 0\n'\
        '0 2 2 0\n'\
        '0 0 1 1\n'\
        '0 0 2 1\n'\
        '0 1 0 1\n'\
        '0 1 2 1\n'\
        '0 2 0 1\n'\
        '0 2 1 1\n'\
        '1 0 0 1\n'\
        '1 1 1 1\n'\
        '1 2 2 1\n'


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
        # nfa1.makePNG('images/nfa1')
        self.assertTrue(isinstance(nfa1, NFA))

    def testParseNFA2(self):
        nfa2 = fio.readOneFromString(nfa2ts)
        # nfa2.makePNG('images/nfa2')
        self.assertTrue(isinstance(nfa2, NFA))

    def testParseSFT1(self):
        sft1 = fio.readOneFromString(sft1ts)
        # sft1.makePNG('images/sft1')
        self.assertTrue(isinstance(sft1, SFT))

    def testParseSSFT1(self):
        ssft1 = fio.readOneFromString(ssft1ts)
        # ssft1.makePNG('images/ssft1')
        self.assertTrue(isinstance(ssft1, SSFT))

    def testParseSSFT2(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        # ssft2.makePNG('images/ssft2')
        self.assertTrue(isinstance(ssft2, SSFT))

    def testProductInput1(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        self.assertTrue(isinstance(ssft2, SSFT))
        sft1 = fio.readOneFromString(sft1ts)
        self.assertTrue(isinstance(sft1, SFT))
        nfa1 = fio.readOneFromString(nfa1ts)
        self.assertTrue(isinstance(nfa1, NFA))

        a = datetime.now()
        prod1 = sft1.runOnNFA(nfa1)
        b = datetime.now()
        prod1.makePNG('images/prod1')
        c = b - a

        a = datetime.now()
        sprod1 = ssft2.runOnNFA(nfa1)
        b = datetime.now()
        sprod1.makePNG('images/sprod1')

        # Check that they are the same
        self.assertTrue(prod1.toDFA().equal(sprod1.toDFA()))

        # Check that this is faster
        # self.assertLess(b - a, c)


    def testProductInput2(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        self.assertTrue(isinstance(ssft2, SSFT))
        sft1 = fio.readOneFromString(sft2ts)
        self.assertTrue(isinstance(sft1, SFT))
        nfa1 = fio.readOneFromString(nfa2ts)
        self.assertTrue(isinstance(nfa1, NFA))

        a = datetime.now()
        prod1 = sft1.runOnNFA(nfa1)
        b = datetime.now()
        prod1.makePNG('images/prod2')
        c = b - a

        a = datetime.now()
        sprod1 = ssft2.runOnNFA(nfa1)
        b = datetime.now()
        sprod1.makePNG('images/sprod2')

        # Check that they are the same
        self.assertTrue(prod1.toDFA().equal(sprod1.toDFA()))

        # Check that this is faster
        # self.assertLess(b - a, c)


if __name__ == '__main__':
    unittest.main()

'''

'''

