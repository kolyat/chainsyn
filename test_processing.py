# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license.
# See the file LICENSE.txt included in this distribution
"""
Module "test_processing" contains unit-tests to processing module

TestSliceChain - test to slice_chain()
TestReplication - tests to replication()
TestTranscription - tests to transcription()
TestRevTranscription - tests to rev_transcription()
TestTranslation - tests to translation()
"""
import unittest

from processing import slice_chain
from processing import replication
from processing import transcription
from processing import rev_transcription
from processing import translation


class TestSliceChain(unittest.TestCase):
    """
    Class TestSliceChain contains tests to slice_chain()
    """

    # Positive tests
    def test_one_codon(self):
        """
        Input chain with three nucleotides - one codon
        """
        self.assertEqual(slice_chain('atc'), ['atc'])

    def test_three_codons(self):
        """
        Input chain with nine nucleotides - three codons
        """
        self.assertEqual(slice_chain('acgaccagg'), ['acg', 'acc', 'agg'])

    # Negative tests
    def test_type(self):
        """
        Incorrect type
        """
        self.assertRaises(TypeError, slice_chain, ['a', 'c', 'g'])

    def test_empty_chain(self):
        """
        Input chain is empty
        """
        self.assertRaises(ValueError, slice_chain, '')

    def test_two_nucleotides(self):
        """
        Input chain contains two nucleotides (less than in codon)
        """
        self.assertRaises(ValueError, slice_chain, 'at')

    def test_four_nucleotides(self):
        """
        Input chain contains five nucleotides (more than one but less than two
        codons)
        """
        self.assertRaises(ValueError, slice_chain, 'atcga')


class TestReplication(unittest.TestCase):
    """
    Class TestReplication contains tests to replication()
    """
    correct_dna = ['TTT', 'AAA', 'GGG', 'CCC']

    # Positive tests
    def test_correct_lower(self):
        """
        Correct codons in lower case
        """
        self.assertEqual(replication(['aaa', 'ttt', 'ccc', 'ggg']),
                         self.correct_dna)

    def test_correct_upper(self):
        """
        Correct codons in upper case
        """
        self.assertEqual(replication(['AAA', 'TTT', 'CCC', 'GGG']),
                         self.correct_dna)

    # Negative tests
    def test_integer(self):
        """
        Not supported type - integer
        """
        self.assertRaises(TypeError, replication, 3)

    def test_empty(self):
        """
        Empty list
        """
        self.assertRaises(ValueError, replication, [])

    def test_dictionary(self):
        """
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, replication,
                          ['aaa', {'a': 't', 'c': 'g'}])

    def test_empty_codon(self):
        """
        Chain with empty codon
        """
        self.assertRaises(ValueError, replication, ['aaa', ''])

    def test_forbidden_char(self):
        """
        String with invalid characters
        """
        self.assertRaises(KeyError, replication, ['aaa', 'axc'])


class TestTranscription(unittest.TestCase):
    """
    Class TestTranscription contains tests to transcription()
    """
    correct_mrna = ['UUU', 'AAA', 'GGG', 'CCC']

    # Positive tests
    def test_correct_lower(self):
        """
        Correct codons in lower case
        """
        self.assertEqual(transcription(['aaa', 'ttt', 'ccc', 'ggg']),
                         self.correct_mrna)

    def test_correct_upper(self):
        """
        Correct codons in upper case
        """
        self.assertEqual(transcription(['AAA', 'TTT', 'CCC', 'GGG']),
                         self.correct_mrna)

    # Negative tests
    def test_integer(self):
        """
        Not a list (integer)
        """
        self.assertRaises(TypeError, transcription, 3)

    def test_empty(self):
        """
        Empty list
        """
        self.assertRaises(ValueError, transcription, [])

    def test_dictionary(self):
        """
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, transcription, ['aaa', {'a': 't'}])

    def test_empty_codon(self):
        """
        Chain with empty codon
        """
        self.assertRaises(ValueError, replication, ['aaa', ''])

    def test_forbidden_char(self):
        """
        Codon with invalid characters
        """
        self.assertRaises(KeyError, transcription, ['aaa', 'cXg'])


