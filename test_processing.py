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

    def test_correct_lower(self):
        """
        Positive test
        Correct string with nucleotides in lower case
        """
        self.assertEqual(replication('atcg'), self.correct)

    def test_correct_upper(self):
        """
        Positive test
        Correct string with nucleotides in upper case
        """
        self.assertEqual(replication('ATCG'), self.correct)

    def test_correct_list(self):
        """
        Positive test
        Correct list of nucleotides
        """
        self.assertEqual(replication(['a', 't', 'c', 'g']), self.correct)

    def test_correct_tuple(self):
        """
        Positive test
        Correct tuple of nucleotides
        """
        self.assertEqual(replication(('a', 't', 'c', 'g')), self.correct)

    def test_empty(self):
        """
        Negative test
        Empty string
        """
        self.assertRaises(ValueError, replication, '')

    def test_uracil(self):
        """
        Negative test
        String with uracil (U)
        """
        self.assertRaises(KeyError, replication, 'atcgu')

    def test_forbidden_char(self):
        """
        Negative test
        String with forbidden characters
        """
        self.assertRaises(KeyError, replication, 'XYZat123cg#$%')

    def test_forbidden_uracil_first(self):
        """
        Negative test
        String with forbidden characters and uracil in first place
        """
        self.assertRaises(KeyError, replication, 'uXYZat123cg#$%')

    def test_forbidden_uracil_mid(self):
        """
        Negative test
        String with forbidden characters and uracil
        somewhere in the middle
        """
        self.assertRaises(KeyError, replication, 'XuYZat123cg#$%')

    def test_integer(self):
        """
        Negative test
        Not a string (integer)
        """
        self.assertRaises(TypeError, replication, 3)

    def test_unicode(self):
        """
        Negative test
        Unicode string with Russian 'АТС'
        """
        self.assertRaises(KeyError, replication, 'АТС')

    def test_dictionary(self):
        """
        Negative test
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, replication, {'a':'t', 'c':'g'})

if __name__ == '__main__':
    unittest.main()
