# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution
"""
Module "processing" with processing functions

replication() - function of DNA replication
"""


def replication(dna_chain):
    """
    Function of DNA replication (DNA -> DNA)

    Arguments:
        dna_chain -- string or list with nucleotides (A, T, C, G)

    Returns list with nucleotides of second DNA chain
    """
    dna_pattern = {
        'a': 't',   # Adenine associates with thymine (A-T)
        't': 'a',   # Thymine associates with adenine (T-A)
        'c': 'g',   # Cytosine associates with guanine (C-G)
        'g': 'c'    # Guanine associates with cytosine (G-C)
    }
    dna1_chain = dna_chain
    dna1_chain.lower()
    dna2_chain = []
    for n in dna1_chain:
        dna2_chain.append(dna_pattern[n])
    return dna2_chain
