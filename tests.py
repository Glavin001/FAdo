import unittest
from datetime import datetime, timedelta
import cProfile

from smu import *

_PROFILE = False
NUM_RUNS = 2

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


ssft1ts = '@SymbolicTransducer 1 * 0\n'\
        '0 any any 0\n'\
        '0 any diff 1\n'\
        '1 any any 1\n'

ssft2ts = '@SymbolicTransducer 1 * 0\n'\
        '0 @s @s 0\n'\
        "0 @s @d 1\n"\
        '1 @s @s 1\n'

class ParserTestCase(unittest.TestCase):

    def test_NFA1(self):
        nfa1 = fio.readOneFromString(nfa1ts)
        # nfa1.makePNG('images/nfa1')
        self.assertTrue(isinstance(nfa1, NFA))

    def test_NFA2(self):
        nfa2 = fio.readOneFromString(nfa2ts)
        # nfa2.makePNG('images/nfa2')
        self.assertTrue(isinstance(nfa2, NFA))

    def test_SFT1(self):
        sft1 = fio.readOneFromString(sft1ts)
        # sft1.makePNG('images/sft1')
        self.assertTrue(isinstance(sft1, SFT))

    def test_SymbolicSFT1(self):
        ssft1 = fio.readOneFromString(ssft1ts)
        # ssft1.makePNG('images/ssft1')
        self.assertTrue(isinstance(ssft1, SymbolicSFT))

    def test_SymbolicSFT2(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        # ssft2.makePNG('images/ssft2')
        self.assertTrue(isinstance(ssft2, SymbolicSFT))

class NFATestCase(unittest.TestCase):

    def test_allTransitions(self):
        nfa1 = fio.readOneFromString(nfa1ts)
        self.assertTrue(isinstance(nfa1, NFA))
        ts = [t for t in nfa1.allTransitions()]
        # print(ts)
        self.assertTrue(len(ts) is 2)

        nfa2 = fio.readOneFromString(nfa2ts)
        self.assertTrue(isinstance(nfa2, NFA))
        ts = [t for t in nfa2.allTransitions()]
        # print(ts)
        self.assertTrue(len(ts) is 4)

    def test_toSFT(self):
        nfa1 = fio.readOneFromString(nfa1ts)
        self.assertTrue(isinstance(nfa1, NFA))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFAtoSFT")
        # print(T)
        # self.assertTrue(len(ts) is 2)

class SymbolicSFTTestCase(unittest.TestCase):

    def test_runOnNFA_1(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        self.assertTrue(isinstance(ssft2, SymbolicSFT))
        sft1 = fio.readOneFromString(sft1ts)
        self.assertTrue(isinstance(sft1, SFT))
        nfa1 = fio.readOneFromString(nfa1ts)
        self.assertTrue(isinstance(nfa1, NFA))

        t = timedelta(0)
        st = timedelta(0)
        profile = cProfile.Profile()
        sprofile = cProfile.Profile()
        for i in xrange(1,NUM_RUNS):
            a = datetime.now()
            if _PROFILE: profile.enable()
            prod1 = sft1.runOnNFA(nfa1)
            if _PROFILE: profile.disable()
            b = datetime.now()
            c = b - a
            t += c

            a = datetime.now()
            if _PROFILE: sprofile.enable()
            sprod1 = ssft2.runOnNFA(nfa1)
            if _PROFILE: sprofile.disable()
            b = datetime.now()
            d = b - a
            st += d

        prod1.makePNG('images/prod2')
        sprod1.makePNG('images/sprod2')

        # Check that they are the same
        self.assertTrue(prod1.toDFA().equal(sprod1.toDFA()))

        # Profiling
        if _PROFILE:
            print("Using SFT:")
            profile.print_stats()
            print("Using SymbolicSFT:")
            sprofile.print_stats()

        # Check that this is faster
        # print("SymbolicSFT: {0}, SFT: {1}".format(st, t))
        # self.assertLess(st, t)

    def test_runOnNFA_2(self):
        ssft2 = fio.readOneFromString(ssft2ts)
        self.assertTrue(isinstance(ssft2, SymbolicSFT))
        sft1 = fio.readOneFromString(sft2ts)
        self.assertTrue(isinstance(sft1, SFT))
        nfa1 = fio.readOneFromString(nfa2ts)
        self.assertTrue(isinstance(nfa1, NFA))

        t = timedelta(0)
        st = timedelta(0)
        profile = cProfile.Profile()
        sprofile = cProfile.Profile()
        for i in xrange(1,NUM_RUNS):
            a = datetime.now()
            if _PROFILE: profile.enable()
            prod1 = sft1.runOnNFA(nfa1)
            if _PROFILE: profile.disable()
            b = datetime.now()
            c = b - a
            t += c

            a = datetime.now()
            if _PROFILE: sprofile.enable()
            sprod1 = ssft2.runOnNFA(nfa1)
            if _PROFILE: sprofile.disable()
            b = datetime.now()
            d = b - a
            st += d

        prod1.makePNG('images/prod2')
        sprod1.makePNG('images/sprod2')

        # Check that they are the same
        self.assertTrue(prod1.toDFA().equal(sprod1.toDFA()))

        # Profiling
        if _PROFILE:
            print("Using SFT:")
            profile.print_stats()
            print("Using SymbolicSFT:")
            sprofile.print_stats()

        # Check that this is faster
        # print("SymbolicSFT: {0}, SFT: {1}".format(st, t))
        # self.assertLess(st, t)

    def test_intersection_nonEmptyW(self):
        # A is NFA
        A = fio.readOneFromString(nfa1ts)
        # B is NFA
        B = fio.readOneFromString(nfa2ts)
        # S is SymbolicSFT
        S = fio.readOneFromString(ssft1ts)
        # ssft2 = fio.readOneFromString(ssft2ts)
        # T is SFT
        T = fio.readOneFromString(sft1ts)

        r = S.inIntersection(A).outIntersection(A)
        result = r.nonEmptyW()
        # print(result, result[0], result[1])
        # r.makePNG('images/in_out_intersection')
        self.assertTrue(result[0] is None)
        self.assertTrue(result[1] is None)

        # result = S.matchSFT(A.toSFT(A)).nonEmptyW()
        # self.assertTrue(result[0] is None)
        # self.assertTrue(result[1] is None)


if __name__ == '__main__':
    unittest.main()

'''

'''

