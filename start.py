# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of chainsyn

Uses curses library for IO
"""

import curses
from uniprocessing import *


def selection_mode():
    """
    Switch to selection mode (e. g. menu item selection)
    """

    curses.noecho()
    curses.cbreak()
    screen.keypad(True)


def input_mode():
    """
    Switch to input mode (e. g. to write string of nucleotides)
    """

    curses.echo()
    curses.nocbreak()
    screen.keypad(False)


def print_results(*chains):
    """
    Print results of genetic processes

    :param chains: set of DNA/RNA/amino acid chains, their number should be
                   equal to 4 or 5

    :raise TypeError: if chain is not a list
    :raise ValueError: when number of chains is not 4 or 5, if number of items
                       in chains is not equal
    """

    # Necessary checks
    if len(chains) < 4 or len(chains) > 5:
        raise ValueError('Number of arguments must be 4 or 5, '
                         'current - {}'.format(len(chains)))
    for i, c in enumerate(chains, start=0):
        if type(c) != list:
            raise TypeError('Argument {} should be a list, not {}'.format(
                i+1, type(c)))
        if i < len(chains)-1:
            if len(c) != len(chains[i+1]):
                raise ValueError('Number of items in arguments {} and {} '
                                 'are not equal: {} != {}'.format(
                                 i+1, i+2, len(c), len(chains[i+1])))
    screen.addstr('\n')
    # Check of terminal supports colors
    if curses.has_colors():
        curses.start_color()
        # Set up dark gray if possible
        if curses.can_change_color():
            curses.init_color(curses.COLOR_WHITE, 70, 70, 70)
        # Print color legend
        screen.addstr('Amino acids:\n')
        screen.addstr('nonpolar   ', curses.COLOR_YELLOW)
        screen.addstr('polar   ', curses.COLOR_GREEN)
        screen.addstr('basic   ', curses.COLOR_BLUE)
        screen.addstr('acidic   ', curses.COLOR_MAGENTA)
        screen.addstr('(stop codon)\n\n\n', curses.COLOR_WHITE)
        # Init color pattern for amino acids
        color_pattern = {
            'Phe': curses.COLOR_YELLOW,
            'Leu': curses.COLOR_YELLOW,
            'Ser': curses.COLOR_GREEN,
            'Pro': curses.COLOR_YELLOW,
            'His': curses.COLOR_BLUE,
            'Gln': curses.COLOR_GREEN,
            'Tyr': curses.COLOR_GREEN,
            'xxx': curses.COLOR_WHITE,
            'Cys': curses.COLOR_GREEN,
            'Trp': curses.COLOR_YELLOW,
            'Arg': curses.COLOR_BLUE,
            'Ile': curses.COLOR_YELLOW,
            'Met': curses.COLOR_YELLOW,
            'Thr': curses.COLOR_GREEN,
            'Asn': curses.COLOR_GREEN,
            'Lys': curses.COLOR_BLUE,
            'Val': curses.COLOR_YELLOW,
            'Ala': curses.COLOR_YELLOW,
            'Asp': curses.COLOR_MAGENTA,
            'Glu': curses.COLOR_MAGENTA,
            'Gly': curses.COLOR_YELLOW
        }
        # Print items in chains one by one
        for i in range(len(chains[0])):
            for n, c in enumerate(chains, start=0):
                if c[i] in color_pattern:
                    screen.addstr(c[i], color_pattern[c[i]])
                else:
                    screen.addstr(c[i])
                if n == len(chains)-1:
                    screen.addstr("\n")
                else:
                    screen.addstr('-')
    else:
        for i in range(len(chains[0])):
            for n, c in enumerate(chains, start=0):
                screen.addstr(c[i])
                if n == len(chains)-1:
                    screen.addstr("\n")
                else:
                    screen.addstr('-')
    # Print conclusion
    screen.addstr('\n\n')
    screen.addstr('Processed {} codons\n'.format(len(chains[0])))


def main():
    """Main function"""

    menu_items = ('1', '2', '0')
    item = ''

    selection_mode()
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
        input_mode()
        y, x = screen.getyx()
        raw_dna = screen.getstr(y, x)
        # Process input chain
        dna1 = slice_chain(str(raw_dna)[2:-1].upper())
        dna2 = process(dna1, pattern_dna)
        mrna = process(dna2, pattern_mrna)
        polypeptide = translation(mrna)
        # Print results
        print_results(dna1, dna2, mrna, polypeptide)
        screen.addstr('Press any key to exit')
        selection_mode()
        screen.getkey()

    # Imitate full virus cycle
    if item == menu_items[1]:
        screen.addstr('Enter viral mRNA chain with nucleotides A, U, C or G\n')
        screen.addstr('> ')
        input_mode()
        y, x = screen.getyx()
        raw_mrna = screen.getstr(y, x)
        # Process input mRNA
        mrna1 = slice_chain(str(raw_mrna)[2:-1].upper())
        dna1 = process(mrna1, pattern_dna_rev)
        dna2 = process(dna1, pattern_dna)
        mrna2 = process(dna2, pattern_mrna)
        polypeptide = translation(mrna2)
        # Print results
        print_results(mrna1, dna1, dna2, mrna2, polypeptide)
        screen.addstr('Press any key to exit')
        selection_mode()
        screen.getkey()

    # Exit
    if item == menu_items[2]:
        pass

    input_mode()
    curses.endwin()

if __name__ == '__main__':
    screen = curses.initscr()
    main()
