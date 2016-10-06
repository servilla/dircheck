#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: dircheck

:Synopsis:
    Perform system level file object checks in a specific directory.

:Author:
    servilla
  
:Created:
    10/05/16
"""
from __future__ import print_function

import logging

# Setup logging
logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('dircheck')

import os
from os.path import join, getsize
import sys
from hashlib import sha1
import getopt


def sha1sum(file_name):
    hash = sha1()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
            hash.update(chunk)
    return hash.hexdigest()


def main(argv):

    synopsis = '"dircheck" will recursively iterate through a directory ' + \
               'tree and list the name for each file and, if verbosity ' + \
               'is requested, the full path, size, and SHA1 checksum hash ' + \
               'for each file.'

    usage = 'Usage: python ./dircheck.py -h (help) | ' + \
            '[-v verbosity] [-o output_file] <root_directory_path>'

    if len(argv) == 0:
        logger.error(usage)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, 'hvo:')
    except getopt.GetoptError as e:
        logger.error('Unrecognized command line flag: {0}'.format(e))
        logger.error(usage)
        sys.exit(1)

    verbosity = False
    out_file = sys.stdout

    for opt, arg in opts:
        if opt == '-h':
            print(synopsis)
            print(usage)
            sys.exit(0)
        elif opt == '-v':
            verbosity = True
        elif opt == '-o':
            out_file = open(arg, 'w')
        else:
            logger.error(usage)
            sys.exit(1)

    if len(args) == 0:
        logger.error('No root directory path found.')
        logger.error(usage)
        sys.exit(1)

    dir_path = args[0]

    for root, dirs, files in os.walk(dir_path):

        if verbosity:
            for file_name in files:
                file_path = join(root,file_name)
                file_size =  getsize(file_path)
                file_hash = sha1sum(file_path)

                print('{0}, {1}, {2}, {3}'.format(file_name, file_path,
                                                  file_size, file_hash),
                      file = out_file)
                out_file.flush()
        else:
            for file_name in files:
                print('{0}'.format(file_name), file = out_file)
                out_file.flush()


if __name__ == "__main__":
    main(sys.argv[1:])