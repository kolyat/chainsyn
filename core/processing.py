# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Module contains utilities for chain processing"""

import re
from core import patterns


class ProcessingErr(Exception):
    """Exception class for processing errors"""
    pass


class Chain(object):
    """Main class for chain processing"""

    info, raw, dna1, dna2, rna, protein, stats = '', '', '', '', '', '', {}

    def __init__(self, info, raw):
        self.info = info
        self.raw = raw

    def replicate(self):
        """DNA -> DNA

        :raise ProcessingErr: if raw string contains nonDNA nucleotide

        :return replicated DNA chain
        """
        invalid = re.search('[^{}]+?'.format(patterns.dna), self.raw)
        if invalid:
            raise ProcessingErr(
                'Error in replication: unexpected DNA nucleotide - {} '
                'at position {}'.format(invalid.group(0), invalid.start())
            )
        self.dna1 = self.raw
        dna = list()
        for n in self.dna1:
            dna.append(patterns.dna_to_dna[n])
        self.dna2 = ''.join(dna)
        return self.dna2

    def transcribe(self):
        """DNA -> RNA

        :raise ProcessingErr: if raw string contains nonDNA nucleotide

        :return transcribed RNA chain
        """
        invalid = re.search('[^{}]+?'.format(patterns.dna), self.raw)
        if invalid:
            raise ProcessingErr(
                'Error in transcription: unexpected DNA nucleotide - {} '
                'at position {}'.format(invalid.group(0), invalid.start())
            )
        self.dna1 = self.raw
        rna = list()
        for n in self.dna1:
            rna.append(patterns.dna_to_rna[n])
        self.rna = ''.join(rna)
        return self.rna

    def translate(self):
        """RNA -> protein

        :raise ProcessingErr:
            - RNA's length is not divisible by 3
            - raw string contains nonRNA nucleotide
            - first codon is not AUG (methionine)
            - stop-codon is absent

        :return translated protein chain
        """
        if len(self.raw) % 3:
            raise ProcessingErr(
                'Error in translation: RNA\'s length should be divisible by 3,'
                ' current length - {}'.format(len(self.raw))
            )
        invalid = re.search('[^{}]+?'.format(patterns.rna), self.raw)
        if invalid:
            raise ProcessingErr(
                'Error in translation: unexpected RNA nucleotide - {} '
                'at position {}'.format(invalid.group(0), invalid.start())
            )
        check = re.match('{}'.format(patterns.abc_to_rna['M'][0]), self.raw)
        if not check:
            raise ProcessingErr(
                'Error in translation: RNA should start with {}'
                ''.format(patterns.abc_to_rna['M'][0])
            )
        check = re.search(
            '{}(?:...)*?({}|{}|{})'
            ''.format(
                patterns.abc_to_rna['M'][0], patterns.abc_to_rna['*'][0],
                patterns.abc_to_rna['*'][1], patterns.abc_to_rna['*'][2]),
            self.raw
        )
        if not check:
            raise ProcessingErr(
                'Error in translation: RNA should have stop-codon: ' +
                ' / '.join(patterns.abc_to_rna['*'])
            )
        self.rna = self.raw
        protein = list()
        for i in range(0, len(self.rna), 3):
            codon = self.rna[i:i+3]
            protein.append(patterns.rna_to_abc[codon])
            if codon in patterns.abc_to_rna['*']:
                break
        self.protein = ''.join(protein)
        return self.protein

    def collect_stats(self):
        """Collects statistics about available data

        :return: dict with stats
        """
        self.stats = dict()
        if self.dna1:
            self.stats.update({'nucleotides': len(self.dna1)})
            self.stats.update({'codons': len(self.dna1) // 3})
            gc = self.dna1.count('G') + self.dna1.count('C')
            gc_percentage = round(gc * 100 / len(self.dna1), 6)
            self.stats.update({'gc-content': gc_percentage})
        if self.protein:
            mass = 0.0
            for i in self.protein:
                mass += patterns.abc_mass[i]
            result = round(mass, ndigits=3)
            self.stats.update({'mass': result})
        return self.stats
