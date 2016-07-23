# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution
"""
Module "processing" with processing functions

replication() - function of DNA replication
transcription() - function of transcription from DNA to mRNA
"""


def replication(dna_chain):
    """
    Function of DNA replication (DNA -> DNA)

    Arguments:
        dna_chain -- string, list or tuple with DNA nucleotides (A, T, C, G)

    Returns list of second DNA chain nucleotides

    Raises an exception if fails:
        - TypeError -- when dna_chain is not string, list or tuple;
        - ValueError -- when dna_chain is empty or contains forbidden
                        characters (non-alphabetic)
        - KeyError - when dna_chain contains not valid nucleotides
    """
    dna_pattern = {
        'A': 'T',   # Adenine associates with thymine (A-T)
        'T': 'A',   # Thymine associates with adenine (T-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
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
            dna1_chain.append(el.upper())
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


def transcription(dna_chain):
    """
    Function of transcription (DNA -> mRNA)

    Arguments:
        dna_chain -- string, list or tuple with DNA nucleotides (A, T, C, G)

    Returns list mRNA nucleotides

    Raises an exception if fails:
        - TypeError -- when dna_chain is not string, list or tuple;
        - ValueError -- when dna_chain is empty or contains forbidden
                        characters (non-alphabetic)
        - KeyError - when dna_chain contains not valid nucleotides
    """
    mrna_pattern = {
        'A': 'U',   # Adenine associates with uracil (A-U)
        'T': 'A',   # Thymine associates with adenine (T-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
    }
    # Check if dna_chain is correct type and not empty
    if type(dna_chain) not in (str, list, tuple):
        raise TypeError
    if len(dna_chain) == 0:
        raise ValueError
    # Try to convert input dna_chain to list of nucleotides
    dna = []
    for el in list(dna_chain):
        try:
            dna.append(el.upper())
        except ValueError:
            # dna_chain might contain non-alphabetic characters
            break
    # Try to transcript mRNA
    mrna = []
    for n in dna:
        if n in mrna_pattern:
            mrna.append(mrna_pattern[n])
        else:
            raise KeyError
    return mrna
