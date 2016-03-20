# coding=utf-8
"""Tranducers and codes tests"""
import unittest
import re
from smu import *

# import FAdo.fio as fio
# from FAdo.reex import str2regexp
# from FAdo.transducers import *
# import FAdo.codes as codes
# import FAdo.fl as fl

#-------------->    GLAVIN:  please read all comments below carefully

def sat_with_symbolic_SFT(a, s):
    # return s
    ## when ready, remove the above line, and use the following statement
    return s.match(a.toSFT(a)).emptyP()    # s = symbolic SFT,  a = NFA

def check_satisfaction(transducer_file, nfa_file, expected_result):
        t = fio.readOneFromFile("datafiles/"+transducer_file)
        a = fio.readOneFromFile("datafiles/"+nfa_file)
        # if isinstance(t, SymbolicSFT):
        #     r = t.match(a.toSFT(a))
        # else:
        r = t.inIntersection(a).outIntersection(a)
        p = t.productInput(a)
        image_file = "images/"+transducer_file+"+"+nfa_file
        # print(image_file)
        d = r.toDFA().renameStates()
        r.makePNG(image_file)
        d.makePNG(image_file+"+DFA")
        p.toDFA().makePNG(image_file+"+productInput")
        # print(d)
        return (r.emptyP() is expected_result)

class MyTestCase(unittest.TestCase):

    def test_Satisfaction(self):        # This tests ordinary SFTs
        """ Satisfaction Test """       # The one below tests symbolic SFTs

        tests = [
            ["TR-sub1_ia.ab.fa", "NFA-EvenBMult03A.fa", True],
            ["TR-sub1_ia.abc.fa", "NFA-EvenBMult03A.abc.fa", True],
            ["TR-sid1_ia.ab.fa", "NFA-EvenBMult03A.fa", True],
            ["TR-sid1_ia.abc.fa", "NFA-EvenBMult03A.abc.fa", False],
            ["TR-infix.ab.fa", "NFA-EvenBMult03A.fa", False],
        ]
        for (transducer_file, nfa_file, expected_result) in tests:
            self.assertTrue(check_satisfaction(transducer_file,nfa_file,expected_result), transducer_file+" and "+nfa_file+" was not "+str(expected_result))

    def test_SYMBOLIC_Satisfaction(self):
        """ Symbolic Satisfaction Test """
        #
        #----> when ready, remove the lines  "t = True"  and  "t = False",
        #      and uncomment all lines below that start with  #t = fio....

        tests = [
            ["TRS-sub1_ia.fa", "NFA-EvenBMult03A.fa", True],
            ["TRS-sub1_ia.fa", "NFA-EvenBMult03A.abc.fa", True],
            ["TRS-sid1_ia.fa", "NFA-EvenBMult03A.fa", True],
            ["TRS-sid1_ia.fa", "NFA-EvenBMult03A.abc.fa", False],
            ["TRS-infix.fa", "NFA-EvenBMult03A.fa", False],
        ]
        for (transducer_file, nfa_file, expected_result) in tests:
            self.assertTrue(check_satisfaction(transducer_file,nfa_file,expected_result), transducer_file+" and "+nfa_file+" was not "+str(expected_result))


if __name__ == '__main__':
    unittest.main()
