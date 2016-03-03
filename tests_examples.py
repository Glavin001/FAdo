import unittest
from smu import *

##  Input preserving transducers for error-detection
#
# Up to 1 substitution (IP transducer)
s1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 substitutions (IP transducer)
s2ts = '@Transducer 0 1 2 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'\
        '1 b a 2\n'\
        '1 a b 2\n'\
        '2 a a 2\n'\
        '2 b b 2\n'

# Up to 1 insertion and deletion (IP transducer)
id1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 @epsilon a 1\n'\
        '0 @epsilon b 1\n'\
        '0 a @epsilon 1\n'\
        '0 b @epsilon 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 insertions and deletions (IP transducer)
id2ts = '@Transducer 0 1 2 * 0\n'\
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
        '2 b b 2\n'

class MyTestCase(unittest.TestCase):

    def testOurPythonClasses(self):

        def _f1(p):
            self.assertTrue(isinstance(p, codes.SuffixProp))
            self.assertTrue(isinstance(p, codes.TrajProp))
            self.assertTrue(isinstance(p, codes.IATProp))
            self.assertTrue(isinstance(p, codes.IPTProp))
            self.assertTrue(isinstance(p, codes.ErrDetectProp))
            self.assertTrue(isinstance(p, codes.CodeProperty))

        p1 = codes.buildSuffixProperty({'a', 'b'})
        _f1(p1)
        p2 = codes.buildInfixProperty({'a', 'b'})
        _f1(p2)
        p3 = codes.buildHypercodeProperty({'a', 'b'})
        _f1(p3)
        p2 = codes.buildPrefixProperty({'a', 'b'})
        self.assertTrue(isinstance(p2, codes.IPTProp))
        self.assertTrue(isinstance(p1 & p2, codes.IATProp))
        ps1d = codes.buildErrorDetectPropS(s1ts)
        self.assertTrue(isinstance(ps1d, codes.ErrDetectProp))
        self.assertTrue(isinstance(ps1d, codes.IPTProp))
        self.assertFalse(isinstance(ps1d, codes.IATProp))
        self.assertFalse(isinstance(ps1d, codes.TrajProp))
        self.assertTrue(isinstance(ps1d, codes.CodeProperty))
        pud = codes.buildUDCodeProperty({'a', 'b'})
        self.assertFalse(isinstance(pud, codes.IPTProp))
        self.assertFalse(isinstance(pud, codes.IATProp))
        self.assertFalse(isinstance(pud, codes.TrajProp))
        self.assertTrue(isinstance(pud, codes.CodeProperty))

    def testFixedPropHierarchy1(self):
        ppx = codes.buildPrefixProperty({'a', 'b'})
        psx = codes.buildSuffixProperty({'a', 'b'})
        pix = codes.buildInfixProperty({'a', 'b'})
        pox = codes.buildOutfixProperty({'a', 'b'})
        phc = codes.buildHypercodeProperty({'a', 'b'})
        ppx1 = codes.buildPrefixProperty({'a', 'b'})
        pud = codes.buildUDCodeProperty({'a', 'b'})
        self.assertEqual(codes.isSubclass(psx, ppx), 0)
        # The next test is not really appropriate, as UD_codes are not IPTProp
        self.assertEqual(codes.isSubclass(pud, ppx), 2)
        self.assertEqual(codes.isSubclass(psx, pix), 2)
        self.assertEqual(codes.isSubclass(pox, ppx), 1)
        self.assertEqual(codes.isSubclass(phc, pix), 1)
        self.assertEqual(codes.isSubclass(pix, pox), 0)
        self.assertEqual(codes.isSubclass(ppx1, ppx), 3)
        p0 = ppx & ppx1
        self.assertEqual(codes.isSubclass(p0, ppx), 3)
        pbx = ppx & psx
        self.assertEqual(codes.isSubclass(pbx, ppx), 1)
        p1 = pix & psx
        p2 = pix & pix
        self.assertEqual(codes.isSubclass(p1, pix), 3)
        self.assertEqual(codes.isSubclass(p2, pix), 3)
        self.assertEqual(codes.isSubclass(p2, p1), 3)
        p3 = pix & pix & ppx
        self.assertEqual(codes.isSubclass(p2, p3), 3)
        p4 = p3 & ppx
        self.assertEqual(codes.isSubclass(p2, p4), 3)
        pbx1 = ppx & psx
        self.assertEqual(codes.isSubclass(pbx1, pbx), 3)
        self.assertEqual(codes.isSubclass(pix, pbx), 1)

    def testErrDetectPropHierarchy1(self):
        pixj = codes.buildTrajPropS('1*0*1*', {'a', 'b'})
        ppx = codes.buildPrefixProperty({'a', 'b'})
        pox = codes.buildOutfixProperty({'a', 'b'})
        ps1d = codes.buildErrorDetectPropS(s1ts)
        ps2d = codes.buildErrorDetectPropS(s2ts)
        pix_s2d = pixj & ps2d
        ps2d_ix = ps2d & pixj
        ppx_s2d = ppx & ps2d
        pox_s2d = pox & ps2d
        pid2d = codes.buildErrorDetectPropS(id2ts)
        self.assertEqual(codes.isSubclass(pix_s2d, pixj), 1)
        self.assertEqual(codes.isSubclass(ps2d_ix, pixj), 1)
        self.assertEqual(codes.isSubclass(pox_s2d, ppx_s2d), 1)
        self.assertEqual(codes.isSubclass(ps2d_ix, pixj), 1)
        self.assertEqual(codes.isSubclass(pox_s2d & ppx, pox_s2d & pid2d), 2)
        self.assertEqual(codes.isSubclass(pox_s2d & pid2d & ps1d, ppx_s2d & ppx), 1)
        self.assertEqual(codes.isSubclass(pix_s2d, ps2d_ix), 3)
        self.assertEqual(codes.isSubclass(pix_s2d, pix_s2d), 3)
        self.assertEqual(pix_s2d, pix_s2d)
        self.assertEqual(pix_s2d, ps2d_ix)
        icp = codes.buildTrajPropS('1*0*1*', {'a', 'b'})
        s = '@Transducer 1 * 0\n 0 a @epsilon 0\n 0 b @epsilon 0\n 0 a @epsilon 1\n 0 b @epsilon 1\n 1 a a 1\n 1 b b 1\n'
        scp = codes.buildIATPropS(s)
        self.assertEqual(codes.isSubclass(icp & scp, scp & icp), 3)
        self.assertEqual(scp & scp, scp)
        self.assertEqual(ppx & ppx & ppx, ppx)
        self.assertEqual(icp & scp, scp & icp)
        self.assertEqual(icp & scp & icp, scp & icp & scp)
        self.assertEqual(ppx & (icp & scp), (ppx & icp) & scp)



if __name__ == '__main__':
    unittest.main()

'''

'''

