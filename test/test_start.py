# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license.
# See the file LICENSE.txt included in this distribution

"""
Module contains unit-tests for start module
"""

import unittest
import glob
import filecmp

from start import RoutineErr
from start import is_file
from start import from_file
from start import to_file


class TestIsFile(unittest.TestCase):
    """Tests for is_file()"""

    def test_positive(self):
        self.assertEqual(is_file('test_input.txt'), True)

    def test_negative(self):
        self.assertEqual(is_file('testinput'), False)


class TestFromFile(unittest.TestCase):
    """Tests for from_file()"""

    def test_readfile(self):
        pat = 'aaagggcccttt'
        self.assertEqual(from_file('test_input.txt'), pat)

    def test_wrong_file(self):
        self.assertRaises(RoutineErr, from_file, 'testinput')


class TestToFile(unittest.TestCase):
    """Tests for to_file()"""

    def test_write(self):
        to_file('', ['111'], ['222'], ['333'], ['444'])
        test_file = glob.glob('chains-*.txt')
        self.assertEqual(filecmp.cmp('test_output.txt', test_file[0]), True)

    def test_wrong_number_of_chains(self):
        self.assertRaises(RoutineErr, to_file, '', [])
        self.assertRaises(RoutineErr, to_file, '', [], [], [], [], [], [])

    def test_wrong_type(self):
        self.assertRaises(RoutineErr, to_file, '', {}, (), 1, 'aaa', [])

    def test_wrong_number_of_items(self):
        self.assertRaises(RoutineErr, to_file, '', ['', '', ''],
                          ['', '', '', ''], ['', '', ''], ['', '', ''])


if __name__ == '__main__':
    unittest.main()
