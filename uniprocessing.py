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
            raise TypeError('Error in codon ' + str(c+1) + ': codon must be '
                            'string, not ' + type(chain[c]))
        if len(chain[c]) != 3:
            raise ValueError('Error in codon ' + str(c+1) + ': number of '
                             'nucleotides equal to ' + str(len(chain[c])) +
                             ', must be 3')
        for n in range(len(chain[c])):
            if chain[c][n].upper() not in pattern:
                raise KeyError('Error in codon ' + str(c+1) + ', nucleotide ' +
                               str(n+1) + ': unexpected nucleotide - ' +
                               chain[c][n])

    # Process input chain
    processed_chain = []
    for c in chain:
        codon = ''
        for n in c:
            codon += pattern[n.upper()]
        processed_chain.append(codon)

    return processed_chain
