# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

# TODO: module description
""""""

import re
import patterns


class ProcessingErr(Exception):
    """Exception class for processing errors"""
    pass


class Chain(object):
    """Main class for chain processing"""

    info, raw, dna1, dna2 = '', '', '', ''

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
                'Error in replication: unexpected nucleotide - {} '
                'at position {}'.format(invalid.group(0), invalid.start())
            )
        self.dna1 = self.raw
        dna = list()
        for n in self.dna1:
            dna.append(patterns.dna_to_dna[n])
        self.dna2 = ''.join(dna)
        return self.dna2
