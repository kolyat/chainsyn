# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
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


class RoutineErr(Exception):
    """Exception class for module's routines (e. g. file IO)"""
    pass


def to_file(exp_dir, *chains):
    """
    Write results to file

    :param exp_dir: directory to export
    :param chains: set of DNA/RNA/amino acid chains, their number should be
                   equal to 4 or 5

    :raise RoutineErr:
      - if cannot create output file
      - chain is not list
      - number of chains is not 4 or 5
      - number of chain's items is not equal to each other
    """

    # Necessary checks
    if len(chains) < 4 or len(chains) > 5:
        raise RoutineErr('{}: number of arguments must be 4 or 5, '
                         'got {}'.format(to_file.__name__, len(chains)))
    for i, c in enumerate(chains, start=0):
        if type(c) != list:
            raise RoutineErr('{}: argument {} should be a list, not {}'.format(
                to_file.__name__, i+1, type(c)))
        if i < len(chains)-1:
            if len(c) != len(chains[i+1]):
                raise RoutineErr(
                    '{}: number of items in arguments {} and {} '
                    'are not equal: {} != {}'.format(
                        to_file.__name__, i+1, i+2, len(c), len(chains[i+1]))
                )

    # Pick current date and time
    current_datetime = datetime.datetime.today()
    now = current_datetime.strftime('%Y%m%d-%H%M%S')
    # Try to open file
    try:
        out = open(os.path.join(exp_dir, 'chains-{}.txt'.format(now)), 'wt')
    except OSError:
        raise RoutineErr('{}: could not open file: {}'.format(to_file.__name__,
                         os.path.join(exp_dir, 'chains-{}.txt'.format(now))))
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
    :raise RoutineErr if cannot open source file
    """

    # Try to open file
    try:
        f = open(r'{}'.format(source_file), 'r')
    except OSError:
        raise RoutineErr('{}: cannot open file {}'.format(from_file.__name__,
                                                          source_file))

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

    :param screen: main window
    """

    def selection_mode():
        """Switch to selection mode (e. g. menu item selection)"""
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

    def input_mode():
        """Switch to input mode (e. g. to write string of nucleotides)"""
        curses.echo()
        curses.nocbreak()
        screen.keypad(False)

    def print_results(*chains):
        """
        Print results of genetic processes

        :param chains: set of DNA/RNA/amino acid chains, their number should be
                       equal to 4 or 5

        :raise RoutineErr:
          - chain is not a list
          - number of chains is not 4 or 5
          - number of items in chains is not equal
        """

        # Necessary checks
        if len(chains) < 4 or len(chains) > 5:
            raise RoutineErr('{}: number of arguments must be 4 or 5, '
                             'got {}'.format(print_results.__name__,
                                             len(chains)))
        for i, c in enumerate(chains, start=0):
            if type(c) != list:
                raise RoutineErr('{}: argument {} should be a list, '
                                 'not {}'.format(print_results.__name__,
                                                 i + 1, type(c)))
            if not c:
                raise RoutineErr(
                    '{}: chain {} is empty'.format(print_results.__name__, i+1)
                )
            if i < len(chains) - 1:
                if len(c) != len(chains[i + 1]):
                    raise RoutineErr(
                        '{}: number of items in arguments {} and {} '
                        'are not equal: {} != {}'.format(
                            print_results.__name__, i + 1, i + 2,
                            len(c), len(chains[i + 1]))
                    )

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
        for i in range(len(chains[0])):
            for n, c in enumerate(chains, start=0):
                if curses.has_colors() and c[i] in color_pattern:
                    screen.addstr(c[i], color_pattern[c[i]])
                else:
                    screen.addstr(c[i])
                if n == len(chains) - 1:
                    screen.addstr('\n')
                    screen.refresh()
                    time.sleep(0.2)
                else:
                    screen.addstr('-')
                    screen.refresh()
                    time.sleep(0.1)

        # Print conclusion
        screen.addstr('\n')
        screen.addstr('Processed {} codon(s)\n'.format(len(chains[0])))

    # Init main window
    screen.scrollok(True)
    selection_mode()
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
    screen.clear()

    # Eucariotic cell polypeptide synthesis
    if item == menu_items[0]:
        screen.addstr('Enter source DNA chain with nucleotides A, T, C or G\n')
        screen.addstr('(or path to source file)\n')
        screen.addstr('> ')
        screen.refresh()
        input_mode()
        y, x = screen.getyx()
        raw_string = screen.getstr(y, x)
        screen.addstr('\n')
        raw_data = str(raw_string)[2:-1]
        dna1 = list()
        dna2 = list()
        mrna = list()
        polypeptide = list()
        if is_file(raw_data):
            raw_dna = ''
            try:
                raw_dna = from_file(raw_data)
            except RoutineErr as err:
                screen.addstr('{}\n'.format(str(err)))
            try:
                dna1 = slice_chain(raw_dna.upper())
            except ProcessErr as err:
                screen.addstr('{}\n'.format(str(err)))
        else:
            try:
                dna1 = slice_chain(raw_data.upper())
            except ProcessErr as err:
                screen.addstr('{}\n'.format(str(err)))
        # Process input chain
        try:
            dna2 = process(dna1, pattern_dna)
            mrna = process(dna2, pattern_mrna)
            polypeptide = translation(mrna)
        except ProcessErr as err:
            screen.addstr('{}\n'.format(str(err)))
        # Print results
        selection_mode()
        try:
            print_results(dna1, dna2, mrna, polypeptide)
        except RoutineErr as err:
            screen.addstr('{}\n'.format(str(err)))
        # Export to text file
        if settings.has_section('EXPORT') and \
                settings.has_option('EXPORT', 'Export'):
            if settings.getboolean('EXPORT', 'Export'):
                try:
                    to_file(settings['EXPORT']['ExportDir'],
                            dna1, dna2, mrna, polypeptide)
                except RoutineErr as err:
                    screen.addstr('{}\n'.format(str(err)))

    # Imitate full virus cycle
    if item == menu_items[1]:
        screen.addstr('Enter viral mRNA chain with nucleotides A, U, C or G\n')
        screen.addstr('(or path to source file)\n')
        screen.addstr('> ')
        screen.refresh()
        input_mode()
        y, x = screen.getyx()
        raw_string = screen.getstr(y, x)
        screen.addstr('\n')
        raw_data = str(raw_string)[2:-1]
        mrna1 = list()
        dna1 = list()
        dna2 = list()
        mrna2 = list()
        polypeptide = list()
        if is_file(raw_data):
            raw_mrna = ''
            try:
                raw_mrna = from_file(raw_data)
            except RoutineErr as err:
                screen.addstr('{}\n'.format(str(err)))
            try:
                mrna1 = slice_chain(raw_mrna.upper())
            except ProcessErr as err:
                screen.addstr('{}\n'.format(str(err)))
        else:
            try:
                mrna1 = slice_chain(raw_data.upper())
            except ProcessErr as err:
                screen.addstr('{}\n'.format(str(err)))
        # Process input mRNA
        try:
            dna1 = process(mrna1, pattern_dna_rev)
            dna2 = process(dna1, pattern_dna)
            mrna2 = process(dna2, pattern_mrna)
            polypeptide = translation(mrna2)
        except ProcessErr as err:
            screen.addstr('{}\n'.format(str(err)))
        # Print results
        selection_mode()
        try:
            print_results(mrna1, dna1, dna2, mrna2, polypeptide)
        except RoutineErr as err:
            screen.addstr('{}\n'.format(str(err)))
        # Export to text file
        if settings.has_section('EXPORT') and \
                settings.has_option('EXPORT', 'Export'):
            if settings.getboolean('EXPORT', 'Export'):
                try:
                    to_file(settings['EXPORT']['ExportDir'],
                            mrna1, dna1, dna2, mrna2, polypeptide)
                except RoutineErr as err:
                    screen.addstr('{}\n'.format(str(err)))

    # Exit
    if item == menu_items[2]:
        pass

    screen.addstr('Press any key to exit')
    screen.refresh()
    screen.getkey()
    input_mode()
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
