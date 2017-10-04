# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
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
dna_to_mrna = {
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
    'Y': 163.06333
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
    'x': ('UAA', 'UGA', 'UAG')
}
