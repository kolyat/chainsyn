# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution
"""
Module "processing" with processing functions

slice_chain() - function that slices input chain into codons
replication() - function of DNA replication
transcription() - function of transcription from DNA to mRNA
translation() - function of translation from mRNA to polypeptide chain
rev_transcription() - function of reverse transcription from mRNA to DNA
"""


def slice_chain(chain):
    """
    Function that slices input chain into codons

    Arguments:
        chain - input chain of nucleotides, must be divisible by 3

    Returns list of codons

    Raises an exception if fails:
        - TypeError: when input chain is not string, list or tuple
        - ValueError:
        --- if chain is empty
        --- when chain's length is not divisible by 3
    """
    # Necessary checks
    if type(chain) not in (str, list, tuple):
        raise TypeError('Type of input chain must be string, list or tuple')
    if len(chain) == 0:
        raise ValueError('Input chain is empty')
    if len(chain) % 3 != 0:
        raise ValueError('Length of chain must be divisible by 3')

    str_chain = list(str(chain))
    output_chain = []
    while len(str_chain) > 0:
        codon = []
        for i in range(3):
            codon.append(str_chain.pop(0))
        output_chain.append(codon)
    return output_chain


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

    Returns list of mRNA nucleotides

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


def translation(mrna_chain):
    """
    Function of translation (mRNA -> polypeptide chain)

    Arguments:
        mrna_chain -- string, list or tuple with mRNA nucleotides (A, U, C, G)

    Returns list of polypeptide chain

    Raises an exception if fails:
        - TypeError -- when mrna_chain is not string, list or tuple;
        - ValueError -- when mrna_chain is empty, contains forbidden
                        characters (non-alphabetic) or number of nucleotides
                        is not divisible by 3
        - KeyError - when mrna_chain contains not valid nucleotides
    """
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
    # Check if mrna_chain is correct type, not empty and divisible by 3
    if type(mrna_chain) not in (str, list, tuple):
        raise TypeError
    if len(mrna_chain) == 0 or len(mrna_chain) % 3 != 0:
        raise ValueError
    # Try to convert mrna_chain list of nucleotides to upper case
    mrna_raw = []
    for el in list(mrna_chain):
        try:
            mrna_raw.append(el.upper())
        except ValueError:
            # mrna_chain might contain non-alphabetic characters
            break
    # Slice mrna_raw to list of nucleotide triplets (codons)
    mrna = []
    while len(mrna_raw) > 0:
        codon = ""
        for i in range(3):
            codon = codon + mrna_raw.pop(0)
        mrna.append(codon)
    # Try to translate mRNA to polypeptide chain
    peptide = []
    for codon in mrna:
        if codon in peptide_pattern:
            peptide.append(peptide_pattern[codon])
        else:
            raise KeyError
    return peptide


def rev_transcription(mrna_chain):
    """
    Function of reverse transcription (mRNA -> DNA)

    Arguments:
        mrna_chain -- string, list or tuple with mRNA nucleotides (A, U, C, G)

    Returns list of DNA nucleotides

    Raises an exception if fails:
        - TypeError -- when mrna_chain is not string, list or tuple;
        - ValueError -- when mrna_chain is empty or contains forbidden
                        characters (non-alphabetic)
        - KeyError - when mrna_chain contains not valid nucleotides
    """
    dna_pattern = {
        'A': 'T',   # Adenine associates with thymine (A-T)
        'U': 'A',   # Uracil associates with adenine (U-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
    }
    # Check if mrna_chain is correct type and not empty
    if type(mrna_chain) not in (str, list, tuple):
        raise TypeError
    if len(mrna_chain) == 0:
        raise ValueError
    # Try to convert input mrna_chain to list of nucleotides
    mrna = []
    for el in list(mrna_chain):
        try:
            mrna.append(el.upper())
        except ValueError:
            # mrna_chain might contain non-alphabetic characters
            break
    # Try to transcript DNA
    dna = []
    for n in mrna:
        if n in dna_pattern:
            dna.append(dna_pattern[n])
        else:
            raise KeyError
    return dna
