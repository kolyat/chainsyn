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
        invalid = re.search('[^{}]+'.format(patterns.dna), self.raw)
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

def slice_chain(chain):
    """
    Slice input chain into codons

    :param chain: input chain of nucleotides, must be divisible by 3
    :type chain: str

    :return list of codons (strings)

    :raise ProcessErr:
      - input chain is not string
      - chain is empty
      - chain's length is not divisible by 3
    """

    # Necessary checks
    if type(chain) != str:
        raise ProcessErr('{}: type of input chain must be str, '
                         'got {}'.format(slice_chain.__name__, type(chain)))
    if not chain:
        raise ProcessErr('{}: input chain is '
                         'empty'.format(slice_chain.__name__))
    if len(chain) % 3 != 0:
        raise ProcessErr('{}: length of chain must be divisible by 3, '
                         'got {} nucleotides'.format(slice_chain.__name__,
                                                     len(chain)))

    raw_chain = list(chain)
    output_chain = []
    while len(raw_chain) > 0:
        codon = ''
        for i in range(3):
            codon += raw_chain.pop(0)
        output_chain.append(codon)
    return output_chain


def translation(mrna_chain):
    """
    Function of translation (mRNA -> polypeptide chain)

    :param mrna_chain: codons with mRNA nucleotides (A, U, C, G)
    :type mrna_chain: list

    :return list of polypeptide chain

    :raise ProcessErr:
      - mrna_chain is not list
      - codon is not str
      - mrna_chain is empty
      - number of nucleotides is not equal to 3
      - mrna_chain contains not valid nucleotides
    """

    mrna_nucleotides = ['A', 'U', 'C', 'G']
    peptide_pattern = {
        # Phenylalanine
        'UUU': 'Phe',
        'UUC': 'Phe',
        # Leucine
        'UUA': 'Leu',
        'UUG': 'Leu',
        'CUU': 'Leu',
        'CUC': 'Leu',
        'CUA': 'Leu',
        'CUG': 'Leu',
        # Serine
        'UCU': 'Ser',
        'UCC': 'Ser',
        'UCA': 'Ser',
        'UCG': 'Ser',
        'AGU': 'Ser',
        'AGC': 'Ser',
        # Proline
        'CCU': 'Pro',
        'CCC': 'Pro',
        'CCA': 'Pro',
        'CCG': 'Pro',
        # Histidine
        'CAU': 'His',
        'CAC': 'His',
        # Glutamine
        'CAA': 'Gln',
        'CAG': 'Gln',
        # Tyrosine
        'UAU': 'Tyr',
        'UAC': 'Tyr',
        # Stop codons
        'UAA': 'xxx',
        'UAG': 'xxx',
        'UGA': 'xxx',
        # Cysteine
        'UGU': 'Cys',
        'UGC': 'Cys',
        # Tryptophan
        'UGG': 'Trp',
        # Arginine
        'CGU': 'Arg',
        'CGC': 'Arg',
        'CGA': 'Arg',
        'CGG': 'Arg',
        'AGA': 'Arg',
        'AGG': 'Arg',
        # Isoleucine
        'AUU': 'Ile',
        'AUC': 'Ile',
        'AUA': 'Ile',
        # Methionine
        'AUG': 'Met',
        # Threonine
        'ACU': 'Thr',
        'ACC': 'Thr',
        'ACA': 'Thr',
        'ACG': 'Thr',
        # Asparagine
        'AAU': 'Asn',
        'AAC': 'Asn',
        # Lysine
        'AAA': 'Lys',
        'AAG': 'Lys',
        # Valine
        'GUU': 'Val',
        'GUC': 'Val',
        'GUA': 'Val',
        'GUG': 'Val',
        # Alanine
        'GCU': 'Ala',
        'GCC': 'Ala',
        'GCA': 'Ala',
        'GCG': 'Ala',
        # Aspartate
        'GAU': 'Asp',
        'GAC': 'Asp',
        # Glutamate
        'GAA': 'Glu',
        'GAG': 'Glu',
        # Glycine
        'GGU': 'Gly',
        'GGC': 'Gly',
        'GGA': 'Gly',
        'GGG': 'Gly',
    }

    # Check if mrna_chain is correct type and not empty
    if type(mrna_chain) != list:
        raise ProcessErr('{}: input mRNA chain must be list of codons, '
                         'got {}'.format(translation.__name__,
                                         type(mrna_chain)))
    if not mrna_chain:
        raise ProcessErr('{}: input mRNA chain '
                         'is empty'.format(translation.__name__))
    # Check every codon
    for c in range(len(mrna_chain)):
        if type(mrna_chain[c]) != str:
            raise ProcessErr('{}: error in codon {}: codon must be string, '
                             'not {}'.format(translation.__name__,
                                             c+1, type(mrna_chain[c])))
        if len(mrna_chain[c]) != 3:
            raise ProcessErr('{}: error in codon {}: number of nucleotides '
                             'equal to {}, '
                             'must be 3'.format(translation.__name__,
                                                c+1, len(mrna_chain[c])))
        for n in range(len(mrna_chain[c])):
            if mrna_chain[c][n].upper() not in mrna_nucleotides:
                raise ProcessErr(
                    '{}: error in codon {}, '
                    'nucleotide {}: '
                    'unexpected nucleotide - {}'.format(translation.__name__,
                                                        c+1, n+1,
                                                        mrna_chain[c][n]))

    # Translate mRNA to polypeptide chain
    peptide = []
    for codon in mrna_chain:
        peptide.append(peptide_pattern[codon.upper()])
    return peptide
