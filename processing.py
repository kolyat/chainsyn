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

    :parameter chain: input chain of nucleotides, must be divisible by 3
    :type chain: str

    :returns list of codons (strings)

    :raises TypeError: when input chain is not string
    :raises ValueError: if chain is empty or chain's length is not divisible
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


def replication(dna_chain):
    """
    Function of DNA replication (DNA -> DNA)

    :parameter dna_chain: codons (strings) with DNA nucleotides (A, T, C, G)
    :type dna_chain: list

    :returns list with codons (strings) of second DNA chain

    :raises TypeError: when dna_chain is not list, codon is not a string;
    :raises ValueError: when dna_chain is empty, number of nucleotides is not
                        equal to 3;
    :raises KeyError: when codon contains not valid nucleotides
    """
    dna_pattern = {
        'A': 'T',   # Adenine associates with thymine (A-T)
        'T': 'A',   # Thymine associates with adenine (T-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
    }

    # Check if dna_chain is correct type and not empty
    if type(dna_chain) != list:
        raise TypeError('Input DNA chain must be list of codons')
    if len(dna_chain) == 0:
        raise ValueError('Input DNA chain is empty')
    # Check every codon
    for c in range(len(dna_chain)):
        if type(dna_chain[c]) != str:
            raise TypeError('Error in codon ' + str(c+1) + ': codon must be '
                            'string, not ' + type(dna_chain[c]))
        if len(dna_chain[c]) != 3:
            raise ValueError('Error in codon ' + str(c+1) + ': number of '
                             'nucleotides equal to ' + str(len(dna_chain[c])) +
                             ', must be 3')
        for n in range(len(dna_chain[c])):
            if dna_chain[c][n].upper() not in dna_pattern:
                raise KeyError('Error in codon ' + str(c+1) + ', nucleotide ' +
                               str(n+1) + ': unexpected nucleotide - ' +
                               dna_chain[c][n])

    # Replicate DNA chain
    dna2_chain = []
    for c in dna_chain:
        codon = ''
        for n in c:
            codon += dna_pattern[n.upper()]
        dna2_chain.append(codon)

    return dna2_chain


def transcription(dna_chain):
    """
    Function of transcription (DNA -> mRNA)

    :parameter dna_chain: codons (strings) with DNA nucleotides (A, T, C, G)
    :type dna_chain: list

    :returns list of codons (strings) with mRNA nucleotides

    :raises TypeError: when dna_chain is not list, codon is not a string;
    :raises ValueError: when dna_chain is empty, number of nucleotides is not
                        equal to 3;
    :raises KeyError: when codon contains not valid nucleotides
    """
    mrna_pattern = {
        'A': 'U',   # Adenine associates with uracil (A-U)
        'T': 'A',   # Thymine associates with adenine (T-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
    }

    # Check if dna_chain is correct type and not empty
    if type(dna_chain) != list:
        raise TypeError('Input DNA chain must be list of codons')
    if len(dna_chain) == 0:
        raise ValueError('Input DNA chain is empty')
    # Check every codon
    for c in range(len(dna_chain)):
        if type(dna_chain[c]) != str:
            raise TypeError('Error in codon ' + str(c+1) + ': codon must be '
                            'string, not ' + type(dna_chain[c]))
        if len(dna_chain[c]) != 3:
            raise ValueError('Error in codon ' + str(c+1) + ': number of '
                             'nucleotides equal to ' + str(len(dna_chain[c])) +
                             ', must be 3')
        for n in range(len(dna_chain[c])):
            if dna_chain[c][n].upper() not in mrna_pattern:
                raise KeyError('Error in codon ' + str(c+1) + ', nucleotide ' +
                               str(n+1) + ': unexpected nucleotide - ' +
                               dna_chain[c][n])

    # Transcript DNA chain into mRNA
    mrna = []
    for c in dna_chain:
        codon = ''
        for n in c:
            codon += mrna_pattern[n.upper()]
        mrna.append(codon)

    return mrna


def rev_transcription(mrna_chain):
    """
    Function of reverse transcription (mRNA -> DNA)

    :parameter mrna_chain: codons with mRNA nucleotides (A, U, C, G)
    :type mrna_chain: list

    :returns list of codons with DNA nucleotides

    :raises TypeError: when mrna_chain is not list, codon is not a string;
    :raises ValueError: when mrna_chain is empty, number of nucleotides is not
                        equal to 3;
    :raises KeyError: when codon contains not valid nucleotides
    """
    dna_pattern = {
        'A': 'T',   # Adenine associates with thymine (A-T)
        'U': 'A',   # Uracil associates with adenine (U-A)
        'C': 'G',   # Cytosine associates with guanine (C-G)
        'G': 'C'    # Guanine associates with cytosine (G-C)
    }

    # Check if mrna_chain is correct type and not empty
    if type(mrna_chain) != list:
        raise TypeError('Input mRNA chain must be list of codons')
    if len(mrna_chain) == 0:
        raise ValueError('Input mRNA chain is empty')
    # Check every codon
    for c in range(len(mrna_chain)):
        if type(mrna_chain[c]) != str:
            raise TypeError('Error in codon ' + str(c+1) + ': codon must be '
                            'string, not ' + type(mrna_chain[c]))
        if len(mrna_chain[c]) != 3:
            raise ValueError('Error in codon ' + str(c+1) + ': number of '
                             'nucleotides equal to ' + str(len(mrna_chain[c]))
                             + ', must be 3')
        for n in range(len(mrna_chain[c])):
            if mrna_chain[c][n].upper() not in dna_pattern:
                raise KeyError('Error in codon ' + str(c+1) + ', nucleotide ' +
                               str(n+1) + ': unexpected nucleotide - ' +
                               mrna_chain[c][n])

    # Transcript mRNA chain into DNA
    dna = []
    for c in mrna_chain:
        codon = ''
        for n in c:
            codon += dna_pattern[n.upper()]
        dna.append(codon)
    return dna


def translation(mrna_chain):
    """
    Function of translation (mRNA -> polypeptide chain)

    :parameter mrna_chain: codons with mRNA nucleotides (A, U, C, G)
    :type mrna_chain: list

    :returns list of polypeptide chain

    :raises TypeError: when mrna_chain is not list, codon is not string;
    :raises ValueError: when mrna_chain is empty, number of nucleotides is not
                        equal to 3
    :raises KeyError: when mrna_chain contains not valid nucleotides
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
            raise TypeError('Error in codon ' + str(c+1) + ': codon must be '
                            'string, not ' + type(mrna_chain[c]))
        if len(mrna_chain[c]) != 3:
            raise ValueError('Error in codon ' + str(c+1) + ': number of '
                             'nucleotides equal to ' + str(len(mrna_chain[c]))
                             + ', must be 3')
        for n in range(len(mrna_chain[c])):
            if mrna_chain[c][n].upper() not in mrna_nucleotides:
                raise KeyError('Error in codon ' + str(c+1) + ', nucleotide ' +
                               str(n+1) + ': unexpected nucleotide - ' +
                               mrna_chain[c][n])

    # Translate mRNA to polypeptide chain
    peptide = []
    for codon in mrna_chain:
        peptide.append(peptide_pattern[codon.upper()])
    return peptide
