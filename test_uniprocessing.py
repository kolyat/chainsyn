# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license.
# See the file LICENSE.txt included in this distribution

"""
Module "test_uniprocessing" contains unit-tests to uniprocessing module

TestProcess - test to process() function
"""

import unittest

from uniprocessing import *


class TestProcess(unittest.TestCase):
    """
    Test cases for process() function
    """

    # Tests with DNA pattern
    def test_pattern_dna_AAA(self):
        """DNA pattern, AAA-codon"""
        self.assertEqual(process(['aaa'], pattern_dna), ['TTT'])

    def test_pattern_dna_TTT(self):
        """DNA pattern, TTT-codon"""
        self.assertEqual(process(['ttt'], pattern_dna), ['AAA'])

    def test_pattern_dna_CCC(self):
        """DNA pattern, CCC-codon"""
        self.assertEqual(process(['CCC'], pattern_dna), ['GGG'])

    def test_pattern_dna_GGG(self):
        """DNA pattern, GGG-codon"""
        self.assertEqual(process(['GGG'], pattern_dna), ['CCC'])

    def test_pattern_dna_UUU(self):
        """DNA pattern, UUU-codon"""
        self.assertRaises(KeyError, process, ['UUU'], pattern_dna)

    # Tests with mRNA pattern
    def test_pattern_mrna_AAA(self):
        """mRNA pattern, AAA-codon"""
        self.assertEqual(process(['aaa'], pattern_mrna), ['UUU'])

    def test_pattern_mrna_TTT(self):
        """mRNA pattern, TTT-codon"""
        self.assertEqual(process(['ttt'], pattern_mrna), ['AAA'])

    def test_pattern_mrna_CCC(self):
        """mRNA pattern, CCC-codon"""
        self.assertEqual(process(['CCC'], pattern_mrna), ['GGG'])

    def test_pattern_mrna_GGG(self):
        """mRNA pattern, GGG-codon"""
        self.assertEqual(process(['GGG'], pattern_mrna), ['CCC'])

    def test_pattern_mrna_UUU(self):
        """mRNA pattern, UUU-codon"""
        self.assertRaises(KeyError, process, ['UUU'], pattern_mrna)

    # Test with reversed DNA pattern
    def test_pattern_dna_rev_AAA(self):
        """Reversed DNA pattern, AAA-codon"""
        self.assertEqual(process(['aaa'], pattern_dna_rev), ['TTT'])

    def test_pattern_dna_rev_TTT(self):
        """Reversed DNA pattern, TTT-codon"""
        self.assertRaises(KeyError, process, ['ttt'], pattern_dna_rev)

    def test_pattern_dna_rev_CCC(self):
        """Reversed DNA pattern, CCC-codon"""
        self.assertEqual(process(['CCC'], pattern_dna_rev), ['GGG'])

    def test_pattern_dna_rev_GGG(self):
        """Reversed DNA pattern, GGG-codon"""
        self.assertEqual(process(['GGG'], pattern_dna_rev), ['CCC'])

    def test_pattern_dna_rev_UUU(self):
        """Reversed DNA pattern, UUU-codon"""
        self.assertEqual(process(['UUU'], pattern_dna_rev), ['AAA'])

    # Negative tests for 'chain' argument
    def test_chain_invalid_type(self):
        """Chain - invalid type"""
        self.assertRaises(TypeError, process, 3, pattern_dna)

    def test_chain_empty(self):
        """Chain - empty"""
        self.assertRaises(ValueError, process, [], pattern_dna)

    def test_chain_bad_codon(self):
        """Chain - codon contains one nucleotide"""
        self.assertRaises(ValueError, process, ['a'], pattern_dna)

    # Negative tests for 'pattern' argument
    def test_pattern_invalid_type(self):
        """Pattern - invalid type"""
        self.assertRaises(TypeError, process, ['aaa'], 3)

    def test_pattern_empty(self):
        """Pattern - empty"""
        self.assertRaises(ValueError, process, ['aaa'], {})

    def test_invalid_pattern(self):
        """Pattern is incorrect"""
        self.assertRaises(KeyError, process, ['aaa'], {'A': '1', 'T': '2',
                                                       'C': '3', 'G': '4'})


if __name__ == '__main__':
    unittest.main()
