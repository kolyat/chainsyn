# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution
"""
Main module of chainsyn
"""

from os import system

from processing import replication
from processing import transcription
from processing import translation
from processing import rev_transcription

menu_items = ('1', '2', '0')
item = ''

m = True
while m:
    try:
        system('clear')
    except OSError:
        system('cls')
    print()
    print('========')
    print('chainsyn')
    print('========')
    print()
    print()
    print('Main menu')
    print()
    print(menu_items[0], ' - Eucariotic cell polypeptide synthesis')
    print(menu_items[1], ' - Imitate full virus cycle')
    print(menu_items[2], ' - Exit')
    print()
    item = input('Choose menu item: ')
    if item not in menu_items:
        input('Please enter correct number of menu item')
    else:
        m = False

if item == menu_items[0]:
    print()
    print('Enter source DNA chain with nucleotides A, T, C or G')
    dna1 = input()
    dna2 = replication(dna1)
    mrna = transcription(dna2)
    polypeptide = translation(mrna)
    # output
if item == menu_items[1]:
    print()
    print('Enter virus mRNA chain with nucleotides A, U, C or G')
    mrna1 = input()
    dna1 = rev_transcription(mrna1)
    dna2 = replication(dna1)
    mrna2 = transcription(dna2)
    polypeptide = translation(mrna2)
    # output

exit(0)
