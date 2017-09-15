import sys


def print_and_exit(message):
    sys.stderr.write(message+'\n')
    exit(1)
