# Copyright (c) 2016-2020 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Module with various processing patterns"""


# DNA patterns
dna = 'ATCG'
dna_to_dna = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}
dna_to_rna = {
    'A': 'U',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}

# RNA patterns
rna = 'AUCG'
rna_to_dna = {
    'A': 'T',
    'U': 'A',
    'C': 'G',
    'G': 'C'
}
rna_to_abc = {
    # Phenylalanine
    'UUU': 'F',
    'UUC': 'F',
    # Leucine
    'UUA': 'L',
    'UUG': 'L',
    'CUU': 'L',
    'CUC': 'L',
    'CUA': 'L',
    'CUG': 'L',
    # Serine
    'UCU': 'S',
    'UCC': 'S',
    'UCA': 'S',
    'UCG': 'S',
    'AGU': 'S',
    'AGC': 'S',
    # Proline
    'CCU': 'P',
    'CCC': 'P',
    'CCA': 'P',
    'CCG': 'P',
    # Histidine
    'CAU': 'H',
    'CAC': 'H',
    # Glutamine
    'CAA': 'Q',
    'CAG': 'Q',
    # Tyrosine
    'UAU': 'Y',
    'UAC': 'Y',
    # Stop codons
    'UAA': '*',
    'UAG': '*',
    'UGA': '*',
    # Cysteine
    'UGU': 'C',
    'UGC': 'C',
    # Tryptophan
    'UGG': 'W',
    # Arginine
    'CGU': 'R',
    'CGC': 'R',
    'CGA': 'R',
    'CGG': 'R',
    'AGA': 'R',
    'AGG': 'R',
    # Isoleucine
    'AUU': 'I',
    'AUC': 'I',
    'AUA': 'I',
    # Methionine
    'AUG': 'M',
    # Threonine
    'ACU': 'T',
    'ACC': 'T',
    'ACA': 'T',
    'ACG': 'T',
    # Asparagine
    'AAU': 'N',
    'AAC': 'N',
    # Lysine
    'AAA': 'K',
    'AAG': 'K',
    # Valine
    'GUU': 'V',
    'GUC': 'V',
    'GUA': 'V',
    'GUG': 'V',
    # Alanine
    'GCU': 'A',
    'GCC': 'A',
    'GCA': 'A',
    'GCG': 'A',
    # Aspartate
    'GAU': 'D',
    'GAC': 'D',
    # Glutamate
    'GAA': 'E',
    'GAG': 'E',
    # Glycine
    'GGU': 'G',
    'GGC': 'G',
    'GGA': 'G',
    'GGG': 'G'
}

# ABC patterns (ABC is amino acid 'alphabet')
abc = 'ARNDCQEGHILKMFPSTWYV'
abc_mass = {
    'A': 71.03711,
    'C': 103.00919,
    'D': 115.02694,
    'E': 129.04259,
    'F': 147.06841,
    'G': 57.02146,
    'H': 137.05891,
    'I': 113.08406,
    'K': 128.09496,
    'L': 113.08406,
    'M': 131.04049,
    'N': 114.04293,
    'P': 97.05276,
    'Q': 128.05858,
    'R': 156.10111,
    'S': 87.03203,
    'T': 101.04768,
    'V': 99.06841,
    'W': 186.07931,
    'Y': 163.06333,
    '*': 0
}
abc_to_rna = {
    'A': ('GCU', 'GCC', 'GCA', 'GCG'),
    'R': ('CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'),
    'N': ('AAU', 'AAC'),
    'D': ('GAU', 'GAC'),
    'C': ('UGU', 'UGC'),
    'Q': ('CAA', 'CAG'),
    'E': ('GAA', 'GAG'),
    'G': ('GGU', 'GGC', 'GGA', 'GGG'),
    'H': ('CAU', 'CAC'),
    'I': ('AUU', 'AUC', 'AUA'),
    'L': ('UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'),
    'K': ('AAA', 'AAG'),
    'M': ('AUG',),
    'F': ('UUU', 'UUC'),
    'P': ('CCU', 'CCC', 'CCA', 'CCG'),
    'S': ('UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'),
    'T': ('ACU', 'ACC', 'ACA', 'ACG'),
    'W': ('UGG',),
    'Y': ('UAU', 'UAC'),
    'V': ('GUU', 'GUC', 'GUA', 'GUG'),
    '*': ('UAA', 'UGA', 'UAG')
}
