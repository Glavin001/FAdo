import unittest
from datetime import datetime, timedelta
import cProfile

from smu import *
import os

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


ssft1ts = '@STransducer 1 * 0\n'\
        '0 any any 0\n'\
        '0 any diff 1\n'\
        '1 any any 1\n'

ssft2ts = '@STransducer 1 * 0\n'\
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

    def test_TRS_sub1_ia(self):
        t = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
        self.assertTrue(isinstance(t, SymbolicSFT))

    def test_TRS_sid1_ia(self):
        t = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        self.assertTrue(isinstance(t, SymbolicSFT))


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

        nfa3 = fio.readOneFromFile("datafiles/NFA-small2.fa")
        self.assertTrue(isinstance(nfa3, NFA))
        ts = [t for t in nfa3.allTransitions()]
        # print(ts)
        self.assertTrue(len(ts) is 2)
        # print(ts)

    def test_toSFT1(self):
        nfa1 = fio.readOneFromString(nfa1ts)
        self.assertTrue(isinstance(nfa1, NFA))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFAtoSFT")
        # print(T)
        # self.assertTrue(len(ts) is 2)

    def test_toSFT2(self):
        nfa1 = fio.readOneFromFile("datafiles/NFA-small1.fa")
        self.assertTrue(isinstance(nfa1, NFA))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFA-small1+toSFT")

    def test_toSFT3(self):
        nfa1 = fio.readOneFromFile("datafiles/NFA-small2.fa")
        self.assertTrue(isinstance(nfa1, NFA))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFA-small2+toSFT")

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

        result = S.match(A.toSFT(A)).nonEmptyW()
        self.assertTrue(result[0] is None)
        self.assertTrue(result[1] is None)

    # def test_thing1(self):
    #     t = fio.readOneFromFile("datafiles/TR-sub1_ia.ab.fa")
    #     a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
    #     r = t.inIntersection(a).outIntersection(a)
    #     r.toDFA().makePNG("images/TR-sid1-EvenBMult03A")
    #     # r.makePNG("images/TR-sid1-EvenBMult03A")
    #     # r.makePNG("images/TR-sid1-EvenBMult03A")
    #     # print('Transducer')
    #     # print("States", r.States)
    #     # print("Sigma", r.Sigma)
    #     # print("Output", r.Output)
    #     # print("Initial", r.Initial)
    #     # print("Final", r.Final)
    #     # print("Delta", r.delta)
    #     self.assertTrue(r.emptyP())
    #     r1 = r
    #
    #     t = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
    #     a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
    #     a.makePNG("images/NFA-EvenBMult03A.fa")
    #     asft = a.toSFT(a)
    #     # print(asft.States)
    #     asft.makePNG("images/asft")
    #     r = t.match(asft)
    #     r.toDFA().makePNG("images/TRS-sid1-EvenBMult03A")
    #     # r.makePNG("images/TRS-sid1-EvenBMult03A")
    #     # r = t.inIntersection(a).outIntersection(a)
    #     # r.makePNG("images/TRS-sid1-EvenBMult03A")
    #     # print("SymbolicTransducer")
    #     # print("States", r.States)
    #     # print("Sigma", r.Sigma)
    #     # print("Output", r.Output)
    #     # print("Initial", r.Initial)
    #     # print("Final", r.Final)
    #     # print("Delta", r.delta)
    #     self.assertTrue(r.emptyP())
    #
    #     # Check that they are the same
    #     self.assertTrue(r1.toDFA().equal(r.toDFA()))
    #     self.assertTrue(r.toDFA().equal(r1.toDFA()))
    #
    # def test_thing2(self):
    #     t = fio.readOneFromFile("datafiles/TR-sid1_ia.abc.fa")
    #     a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
    #     r = t.inIntersection(a).outIntersection(a)
    #     r.toDFA().makePNG("images/TR-sid1-EvenBMult03A.abc")
    #     # r.makePNG("images/TR-sid1-EvenBMult03A.abc")
    #     # print('Transducer')
    #     # print("States", r.States)
    #     # print("Sigma", r.Sigma)
    #     # print("Output", r.Output)
    #     # print("Initial", r.Initial)
    #     # print("Final", r.Final)
    #     # print("Delta", r.delta)
    #     self.assertFalse(r.emptyP())
    #     r1 = r
    #
    #     t = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
    #     a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
    #     asft = a.toSFT(a)
    #     asft.makePNG("images/asft")
    #     r = t.match(asft)
    #     r.toDFA().makePNG("images/TRS-sid1-EvenBMult03A.abc")
    #     # r.makePNG("images/TRS-sid1-EvenBMult03A.abc")
    #     # r = t.inIntersection(a).outIntersection(a)
    #     # r.makePNG("images/TRS-sid1-EvenBMult03A")
    #     # print("SymbolicTransducer")
    #     # print("States", r.States)
    #     # print("Sigma", r.Sigma)
    #     # print("Output", r.Output)
    #     # print("Initial", r.Initial)
    #     # print("Final", r.Final)
    #     # print("Delta", r.delta)
    #     self.assertFalse(r.emptyP())
    #
    #     # Check that they are the same
    #     self.assertTrue(r1.toDFA().equal(r.toDFA()))
    #     self.assertTrue(r.toDFA().equal(r1.toDFA()))

    @unittest.skip("Skip for now")
    def test_satisfaction(self):
        def check_satisfaction(transducer_file, stransducer_file, nfa_file, expected_result):
            # Get input files
            t = fio.readOneFromFile("datafiles/"+transducer_file)
            st = fio.readOneFromFile("datafiles/"+stransducer_file)
            a = fio.readOneFromFile("datafiles/"+nfa_file)

            # Process
            r = t.inIntersection(a).outIntersection(a)
            sr = st.inIntersection(a).outIntersection(a)
            asft = a.toSFT(a)
            sr2 = st.match(asft)
            p = t.productInput(a)
            sp = st.productInput(a)

            # Save images
            folder = "images/test/"+nfa_file+"/"+transducer_file+"/"
            try:
                os.makedirs(folder)
            except:
                pass
            image_nfa_file = folder+nfa_file
            image_transducer_file = folder+transducer_file
            image_stransducer_file = folder+stransducer_file

            image_file = folder+transducer_file+"+"+nfa_file
            simage_file = folder+stransducer_file+"+"+nfa_file

            # d = r.toDFA().renameStates()
            # sd = sr.toDFA().renameStates()
            # sd2 = sr2.toDFA().renameStates()
            #
            def prep(d):
                return d.toDFA()

            # t.makePNG(image_transducer_file)
            # st.makePNG(image_stransducer_file)
            #
            # prep(r).makePNG(image_file)
            # prep(sr).makePNG(simage_file)
            # prep(sr2).makePNG(simage_file+"_2")
            # # d.makePNG(image_file+"+DFA")
            # prep(p).makePNG(image_file+"+productInput")
            # prep(sp).makePNG(simage_file+"+productInput")
            # prep(asft).makePNG(image_nfa_file+"+SFT")

            # Test productInput
            self.assertTrue(p.toDFA().equal(sp.toDFA()), "productInput of "+stransducer_file+" and "+nfa_file+" did not match "+transducer_file)

            # Test Intersection
            self.assertTrue(r.toDFA().equal(sr.toDFA()), "Intersection of "+stransducer_file+" and "+nfa_file+" did not match "+transducer_file)

            # Test toSFT
            # self.assertTrue(p.toDFA().equal(sp.toDFA()), "toSFT of "+stransducer_file+" and "+nfa_file+" did not match "+transducer_file)

            # Test Match & toSFT
            self.assertTrue(r.toDFA().equal(sr2.toDFA()), "Match of "+stransducer_file+" and "+nfa_file+" did not match "+transducer_file)

            # Test EmptyP
            self.assertTrue(sr.emptyP() == r.emptyP(), "EmptyP of "+stransducer_file+" and "+nfa_file+" (using intersection) did not match "+transducer_file)
            self.assertTrue(sr2.emptyP() == r.emptyP(), "EmptyP of "+stransducer_file+" and "+nfa_file+" (using match and toSFT) did not match "+transducer_file)
            self.assertTrue((r.emptyP() == expected_result), "EmptyP of "+transducer_file+" and "+nfa_file+" was not "+str(expected_result))
            self.assertTrue((sr.emptyP() == expected_result), "EmptyP of "+stransducer_file+" and "+nfa_file+" was not "+str(expected_result))

        tests = [
            ["TR-sub1_ia.ab.fa", "TRS-sub1_ia.fa", "NFA-EvenBMult03A.fa", True],
            ["TR-sub1_ia.abc.fa", "TRS-sub1_ia.fa", "NFA-EvenBMult03A.abc.fa", True],
            ["TR-sid1_ia.ab.fa", "TRS-sid1_ia.fa", "NFA-EvenBMult03A.fa", True],
            ["TR-sid1_ia.abc.fa", "TRS-sid1_ia.fa", "NFA-EvenBMult03A.abc.fa", False],
            ["TR-infix.ab.fa", "TRS-infix.fa", "NFA-EvenBMult03A.fa", False],
        ]

        for (transducer_file,stransducer_file, nfa_file, expected_result) in tests:
            check_satisfaction(transducer_file,stransducer_file,nfa_file,expected_result)

    @unittest.skip("Skip")
    def test_match_toSFT(self):
        nfa1 = fio.readOneFromFile("datafiles/NFA-small2.fa")
        st = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
        self.assertTrue(isinstance(nfa1, NFA))
        self.assertTrue(isinstance(st, SymbolicSFT))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFA-small2+toSFT")
        W = st.match(T)
        st.makePNG("images/TRS-sub1_ia")
        W.makePNG("images/TRS-sub1_ia+NFA-small2+match_toSFT")

    @unittest.skip("Skip")
    def test_match_toSFT2(self):
        nfa1 = fio.readOneFromFile("datafiles/NFA-small2.fa")
        st = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        self.assertTrue(isinstance(nfa1, NFA))
        self.assertTrue(isinstance(st, SymbolicSFT))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFA-small2+toSFT")
        W = st.match(T)
        st.makePNG("images/TRS-sid1_ia")
        W.makePNG("images/TRS-sid1_ia+NFA-small2+match_toSFT")

    def test_allTransitions(self):
        sid1 = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        sid1.makePNG("images/TRS-sid1_ia")
        self.assertTrue(isinstance(sid1, SymbolicSFT))
        ts = [t for t in sid1.allTransitions()]
        # print("sid1", ts)
        self.assertTrue(len(ts) is 5)
        # print(ts)

        sub1 = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
        self.assertTrue(isinstance(sub1, SymbolicSFT))
        ts = [t for t in sub1.allTransitions()]
        # print(ts)
        self.assertTrue(len(ts) is 3)

        nfa1 = fio.readOneFromFile("datafiles/NFA-small2.fa")
        self.assertTrue(isinstance(nfa1, NFA))
        T = nfa1.toSFT(nfa1)
        T.makePNG("images/NFA-small2+toSFT")
        self.assertTrue(isinstance(T, SFT))
        ts = [t for t in T.allTransitions()]
        # print("T", ts)
        self.assertTrue(len(ts) is 12)
        W = sid1.match(T)
        W.makePNG("images/TRS-sid1_ia+NFA-small2+match_toSFT")
        self.assertTrue(isinstance(W, SFT))
        ts = [t for t in W.allTransitions()]
        # print("W", ts)
        self.assertTrue(len(ts) is 14)

    def test_match(self):
        self.assertTrue(SymbolicSFT.matchLabels(AnySet, Epsilon, "a",Epsilon))
        # print(AnySet, Epsilon, "a",Epsilon)
        # print("@s", "@epsilon", "a","@epsilon")
        self.assertTrue(SymbolicSFT.matchLabels("@s", "@epsilon", "a","@epsilon"))

        # S = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        # nfa = fio.readOneFromFile("datafiles/NFA-small2.fa")
        # T = nfa.toSFT(nfa)
        #
        # for (s1, u, v, s2) in S.allTransitions():
        #     for (t1, x, y, t2) in T.allTransitions():
        #         print((u,v,x,y), SymbolicSFT.matchLabels(u,v,x,y))


if __name__ == '__main__':
    unittest.main()

'''

'''

