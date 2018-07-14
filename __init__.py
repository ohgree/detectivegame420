# -*- coding: utf-8 -*-
"""Package for demonstrating a planned bukkit plugin DetectiveGame420."""
__name__ = 'DetectiveGame420'

__version__ = 'Pre-Alpha'

__all__ = ['detectivegame']

__date__ = '25 May 2018'
__author__ = 'Minjun Shin <ohgree@u.sogang.ac.kr>'
__status__ = 'Prototype'

from detectivegame420.detectivegame import main

def test():
    import sys

    try:
        testfile = open('./input.txt', 'r')
        sys.stdin = testfile
    except IOError:
        pass
    return main()
