#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of ItemList class in the planned plugin DetectiveGame420"""

__all__ = ['Investigate', 'Autopsy']

from detectivegame420.professions.dgprofessionlist import *
from detectivegame420.items.dgitem import InvestigationItem

class Investigate(InvestigationItem):
    def __init__(self):
        super().__init__('Investigate', Detective(), Police())
        self.discription = 'Investigate the body for clues.'
        
class Autopsy(InvestigationItem):
    def __init__(self):
        super().__init__('Autopsy', Doctor(), Student())
        self.discription = 'Performs autopsy on the body for clues.'