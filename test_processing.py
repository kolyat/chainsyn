# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license.
# See the file LICENSE.txt included in this distribution
"""
Module "test_processing" contains unit-tests to processing module

TestReplication - tests to replication()
"""
import unittest

from processing import replication


class TestReplication(unittest.TestCase):
    """
    Class TestReplication contains tests to replication()
    """
    correct = ['t', 'a', 'g', 'c']

    def test_positive(self):
        """Positive tests"""

        """Correct string with nucleotides in lower case"""
        self.assertEqual(replication('atcg'), self.correct)
        """Correct string with nucleotides in upper case"""
        self.assertEqual(replication('ATCG'), self.correct)
        """Correct list of nucleotides"""
        self.assertEqual(replication(['a', 't', 'c', 'g']), self.correct)
        """Correct tuple of nucleotides"""
        self.assertEqual(replication(('a', 't', 'c', 'g')), self.correct)

    def test_negative(self):
        """Negative tests"""

        """Empty string"""
        self.assertRaises(ValueError, replication, '')
        """String with uracil (U)"""
        self.assertRaises(ValueError, replication, 'atcgu')
        """String with forbidden characters"""
        self.assertRaises(ValueError, replication, 'XYZat123cg#$%')
        """String with forbidden characters and uracil in first place"""
        self.assertRaises(ValueError, replication, 'uXYZat123cg#$%')
        """String with forbidden characters and uracil
        somewhere in the middle"""
        self.assertRaises(ValueError, replication, 'XuYZat123cg#$%')
        """Not a string (integer)"""
        self.assertRaises(TypeError, replication, 3)
        """Unicode string with Russian 'АТС'"""
        self.assertRaises(UnicodeError, replication, 'АТС')
        """Not supported type - dictionary"""
        self.assertRaises(TypeError, replication, {'a':'t', 'c':'g'})

if __name__ == '__main__':
    unittest.main()
