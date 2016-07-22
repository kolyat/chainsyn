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
        dna_chain -- string, list or tuple with nucleotides (A, T, C, G)

    Returns list with nucleotides of second DNA chain

    Raises an exception if fails:
        - TypeError -- when dna_chain is not string, list or tuple;
        - ValueError -- when dna_chain is empty or contains forbidden
                        characters (non-alphabetic)
        - KeyError - when dna_chain contains not valid nucleotides
    """
    dna_pattern = {
        'a': 't',   # Adenine associates with thymine (A-T)
        't': 'a',   # Thymine associates with adenine (T-A)
        'c': 'g',   # Cytosine associates with guanine (C-G)
        'g': 'c'    # Guanine associates with cytosine (G-C)
    }
    # Check if dna_chain is correct type and not empty
    if type(dna_chain) not in (str, list, tuple):
        raise TypeError
    if len(dna_chain) == 0:
        raise ValueError
    # Try to convert input dna_chain to list of nucleotides
    dna1_chain = []
    for el in list(dna_chain):
        try:
            dna1_chain.append(el.lower())
        except ValueError:
            # dna_chain might contain non-alphabetic characters
            break
    # Try to replicate DNA chain
    dna2_chain = []
    for n in dna1_chain:
        if n in dna_pattern:
            dna2_chain.append(dna_pattern[n])
        else:
            raise KeyError
    return dna2_chain
