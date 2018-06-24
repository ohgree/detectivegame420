#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of DGProfession class in the planned plugin DetectiveGame420"""

__all__ = ['DGProfession', 'DGProfessionSet']

from random import randint as _randint


class DGNamedObject(object):
    pass


class DGProfession(object):
    """Represents a profession.
    
    This class is meant to be subclassed. Thus independent use of this class is
    not recommended.
    """
    def __init__(self, name, essential=False, discription='',
                                              usable_items=None):
        """Arguments are:
        
        *name* is the name of the profession.
        
        *essential* is a boolean value indicating whether this profession is
        a must in running the whole plugin.
        
        *discription* is a discription of this profession in strings. It is
        recommended to change discription attribute directly for the sake of
        code readability.
        
        *usable_items* is a list of all usable items of this profession. It is
        advised to use add_usable_items() method over using this argument.
        """
        self._name = name
        self._essential = essential
        self._discription = discription
        if usable_items is None:
            usable_items = []
        self._usable_items = usable_items
        
    def __repr__(self):
        return '{0}()'.format(self.__class__.__name__)
    
    @property
    def name(self):
        return self._name
    
    def add_usable_items(self, items):
        self._usable_items.extend(items)
    
    def usable_items(self):
        return tuple(self._usable_items)
    
    @property
    def discription(self):
        return self._discription
    
    @discription.setter
    def discription(self, discription):
        self._discription = discription
        
    @property
    def essential(self):
        return self._essential
    
    @property
    def info(self):
        """Returns a string containing information on this profession."""
        info_ = self._name
        info_ += '\n' + self.discription + '\n'
        for item in self._usable_items:
            info_ += item + ' '
        info_ += '\n'
        return info_
    
    
class DGProfessionSet(DGProfession):
    """Represents the set of DGProfession, including the probabilities on
    choosing contained profession.
    """
    def __init__(self, name, job_odds=None, essential=False,
                                            discription=None):
        """The arguments are:
        
        *name* is the name of this DGProfession set
        
        *job_odds* is a dictionary containing the professions and its chances 
        to be chosen. The format is as follows:
        {<DGProfession instance>:<probability in integer, ...}
        <probability in integer> does not have to be a total of 100.
        
        *essential* is a boolean value indicating whether this profession is
        a must in running the whole plugin.
        
        *discription* is a discription of this set, in strings. It is
        recommended to change discription attribute directly for the sake of
        code readability.
        """
        super().__init__(name, essential, discription)
        if job_odds is None:
            job_odds = {}
        self._job_odds = job_odds
    
    def jobs(self):
        """Returns a tuple of all jobs contained in this set."""
        return tuple(self._job_odds.keys())
    
    def choose_job(self):
        """Returns a job, depending on the probability specified."""
        job_list = self._job_odds.keys()
        
        total_odds = 0
        for odds in self._job_odds.values():
            total_odds += odds
        
        rand_result = _randint(1, total_odds)
        
        base = 0
        for job in job_list:
            if base < rand_result <= base + self._job_odds[job]:
                final_job = job
                break
            else:
                base += self._job_odds[job]
        
        return final_job
    