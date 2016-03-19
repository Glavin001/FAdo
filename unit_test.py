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
    return s
    ## when ready, remove the above line, and use the following statement
    return s.match(a.toSFT(a)).emptyP()    # s = symbolic SFT,  a = NFA

class MyTestCase(unittest.TestCase):

    def test_Satisfaction(self):        # This tests ordinary SFTs
        """ Satisfaction Test """       # The one below tests symbolic SFTs
        #
        t = fio.readOneFromFile("datafiles/TR-sub1_ia.ab.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertTrue(t.inIntersection(a).outIntersection(a).emptyP())
        #
        t = fio.readOneFromFile("datafiles/TR-sub1_ia.abc.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
        self.assertTrue(t.inIntersection(a).outIntersection(a).emptyP())
        #
        t = fio.readOneFromFile("datafiles/TR-sid1_ia.ab.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertTrue(t.inIntersection(a).outIntersection(a).emptyP())
        #
        t = fio.readOneFromFile("datafiles/TR-sid1_ia.abc.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
        self.assertFalse(t.inIntersection(a).outIntersection(a).emptyP())
        #
        t = fio.readOneFromFile("datafiles/TR-infix.ab.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertFalse(t.inIntersection(a).outIntersection(a).emptyP())

    def test_SYMBOLIC_Satisfaction(self):
        """ Symbolic Satisfaction Test """
        #
        #----> when ready, remove the lines  "t = True"  and  "t = False",
        #      and uncomment all lines below that start with  #t = fio....
        #
        t = True
        #t = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertTrue(sat_with_symbolic_SFT(a, t))
        #
        #t = fio.readOneFromFile("datafiles/TRS-sub1_ia.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
        self.assertTrue(sat_with_symbolic_SFT(a, t))
        #
        #t = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertTrue(sat_with_symbolic_SFT(a, t))
        #
        t = False
        #t = fio.readOneFromFile("datafiles/TRS-sid1_ia.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.abc.fa")
        self.assertFalse(sat_with_symbolic_SFT(a, t))
        #
        #t = fio.readOneFromFile("datafiles/TRS-infix.fa")
        a = fio.readOneFromFile("datafiles/NFA-EvenBMult03A.fa")
        self.assertFalse(sat_with_symbolic_SFT(a, t))

if __name__ == '__main__':
    unittest.main()
