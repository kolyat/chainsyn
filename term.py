# Copyright (c) 2016-2023 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Main module of chainsyn"""


import os
import datetime
import curses
import re
import config
from core import processing, tools


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
    if chain.rna:
        screen.addstr('{} - RNA chain\n\n'.format(chain.info))
        for n in chain.rna:
            screen.addstr(n, nucleo_color_pattern[n])
            screen.refresh()
        screen.getkey()
        screen.addstr('\n\n\n')
    if chain.protein:
        screen.addstr('{} - protein chain\n\n'.format(chain.info))
        for n in chain.protein:
            screen.addstr(n, abc_color_pattern[n])
            screen.refresh()
        screen.getkey()
        screen.addstr('\n\n\n')
    # Print stats
    if chain.stats.get('nucleotides'):
        screen.addstr('Number of nucleotides: {}\n'
                      ''.format(chain.stats['nucleotides']))
    if chain.stats.get('codons'):
        screen.addstr('Number of codons: {}\n'.format(chain.stats['codons']))
    if type(chain.stats.get('gc-content')) == float:
        screen.addstr('GC-content: {:f} %\n'.format(chain.stats['gc_content']))
    if chain.stats.get('mass'):
        screen.addstr('Protein\'s mass: {}\n'.format(chain.stats['mass']))
    screen.getkey()


def main(screen):
    """Main function

    :param screen: main window
    """

    def driver(process):
        """Common function which consists of user input, processing, writing to
        file and results printing

        :param process: type of process: replication, transcription,
                        translation

        :return True: on success
        :return False: if fails
        """
        if process not in menu_items.keys():
            raise tools.RoutineErr('Driver call error: unknown process - {}'
                                   ''.format(process))
        # User input
        base = str()
        if process in ('replication', 'transcription'):
            base = 'DNA'
        if process == 'translation':
            base = 'RNA'
        screen.clear()
        screen.addstr('Enter source {} '
                      'or path to source file in FASTA format\n'.format(base))
        screen.addstr('> ')
        screen.refresh()
        input_mode(screen)
        y, x = screen.getyx()
        input_data = screen.getstr(y, x)
        selection_mode(screen)
        screen.addstr('\n')
        input_str = re.sub('\s+', '', input_data.decode())
        source = dict()
        if is_file(input_str):
            try:
                source.update(tools.from_file(input_str))
            except tools.RoutineErr as err:
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
                if process == 'replication':
                    chain.replicate()
                if process == 'transcription':
                    chain.transcribe()
                if process == 'translation':
                    chain.translate()
            except processing.ProcessingErr as err:
                screen.addstr('{}\n'.format(str(err)))
                screen.getkey()
            finally:
                chain.collect_stats()
                chains.append(chain)
        # Export to text file
        if config.EXPORT_ENABLED:
            for chain in chains:
                try:
                    tools.to_file(config.EXPORT_DIR, chain)
                except tools.RoutineErr as err:
                    screen.addstr('{}\n'.format(str(err)))
                    screen.getkey()
        # Print results
        for chain in chains:
            print_results(screen, chain)

    # Init colors if supported
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
    nucleo_color_pattern.update({
        'A': curses.color_pair(6),
        'T': curses.color_pair(4),
        'U': curses.color_pair(1),
        'C': curses.color_pair(2),
        'G': curses.color_pair(3)
    })
    # Init color pattern for amino acids
    abc_color_pattern.update({
        'F': curses.color_pair(1),
        'L': curses.color_pair(1),
        'S': curses.color_pair(2),
        'P': curses.color_pair(1),
        'H': curses.color_pair(3),
        'Q': curses.color_pair(2),
        'Y': curses.color_pair(2),
        '*': curses.color_pair(5),
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
    })
    # Init main window
    screen.scrollok(True)
    selection_mode(screen)
    screen.clear()

    # Main cycle
    menu_items = {
        'replication': '1',
        'transcription': '2',
        'translation': '3',
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
        screen.addstr('{} - Transcription (DNA -> RNA)\n'
                      ''.format(menu_items['transcription']))
        screen.addstr('{} - Translation (RNA -> protein)\n'
                      ''.format(menu_items['translation']))
        screen.addstr('{} - Exit\n'.format(menu_items['exit']))
        screen.addstr('\n')
        screen.refresh()
        item = screen.getkey()
        if item == menu_items['replication']:
            driver('replication')
        if item == menu_items['transcription']:
            driver('transcription')
        if item == menu_items['translation']:
            driver('translation')
        if item == menu_items['exit']:
            break
    input_mode(screen)
    curses.endwin()


if __name__ == '__main__':
    nucleo_color_pattern, abc_color_pattern = dict(), dict()
    curses.wrapper(main)
