# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license.
# See the file LICENSE.txt included in this distribution
"""
Module "test_processing" contains unit-tests to processing module

TestReplication - tests to replication()
TestTranscription - tests to transcription()
"""
import unittest

from processing import replication
from processing import transcription


class TestReplication(unittest.TestCase):
    """
    Class TestReplication contains tests to replication()
    """
    correct_dna = ['T', 'A', 'G', 'C']

    def test_correct_lower(self):
        """
        Positive test
        Correct string with nucleotides in lower case
        """
        self.assertEqual(replication('atcg'), self.correct_dna)

    def test_correct_upper(self):
        """
        Positive test
        Correct string with nucleotides in upper case
        """
        self.assertEqual(replication('ATCG'), self.correct_dna)

    def test_correct_list(self):
        """
        Positive test
        Correct list of nucleotides
        """
        self.assertEqual(replication(['a', 't', 'c', 'g']), self.correct_dna)

    def test_correct_tuple(self):
        """
        Positive test
        Correct tuple of nucleotides
        """
        self.assertEqual(replication(('a', 't', 'c', 'g')), self.correct_dna)

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


class TestTranscription(unittest.TestCase):
    """
    Class TestReplication contains tests to transcription()
    """
    correct_mrna = ['U', 'A', 'G', 'C']

    def test_correct_lower(self):
        """
        Positive test
        Correct string with nucleotides in lower case
        """
        self.assertEqual(transcription('atcg'), self.correct_mrna)

    def test_correct_upper(self):
        """
        Positive test
        Correct string with nucleotides in upper case
        """
        self.assertEqual(transcription('ATCG'), self.correct_mrna)

    def test_correct_list(self):
        """
        Positive test
        Correct list of nucleotides
        """
        self.assertEqual(transcription(['a', 't', 'c', 'g']), self.correct_mrna)

    def test_correct_tuple(self):
        """
        Positive test
        Correct tuple of nucleotides
        """
        self.assertEqual(transcription(('a', 't', 'c', 'g')), self.correct_mrna)

    def test_empty(self):
        """
        Negative test
        Empty string
        """
        self.assertRaises(ValueError, transcription, '')

    def test_uracil(self):
        """
        Negative test
        String with uracil (U)
        """
        self.assertRaises(KeyError, transcription, 'atcgu')

    def test_forbidden_char(self):
        """
        Negative test
        String with forbidden characters
        """
        self.assertRaises(KeyError, transcription, 'XYZat123cg#$%')

    def test_forbidden_uracil_first(self):
        """
        Negative test
        String with forbidden characters and uracil in first place
        """
        self.assertRaises(KeyError, transcription, 'uXYZat123cg#$%')

    def test_forbidden_uracil_mid(self):
        """
        Negative test
        String with forbidden characters and uracil
        somewhere in the middle
        """
        self.assertRaises(KeyError, transcription, 'XuYZat123cg#$%')

    def test_integer(self):
        """
        Negative test
        Not a string (integer)
        """
        self.assertRaises(TypeError, transcription, 3)

    def test_unicode(self):
        """
        Negative test
        Unicode string with Russian 'АТС'
        """
        self.assertRaises(KeyError, transcription, 'АТС')

    def test_dictionary(self):
        """
        Negative test
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, transcription, {'a':'t', 'c':'g'})

if __name__ == '__main__':
    unittest.main()
