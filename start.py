# Copyright (c) 2016-2017 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Main module of chainsyn"""


import os
import datetime
import curses
import configparser
import re
import processing


class RoutineErr(Exception):
    """Exception class for module's routines (e. g., file I/O)"""
    pass


def is_file(raw_path):
    """Check if input data is a file name

    :param raw_path: possible path to file

    :return: True if raw_path is file
    :return: False if raw_path is not file
    """
    if os.path.isfile(os.path.normpath(raw_path)):
        return True
    else:
        return False


def from_file(source_file):
    """Read data from source file in FASTA format

    :param source_file: path to source file

    :return: dict with description(s) and stored chain(s)
    :raise RoutineErr if could not open source file
    """
    # Try to open file
    try:
        with open(os.path.normpath(source_file), 'rt') as f:
            raw = f.read()
            f.close()
    except OSError:
        raise RoutineErr('Could not open file: {}'.format(source_file))
    # Parse file
    data = dict()
    pat = re.compile('>(\S+)\s([A-Z\s]+)')
    for it in pat.finditer(raw):
        data.update({it.group(1): re.sub('\s+', '', it.group(2))})
    return data


def to_file(exp_dir, chain):
    """Write results to file

    :param exp_dir: directory to export
    :param chain: Chain object

    :raise RoutineErr: on file I/O error

    :return True: on success
    """
    now = datetime.datetime.today().strftime('%Y%m%d-%H%M%S-%f')
    file_name = os.path.join(exp_dir, 'chains-{}.txt'.format(now))
    try:
        out = open(file_name, 'wt')
    except OSError:
        raise RoutineErr('Could not open file: {}'.format(file_name))
    if chain.dna1:
        out.write('>{}-DNA1\n'.format(chain.info))
        out.write('{}\n'.format(chain.dna1))
        out.write('\n')
    if chain.dna2:
        out.write('>{}-DNA2\n'.format(chain.info))
        out.write('{}\n'.format(chain.dna2))
        out.write('\n')
    out.close()
    return True


def generate_chain_info():
    """Generate info for manually entered chain"""

    return 'chainsyn-{}'.format(
        datetime.datetime.today().strftime('%Y%m%d-%H%M%S'))


def selection_mode(screen):
    """Switch to selection mode

    :param screen: main window
    """
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)


def input_mode(screen):
    """Switch to input mode

    :param screen: main window
    """
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)


def print_results(screen, chain):
    """Print results of processing

    :param chain: Chain object
    :param screen: main window
    """
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
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    else:
        for i in (1, 2, 3, 4, 5, 6):
            curses.init_pair(i, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Init color for nucleotides
    nucleo_color_pattern = {
        'A': curses.color_pair(6),
        'T': curses.color_pair(4),
        'U': curses.color_pair(1),
        'C': curses.color_pair(2),
        'G': curses.color_pair(3)
    }
    # Init color pattern for amino acids
    abc_color_pattern = {
        'F': curses.color_pair(1),
        'L': curses.color_pair(1),
        'S': curses.color_pair(2),
        'P': curses.color_pair(1),
        'H': curses.color_pair(3),
        'Q': curses.color_pair(2),
        'Y': curses.color_pair(2),
        '.': curses.color_pair(5),
        'C': curses.color_pair(2),
        'W': curses.color_pair(1),
        'R': curses.color_pair(3),
        'I': curses.color_pair(1),
        'M': curses.color_pair(1),
        'T': curses.color_pair(2),
        'N': curses.color_pair(2),
        'K': curses.color_pair(3),
        'V': curses.color_pair(1),
        'A': curses.color_pair(1),
        'D': curses.color_pair(4),
        'E': curses.color_pair(4),
        'G': curses.color_pair(1)
    }
    # Print results
    if chain.dna1:
        screen.addstr('{} - first DNA chain\n\n'.format(chain.info))
        for n in chain.dna1:
            screen.addstr(n, nucleo_color_pattern[n])
            screen.refresh()
        screen.getkey()
        screen.addstr('\n\n\n')
    if chain.dna2:
        screen.addstr('{} - second DNA chain\n\n'.format(chain.info))
        for n in chain.dna2:
            screen.addstr(n, nucleo_color_pattern[n])
            screen.refresh()
        screen.getkey()
        screen.addstr('\n\n\n')


def main(screen):
    """Main function

    :param screen: main window
    """

    def replication():
        """Replication menu item

        :return True: on success
        :return False: if fails
        """
        screen.clear()
        screen.addstr('Enter source DNA '
                      'or path to source file in FASTA format\n')
        screen.addstr('> ')
        screen.refresh()
        input_mode(screen)
        y, x = screen.getyx()
        input_data = screen.getstr(y, x)
        selection_mode(screen)
        screen.addstr('\n')
        input_str = input_data.decode()
        source = dict()
        if is_file(input_str):
            try:
                source.update(from_file(input_str))
            except RoutineErr as err:
                screen.addstr('{}\n'.format(str(err)))
                screen.getkey()
                return False
        else:
            source.update({generate_chain_info(): input_str.upper()})
        # Process source data
        chains = list()
        for s in source:
            chain = processing.Chain(s, source[s])
            try:
                chain.replicate()
            except processing.ProcessingErr as err:
                screen.addstr('{}\n'.format(str(err)))
                screen.getkey()
            finally:
                chains.append(chain)
        # Export to text file
        if settings.has_section('EXPORT') \
                and settings.has_option('EXPORT', 'Export') \
                and settings.getboolean('EXPORT', 'Export'):
            for chain in chains:
                try:
                    to_file(settings['EXPORT']['ExportDir'], chain)
                except RoutineErr as err:
                    screen.addstr('{}\n'.format(str(err)))
                    screen.getkey()
        # Print results
        for chain in chains:
            print_results(screen, chain)

    # Init main window
    screen.scrollok(True)
    selection_mode(screen)
    screen.clear()

    # Set up settings
    settings = configparser.ConfigParser()
    # Try to read settings file
    st = None
    try:
        st = open('settings.ini', 'rt')
        settings.read_file(st)
    except OSError:
        screen.addstr('Cannot read settings.ini - using defaults\n')
        # Set defaults if read error
        settings['EXPORT'] = {
            'Export': 'no',
            'ExportDir': ''
        }
        # Try to create new settings file
        try:
            st = open('settings.ini', 'wt')
            settings.write(st)
        except OSError:
            screen.addstr('Cannot write settings.ini with defaults\n')
        screen.addstr('Press any key to continue')
        screen.getkey()
    finally:
        if st:
            st.close()

    # Main cycle
    menu_items = {
        'replication': '1',
        'exit': '0'
    }
    while True:
        screen.clear()
        screen.addstr('\n')
        screen.addstr('========\n')
        screen.addstr('chainsyn\n')
        screen.addstr('========\n')
        screen.addstr('\n\n')
        screen.addstr('Main menu\n')
        screen.addstr('\n')
        screen.addstr('{} - Replication (DNA -> DNA)\n'
                      ''.format(menu_items['replication']))
        # screen.addstr('{} - Eucariotic cell polypeptide synthesis\n'.format(menu_items[0]))
        # screen.addstr('{} - Imitate full viral cycle\n'.format(menu_items[1]))
        screen.addstr('{} - Exit\n'.format(menu_items['exit']))
        screen.addstr('\n')
        screen.refresh()
        item = screen.getkey()
        if item == menu_items['replication']:
            replication()
        if item == menu_items['exit']:
            break
    input_mode(screen)
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
