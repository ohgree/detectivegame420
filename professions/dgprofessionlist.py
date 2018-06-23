#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of all professions in the planned plugin DetectiveGame420"""

__all__ = [
    'Doctor', 'Student', 'Detective', 'Police',
    'Engineer', 'Clerk', 'Chef', 'Serviceman',
    'DeltaForce', 'Unemployed',
]

from detectivegame420.professions.dgprofession import DGProfession

class Doctor(DGProfession):
    def __init__(self):
        super().__init__('Doctor', True)
        self.discription = \
        'You are an experienced doctor who\n'\
        'went on a vacation to remedy his trauma\n'\
        'from his recent medical malpractice'
        # change this to class object
        self.add_usable_items(['Autopsy', 'Luminol Solution'])
        
class Student(DGProfession):
    def __init__(self):
        super().__init__('Student', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['Autopsy'])
        
class Detective(DGProfession):
    def __init__(self):
        super().__init__('Detective', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['Investigate'])
        
class Police(DGProfession):
    def __init__(self):
        super().__init__('Police', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['Investigate', 'Body Check'])
        
class Engineer(DGProfession):
    def __init__(self):
        super().__init__('Engineer', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['CCTV', 'Ice'])
        
class Clerk(DGProfession):
    def __init__(self):
        super().__init__('Clerk', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['Googling'])
        
class Chef(DGProfession):
    def __init__(self):
        super().__init__('Chef', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.'
        self.add_usable_items(['Chef\'s Kitchen Knife'])
        
class Serviceman(DGProfession):
    def __init__(self):
        super().__init__('Serviceman', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.\n'\
        'Kills the killer if he trys to kill you.'
        self.add_usable_items([])
        
class DeltaForce(DGProfession):
    def __init__(self):
        super().__init__('DeltaForce', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.\n'\
        'Kills the killer if he trys to kill you.\n'\
        'You appear to be unemployed in Internet.'
        self.add_usable_items([])
        
class Unemployed(DGProfession):
    def __init__(self):
        super().__init__('Unemployed', True)
        self.discription = \
        'Interesting discription with character\'s\n'\
        'dark sides revealed.\n'\
        'Gets bonus points for every score gained.'
        self.add_usable_items(['Body Check'])

# Self-test code
def _test():
    p = Unemployed()
    print(p.info)
    
if __name__ == '__main__':
    _test()