class TestRevTranscription(unittest.TestCase):
    """
    Class TestRevTranscription contains tests to rev_transcription()
    """
    correct_dna = ['TTT', 'AAA', 'GGG', 'CCC']

    # Positive tests
    def test_correct_lower(self):
        """
        Correct codons in lower case
        """
        self.assertEqual(rev_transcription(['aaa', 'uuu', 'ccc', 'ggg']),
                         self.correct_dna)

    def test_correct_upper(self):
        """
        Correct codons in upper case
        """
        self.assertEqual(rev_transcription(['AAA', 'UUU', 'CCC', 'GGG']),
                         self.correct_dna)

    # Negative tests
    def test_integer(self):
        """
        Not a list (integer)
        """
        self.assertRaises(TypeError, rev_transcription, 3)

    def test_empty(self):
        """
        Empty list
        """
        self.assertRaises(ValueError, rev_transcription, [])

    def test_dictionary(self):
        """
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, rev_transcription, ['aaa', {'c': 'g'}])

    def test_empty_codon(self):
        """
        Chain with empty codon
        """
        self.assertRaises(ValueError, rev_transcription, ['aaa', ''])

    def test_forbidden_char(self):
        """
        Codon with invalid characters
        """
        self.assertRaises(KeyError, rev_transcription, ['aaa', 'cXg'])


class TestTranslation(unittest.TestCase):
    """
    Class TestTranslation contains tests to translation()
    """
    @classmethod
    def setUpClass(cls):
        """Initialize correct mRNA with all possible codons"""
        mrna = []
        mrna_lower = []
        for n1 in ['U', 'C', 'A', 'G']:
            for n2 in ['U', 'C', 'A', 'G']:
                for n3 in ['U', 'C', 'A', 'G']:
                    mrna.append(str(n1 + n2 + n3))
                    mrna_lower.append(str(n1.lower() + n2.lower() +
                                          n3.lower()))
        cls.correct_mrna = mrna
        cls.correct_mrna_lower = mrna_lower

    correct_peptide = [
        'Phe', 'Phe', 'Leu', 'Leu', 'Ser', 'Ser', 'Ser', 'Ser',
        'Tyr', 'Tyr', 'xxx', 'xxx', 'Cys', 'Cys', 'xxx', 'Trp',
        'Leu', 'Leu', 'Leu', 'Leu', 'Pro', 'Pro', 'Pro', 'Pro',
        'His', 'His', 'Gln', 'Gln', 'Arg', 'Arg', 'Arg', 'Arg',
        'Ile', 'Ile', 'Ile', 'Met', 'Thr', 'Thr', 'Thr', 'Thr',
        'Asn', 'Asn', 'Lys', 'Lys', 'Ser', 'Ser', 'Arg', 'Arg',
        'Val', 'Val', 'Val', 'Val', 'Ala', 'Ala', 'Ala', 'Ala',
        'Asp', 'Asp', 'Glu', 'Glu', 'Gly', 'Gly', 'Gly', 'Gly'
    ]

    # Positive tests
    def test_correct_lower(self):
        """
        Correct string with nucleotides in lower case
        """
        self.assertEqual(translation(self.correct_mrna_lower),
                         self.correct_peptide)

    def test_correct_upper(self):
        """
        Correct string with nucleotides in upper case
        """
        self.assertEqual(translation(self.correct_mrna), self.correct_peptide)

    # Negative tests
    def test_integer(self):
        """
        Not a list (integer)
        """
        self.assertRaises(TypeError, translation, 3)

    def test_empty(self):
        """
        Empty list
        """
        self.assertRaises(ValueError, translation, [])

    def test_dictionary(self):
        """
        Not supported type - dictionary
        """
        self.assertRaises(TypeError, translation,
                          ['AAA', {'c': 'g', 'u': 'a'}])

    def test_empty_codon(self):
        """
        Chain with empty codon
        """
        self.assertRaises(ValueError, translation, ['aaa', ''])

    def test_forbidden_char(self):
        """
        Codon with invalid nucleotides
        """
        self.assertRaises(KeyError, translation, ['aaa', 'axc'])


if __name__ == '__main__':
    unittest.main()
