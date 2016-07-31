# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution
"""
Main module of chainsyn
"""

import sys
from os import system

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

m = True
while m:
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
    print(menu_items[1], '- Imitate full virus cycle')
    print(menu_items[2], '- Exit')
    print()
    item = input('Choose menu item: ',)
    if item not in menu_items:
        input('Please enter correct number of menu item')
    else:
        m = False

# Eucariotic cell polypeptide synthesis
if item == menu_items[0]:
    print()
    print('Enter source DNA chain with nucleotides A, T, C or G')
    dna1 = input('> ')
    dna2 = replication(dna1)
    mrna = transcription(dna2)
    polypeptide = translation(mrna)
    # Print results (this block needs refactoring)
    for i in range(len(dna1)):
        print(dna1[i].upper(), dna2[i], mrna[i], sep=' - ', end='')
        p, b = divmod(i+1, 3)
        if b == 0:
            print(' -', polypeptide[p-1], end='')
        print()
# Imitate full virus cycle
if item == menu_items[1]:
    print()
    print('Enter virus mRNA chain with nucleotides A, U, C or G')
    mrna1 = input('> ')
    dna1 = rev_transcription(mrna1)
    dna2 = replication(dna1)
    mrna2 = transcription(dna2)
    polypeptide = translation(mrna2)
    # Print results (this block needs refactoring)
    for i in range(len(mrna1)):
        print(mrna1[i].upper(), dna1[i], dna2[i], mrna2[i], sep=' - ', end='')
        p, b = divmod(i+1, 3)
        if b == 0:
            print(' -', polypeptide[p-1], end='')
        print()
# Exit
if item == menu_items[2]:
    exit(0)
