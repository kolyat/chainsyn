# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of chainsyn

Uses native Python IO
"""

import sys
from os import system

from processing import slice_chain
from processing import replication
from processing import transcription
from processing import translation
from processing import rev_transcription


def clrscr():
    """Clear screen"""
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        system('clear')
    if sys.platform.startswith('win'):
        system('cls')

menu_items = ('1', '2', '0')
item = ''

while item not in menu_items:
    clrscr()
    print()
    print('========')
    print('chainsyn')
    print('========')
    print()
    print()
    print('Main menu')
    print()
    print(menu_items[0], '- Eucariotic cell polypeptide synthesis')
    print(menu_items[1], '- Imitate full viral cycle')
    print(menu_items[2], '- Exit')
    print()
    item = input('Choose menu item: ',)
    if item not in menu_items:
        input('Please, enter correct number of menu item')

# Eucariotic cell polypeptide synthesis
if item == menu_items[0]:
    print()
    print('Enter source DNA chain with nucleotides A, T, C or G')
    raw_dna = input('> ')
    # Process input chain
    dna1 = slice_chain(raw_dna)
    dna2 = replication(dna1)
    mrna = transcription(dna2)
    polypeptide = translation(mrna)
    # Print results
    for i in range(len(dna1)):
        seq = (dna1[i].upper(), dna2[i], mrna[i], polypeptide[i])
        print('-'.join(seq))
    print()
    print('Processed ' + str(len(dna1)) + ' codons')
    print('Press <Enter> to exit',)
    input()

# Imitate full virus cycle
if item == menu_items[1]:
    print()
    print('Enter viral mRNA chain with nucleotides A, U, C or G')
    raw_mrna = input('> ')
    # Process input mRNA
    mrna1 = slice_chain(raw_mrna)
    dna1 = rev_transcription(mrna1)
    dna2 = replication(dna1)
    mrna2 = transcription(dna2)
    polypeptide = translation(mrna2)
    # Print results
    for i in range(len(mrna1)):
        seq = (mrna1[i].upper(), dna1[i], dna2[i], mrna2[i], polypeptide[i])
        print('-'.join(seq))
    print()
    print('Processed ' + str(len(mrna1)) + ' codons')
    print('Press <Enter> to exit',)
    input()

# Exit
if item == menu_items[2]:
    exit(0)
