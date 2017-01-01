# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Module "uniprocessing" with patterns and universal processing function

process() - function that process one chain to another using given pattern

Valid patterns:
pattern_dna - to replicate another DNA chain
pattern_mrna - to transcript mRNA from DNA
pattern_dna_rev - to transcript DNA from mRNA (reverted transcription)
"""


pattern_dna = {
    'A': 'T',  # Adenine - Thymine
    'T': 'A',  # Thymine - Adenine
    'C': 'G',  # Cytosine - Guanine
    'G': 'C'   # Guanine - Cytosine
}
pattern_mrna = {
    'A': 'U',  # Adenine - Uracil
    'T': 'A',  # Thymine - Adenine
    'C': 'G',  # Cytosine - Guanine
    'G': 'C'   # Guanine - Cytosine
}
pattern_dna_rev = {
    'A': 'T',  # Adenine - Thymine
    'U': 'A',  # Uracil - Adenine
    'C': 'G',  # Cytosine - Guanine
    'G': 'C'   # Guanine - Cytosine
}

valid_patterns = (pattern_dna, pattern_mrna, pattern_dna_rev)


def slice_chain(chain):
    """
    Function that slices input chain into codons

    :param chain: input chain of nucleotides, must be divisible by 3
    :type chain: str

    :return list of codons (strings)

    :raise TypeError: when input chain is not string
    :raise ValueError: if chain is empty or chain's length is not divisible
                        by 3
    """

    # Necessary checks
    if type(chain) != str:
        raise TypeError('Type of input chain must be string, list or tuple')
    if not chain:
        raise ValueError('Input chain is empty')
    if len(chain) % 3 != 0:
        raise ValueError('Length of chain must be divisible by 3')

    raw_chain = list(chain)
    output_chain = []
    while len(raw_chain) > 0:
        codon = ''
        for i in range(3):
            codon += raw_chain.pop(0)
        output_chain.append(codon)
    return output_chain


def process(chain, pattern):
    """
    Function of universal processing

    :parameter chain: codons (strings) with nucleotides
    :type chain: list

    :parameter pattern: any pattern (dictionary) which is used to build another
                        chain
    :type pattern: dictionary

    :returns list with codons (strings) of second chain

    :raises TypeError: when chain is not list, codon is not a string, pattern
                       is not a dictionary;
    :raises ValueError: when chain or pattern is empty, number of nucleotides
                        is not equal to 3;
    :raises KeyError: when codon contains not correct nucleotides or pattern is
                      not valid;
    """
    # Check if input chain is correct type and not empty
    if type(chain) != list:
        raise TypeError('Input chain must be list of codons')
    if not chain:
        raise ValueError('Input chain is empty')
    # Check if input pattern is correct type and valid
    if type(pattern) != dict:
        raise TypeError('Input pattern must be dictionary type')
    if not pattern:
        raise ValueError('Input pattern is empty')
    if pattern not in valid_patterns:
        raise KeyError('Input pattern is not valid')
    # Check every codon of input chain
    for c in range(len(chain)):
        if type(chain[c]) != str:
            raise TypeError('Error in codon {}: codon must be '
                            'string, not {}'.format(c+1, type(chain[c])))
        if len(chain[c]) != 3:
            raise ValueError('Error in codon {}: number of '
                             'nucleotides equal to {}, '
                             'must be 3'.format(c+1, len(chain[c])))
        for n in range(len(chain[c])):
            if chain[c][n].upper() not in pattern:
                raise KeyError(
                    'Error in codon {}, '
                    'nucleotide {}: '
                    'unexpected nucleotide - '.format(c+1, n+1, chain[c][n]))

    # Process input chain
    processed_chain = []
    for c in chain:
        codon = ''
        for n in c:
            codon += pattern[n.upper()]
        processed_chain.append(codon)

    return processed_chain


def translation(mrna_chain):
    """
    Function of translation (mRNA -> polypeptide chain)

    :param mrna_chain: codons with mRNA nucleotides (A, U, C, G)
    :type mrna_chain: list

    :return list of polypeptide chain

    :raise TypeError: when mrna_chain is not list, codon is not string;
    :raise ValueError: when mrna_chain is empty, number of nucleotides is not
                        equal to 3
    :raise KeyError: when mrna_chain contains not valid nucleotides
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
        raise TypeError('Input mRNA chain must be list of codons')
    if len(mrna_chain) == 0:
        raise ValueError('Input mRNA chain is empty')
    # Check every codon
    for c in range(len(mrna_chain)):
        if type(mrna_chain[c]) != str:
            raise TypeError('Error in codon {}: codon must be '
                            'string, not {}'.format(c+1, type(mrna_chain[c])))
        if len(mrna_chain[c]) != 3:
            raise ValueError('Error in codon {}: number of '
                             'nucleotides equal to {}, '
                             'must be 3'.format(c+1, len(mrna_chain[c])))
        for n in range(len(mrna_chain[c])):
            if mrna_chain[c][n].upper() not in mrna_nucleotides:
                raise KeyError(
                    'Error in codon {}, '
                    'nucleotide {}: '
                    'unexpected nucleotide - {}'.format(c+1, n+1,
                                                        mrna_chain[c][n]))

    # Translate mRNA to polypeptide chain
    peptide = []
    for codon in mrna_chain:
        peptide.append(peptide_pattern[codon.upper()])
    return peptide
