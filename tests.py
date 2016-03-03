import unittest
from smu import *

ssft1 = '@Transducer 0 1 2 * 0\n'\
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

class SymbolicTransducerTestCase(unittest.TestCase):

    def testParser(self):
        t = fio.readOneFromString(ssft1)
        t.makePNG('images/ssft1')

if __name__ == '__main__':
    unittest.main()

'''

'''

