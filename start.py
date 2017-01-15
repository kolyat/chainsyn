# Copyright (c) 2016 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""
Main module of chainsyn

Uses curses library for user IO
"""

import os
import time
import datetime
import curses
import configparser
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
        raise OSError('stdscr object is not defined')
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

    max_yx = screen.getmaxyx()
    max_y = max_yx[0]
    screen.clear()
    # Check of terminal supports colors
    if curses.has_colors():
        # Set up dark gray if possible
        if curses.can_change_color():
            curses.init_color(curses.COLOR_WHITE, 70, 70, 70)
        # Init color pairs
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Print color legend
        screen.addstr('Amino acids:\n')
        screen.addstr('nonpolar   ', curses.color_pair(1))
        screen.addstr('polar   ', curses.color_pair(2))
        screen.addstr('basic   ', curses.color_pair(3))
        screen.addstr('acidic   ', curses.color_pair(4))
        screen.addstr('(stop codon)\n\n\n', curses.color_pair(5))
        screen.refresh()
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
    y = 0
    for i in range(len(chains[0])):
        for n, c in enumerate(chains, start=0):
            if curses.has_colors() and c[i] in color_pattern:
                screen.addstr(c[i], color_pattern[c[i]])
            else:
                screen.addstr(c[i])
            if n == len(chains)-1:
                screen.addstr('\n')
                screen.refresh()
                time.sleep(0.2)
            else:
                screen.addstr('-')
                screen.refresh()
                time.sleep(0.1)
            yx = screen.getyx()
            y = yx[0]
            if y == max_y-1:
                screen.addstr('Press any key to continue')
                screen.getkey()
                screen.clear()
    if y != 0:
        screen.getkey()

    # Print conclusion
    if y > max_y-4:
        screen.clear()
    screen.addstr('\n\nProcessed {} codon(s)\n'.format(len(chains[0])))
    screen.refresh()


def to_file(exp_dir, *chains):
    """
    Write results to file

    :param exp_dir: directory to export
    :param chains: set of DNA/RNA/amino acid chains, their number should be
                   equal to 4 or 5

    :raise OSError: if cannot create output file
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
                raise ValueError(
                    'Number of items in arguments {} and {} are not equal: '
                    '{} != {}'.format(i+1, i+2, len(c), len(chains[i+1]))
                )

    # Pick current date and time
    current_datetime = datetime.datetime.today()
    now = current_datetime.strftime('%Y%m%d-%H%M%S')
    # Try to open file
    try:
        out = open(os.path.join(exp_dir, 'chains-{}.txt'.format(now)), 'wt')
    except OSError:
        print('Could not open file: {}'.format(
            os.path.join(exp_dir, 'chains-{}.txt'.format(now))))
        return None
    # Write data to file
    for i in range(len(chains[0])):
        for n, c in enumerate(chains, start=0):
            out.write(c[i])
            if n == len(chains)-1:
                out.write('\n')
            else:
                out.write('-')
    # Close file
    out.close()


def is_file(raw_path):
    """
    Check if input data refers to file with data

    :param raw_path: possible path to file
    :type: str

    :return: True if raw_path is file
    :return: False if raw_path is not file
    """

    if os.path.isfile(raw_path):
        return True
    else:
        return False


def from_file(source_file):
    """
    Read data from source file

    :param source_file: path to source file
    :type: str

    :return: str with nucleotides
    """

    # Try to open file
    try:
        f = open(r'{}'.format(source_file), 'r')
    except OSError:
        print('Cannot open file {}'.format(source_file))
        return None

    ignore_sym = (' ', '\n')  # Symbols to be ignored
    raw_data = []
    # Read file byte by byte
    while True:
        s = f.read(1)
        if s:
            if s not in ignore_sym:
                raw_data.append(s)
        else:
            break
    f.close()
    return ''.join(raw_data)


def main(screen):
    """
    Main function

    :param screen: curses stdscr object
    """

    selection_mode(screen)
    screen.clear()

    # Set up settings
    settings = configparser.ConfigParser()
    # Try to read settings file
    s = None
    try:
        s = open('settings.ini', 'r')
        settings.read_file(s)
    except OSError:
        screen.addstr('Cannot read settings.ini - using defaults\n')
        # Set defaults if read error
        settings['EXPORT'] = {
            'Export': 'no',
            'ExportDir': ''
        }
        # Try to create new settings file
        try:
            s = open('settings.ini', 'w')
            settings.write(s)
        except OSError:
            screen.addstr('Cannot write settings.ini with defaults\n')
        screen.addstr('Press any key to continue')
        screen.getkey()
    finally:
        s.close()

    # Show main menu
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
        screen.refresh()
        item = screen.getkey()

    # Eucariotic cell polypeptide synthesis
    if item == menu_items[0]:
        screen.clear()
        screen.addstr('Enter source DNA chain with nucleotides A, T, C or G\n')
        screen.addstr('(or path to source file)\n')
        screen.addstr('> ')
        screen.refresh()
        input_mode(screen)
        y, x = screen.getyx()
        raw_string = screen.getstr(y, x)
        raw_data = str(raw_string)[2:-1]
        if is_file(raw_data):
            raw_dna = from_file(raw_data)
            dna1 = slice_chain(raw_dna.upper())
        else:
            dna1 = slice_chain(raw_data.upper())
        # Process input chain
        dna2 = process(dna1, pattern_dna)
        mrna = process(dna2, pattern_mrna)
        polypeptide = translation(mrna)
        # Print results
        selection_mode(screen)
        print_results(screen, dna1, dna2, mrna, polypeptide)
        # Export to text file
        if settings.has_section('EXPORT') and \
                settings.has_option('EXPORT', 'Export'):
            if settings.getboolean('EXPORT', 'Export'):
                to_file(settings['EXPORT']['ExportDir'],
                        dna1, dna2, mrna, polypeptide)

    # Imitate full virus cycle
    if item == menu_items[1]:
        screen.clear()
        screen.addstr('Enter viral mRNA chain with nucleotides A, U, C or G\n')
        screen.addstr('(or path to source file)\n')
        screen.addstr('> ')
        screen.refresh()
        input_mode(screen)
        y, x = screen.getyx()
        raw_string = screen.getstr(y, x)
        raw_data = str(raw_string)[2:-1]
        if is_file(raw_data):
            raw_mrna = from_file(raw_data)
            mrna1 = slice_chain(raw_mrna.upper())
        else:
            mrna1 = slice_chain(raw_data.upper())
        # Process input mRNA
        dna1 = process(mrna1, pattern_dna_rev)
        dna2 = process(dna1, pattern_dna)
        mrna2 = process(dna2, pattern_mrna)
        polypeptide = translation(mrna2)
        # Print results
        selection_mode(screen)
        print_results(screen, mrna1, dna1, dna2, mrna2, polypeptide)
        # Export to text file
        if settings.has_section('EXPORT') and \
                settings.has_option('EXPORT', 'Export'):
            if settings.getboolean('EXPORT', 'Export'):
                to_file(settings['EXPORT']['ExportDir'],
                        mrna1, dna1, dna2, mrna2, polypeptide)

    # Exit
    if item == menu_items[2]:
        pass

    screen.addstr('Press any key to exit')
    screen.refresh()
    screen.getkey()
    input_mode(screen)
    curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
