# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of chainsyn

Uses curses library for IO
"""

import curses
from uniprocessing import *


def selection_mode(screen):
    """
    Switch to selection mode (e. g. menu item selection)

    :param screen: curses stdscr object

    :raise OSError: when curses stdscr object is not defined
    """

    if not screen:
        raise OSError('Stdscr object is not defined')
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)


def input_mode(screen):
    """
    Switch to input mode (e. g. to write string of nucleotides)

    :param screen: curses stdscr object

    :raise OSError: when curses stdscr object is not defined
    """

    if not screen:
        raise OSError('Stdscr object is not defined')
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)


def print_results(screen, *chains):
    """
    Print results of genetic processes

    :param screen: curses stdscr object
    :param chains: set of DNA/RNA/amino acid chains, their number should be
                   equal to 4 or 5

    :raise OSError: when curses stdscr object is not defined
    :raise TypeError: if chain is not a list
    :raise ValueError: when number of chains is not 4 or 5, if number of items
                       in chains is not equal
    """

    # Necessary checks
    if not screen:
        raise OSError('Stdscr object is not defined')
    if len(chains) < 4 or len(chains) > 5:
        raise ValueError('Number of arguments must be 4 or 5, '
                         'current - {}'.format(len(chains)))
    for i, c in enumerate(chains, start=0):
        if type(c) != list:
            raise TypeError('Argument {} should be a list, not {}'.format(
                i+1, type(c)))
        if i < len(chains)-1:
            if len(c) != len(chains[i+1]):
                raise ValueError(
                    'Number of items in arguments {} and {} are not equal: '
                    '{} != {}'.format(i+1, i+2, len(c), len(chains[i+1]))
                )
    screen.addstr('\n')
    # Check of terminal supports colors
    if curses.has_colors():
        # Set up dark gray if possible
        if curses.can_change_color():
            curses.init_color(curses.COLOR_WHITE, 70, 70, 70)
        # Init color pairs
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Print color legend
        screen.addstr('Amino acids:\n')
        screen.addstr('nonpolar   ', curses.color_pair(1))
        screen.addstr('polar   ', curses.color_pair(2))
        screen.addstr('basic   ', curses.color_pair(3))
        screen.addstr('acidic   ', curses.color_pair(4))
        screen.addstr('(stop codon)\n\n\n', curses.color_pair(5))
        # Init color pattern for amino acids
        color_pattern = {
            'Phe': curses.color_pair(1),
            'Leu': curses.color_pair(1),
            'Ser': curses.color_pair(2),
            'Pro': curses.color_pair(1),
            'His': curses.color_pair(3),
            'Gln': curses.color_pair(2),
            'Tyr': curses.color_pair(2),
            'xxx': curses.color_pair(5),
            'Cys': curses.color_pair(2),
            'Trp': curses.color_pair(1),
            'Arg': curses.color_pair(3),
            'Ile': curses.color_pair(1),
            'Met': curses.color_pair(1),
            'Thr': curses.color_pair(2),
            'Asn': curses.color_pair(2),
            'Lys': curses.color_pair(3),
            'Val': curses.color_pair(1),
            'Ala': curses.color_pair(1),
            'Asp': curses.color_pair(4),
            'Glu': curses.color_pair(4),
            'Gly': curses.color_pair(1)
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
    screen.addstr("\n\nProcessed {} codons\n".format(len(chains[0])))


def main(screen):
    """
    Main function

    :param screen: curses stdscr object
    """

    menu_items = ('1', '2', '0')
    item = ''

    selection_mode(screen)
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
        input_mode(screen)
        y, x = screen.getyx()
        raw_dna = screen.getstr(y, x)
        # Process input chain
        dna1 = slice_chain(str(raw_dna)[2:-1].upper())
        dna2 = process(dna1, pattern_dna)
        mrna = process(dna2, pattern_mrna)
        polypeptide = translation(mrna)
        # Print results
        print_results(screen, dna1, dna2, mrna, polypeptide)

    # Imitate full virus cycle
    if item == menu_items[1]:
        screen.addstr('Enter viral mRNA chain with nucleotides A, U, C or G\n')
        screen.addstr('> ')
        input_mode(screen)
        y, x = screen.getyx()
        raw_mrna = screen.getstr(y, x)
        # Process input mRNA
        mrna1 = slice_chain(str(raw_mrna)[2:-1].upper())
        dna1 = process(mrna1, pattern_dna_rev)
        dna2 = process(dna1, pattern_dna)
        mrna2 = process(dna2, pattern_mrna)
        polypeptide = translation(mrna2)
        # Print results
        print_results(screen, mrna1, dna1, dna2, mrna2, polypeptide)

    # Exit
    if item == menu_items[2]:
        pass

    screen.addstr('Press any key to exit')
    selection_mode(screen)
    screen.getkey()
    input_mode(screen)
    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
