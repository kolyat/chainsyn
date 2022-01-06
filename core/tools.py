# Copyright (c) 2016-2022 Kirill 'Kolyat' Kiselnikov
# This file is the part of chainsyn, released under modified MIT license
# See the file LICENSE.txt included in this distribution

"""Miscellaneous functions"""


import os
import re
import datetime


class RoutineErr(Exception):
    """Exception class for module's routines (e. g., file I/O)"""
    pass


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
    if chain.rna:
        out.write('>{}-RNA\n'.format(chain.info))
        out.write('{}\n'.format(chain.rna))
        out.write('\n')
    if chain.protein:
        out.write('>{}-protein\n'.format(chain.info))
        out.write('{}\n'.format(chain.protein))
        out.write('\n')
    out.close()
    return True
