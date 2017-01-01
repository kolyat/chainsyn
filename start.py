# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of chainsyn

Uses curses library for IO
"""

import curses
from uniprocessing import *
from processing import slice_chain
from processing import translation


def main():
    # Init section
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    menu_items = ('1', '2', '0')
    item = ''

    while item not in menu_items:
        screen.clear()
        screen.addstr('\n')
        screen.addstr('========\n')
        screen.addstr('chainsyn\n')
        screen.addstr('========\n')
        screen.addstr('\n\n')
        screen.addstr('Main menu\n')
        screen.addstr('\n')
        screen.addstr(
            '{} - Eucariotic cell '
            'polypeptide synthesis\n'.format(menu_items[0]))
        screen.addstr('{} - Imitate full viral cycle\n'.format(menu_items[1]))
        screen.addstr('{} - Exit\n'.format(menu_items[2]))
        screen.addstr('\n')
        item = screen.getkey()

    # Eucariotic cell polypeptide synthesis
    if item == menu_items[0]:
        screen.addstr('Enter source DNA chain with nucleotides A, T, C or G\n')
        screen.addstr('> ')
        curses.echo()
        curses.nocbreak()
        screen.keypad(False)
        y, x = screen.getyx()
        raw_dna = screen.getstr(y, x)
        # Process input chain
        dna1 = slice_chain(str(raw_dna)[2:-1])
        dna2 = process(dna1, pattern_dna)
        mrna = process(dna2, pattern_mrna)
        polypeptide = translation(mrna)
        # Print results
        screen.addstr('\n')
        for i in range(len(dna1)):
            seq = (dna1[i].upper(), dna2[i], mrna[i], polypeptide[i])
            screen.addstr('-'.join(seq) + '\n')
        screen.addstr('\n')
        screen.addstr('Processed {} codons\n'.format(len(dna1)))
        screen.addstr('Press any key to exit')
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        screen.getkey()

    # Imitate full virus cycle
    if item == menu_items[1]:
        screen.addstr('Enter viral mRNA chain with nucleotides A, U, C or G\n')
        screen.addstr('> ')
        curses.echo()
        curses.nocbreak()
        screen.keypad(False)
        y, x = screen.getyx()
        raw_mrna = screen.getstr(y, x)
        # Process input mRNA
        mrna1 = slice_chain(str(raw_mrna)[2:-1])
        dna1 = process(mrna1, pattern_dna_rev)
        dna2 = process(dna1, pattern_dna)
        mrna2 = process(dna2, pattern_mrna)
        polypeptide = translation(mrna2)
        # Print results
        for i in range(len(mrna1)):
            seq = (
                mrna1[i].upper(), dna1[i], dna2[i], mrna2[i], polypeptide[i])
            screen.addstr('-'.join(seq) + '\n')
        screen.addstr('\n')
        screen.addstr('Processed {} codons\n'.format(len(mrna1)))
        screen.addstr('Press <Enter> to exit')
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        screen.getkey()

    # Exit
    if item == menu_items[2]:
        pass

    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':
    main()
