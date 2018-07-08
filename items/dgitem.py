#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of Item class in the planned plugin DetectiveGame420"""

__all__ = ['DGItem', 'DGFood', 'InvestigationItem']

from detectivegame420.dgutil import eligible_itemuse

# Constants
from detectivegame420.gamesettings import ITEMUSE_DEFAULT_SCORE


class DGItemBase(object):
    raise NotImplementedError('This class is not yet to be implemented')
    pass

class DGItem(object):
    """A class representing an item in DetectiveGame420
    
    This class is meant to be subclassed, therefore it is not a good idea to
    use this as it is.
    """
    def __init__(self, name, user_jobs=(), killer_only=False,
                 itemuse_score=ITEMUSE_DEFAULT_SCORE, discription=None):
        """Initializing this class with keyword arguments is recommended.
        Arguments are:
        
        *name* is the name of this item.
        
        *user_jobs* is a tuple of DGProfession instances representing the jobs
        eligible for using this item. Defaults to an empty tuple, meaning that
        everyone can use this item.
        
        *killer_only* is a boolean value showing whether this item can be used
        only by killers. If set, the eligibility check for *user_jobs* is
        overridden.
        
        *itemuse_score* is an integer for scores given when a player 
        successfully uses this item. Can be a negative value, although not
        recommended to be so.
        
        *discription* is the discription of this item in strings. Using 
        discription attribute is recommended, for the sake of PEP-8.
        
        If a subclass overrides the constructor, make sure to invoke the base 
        class constructor(DGItem.__init__()) before doing anything else.
        """
        self._name = name
        self._user_jobs = user_jobs
        self._killer_only = killer_only
        if discription is None:
            discription = ''
        self._discription = discription
        self._itemuse_score = itemuse_score
        self._use_msg = 'Used item - {name}'
    
    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, repr(self._name))
    
    @property
    def name(self):
        return self._name
    
    @property
    def discription(self):
        return self._discription
    
    @discription.setter
    def discription(self, discription):
        self._discription = discription
        
    @property
    def user_jobs(self):
        return self._user_jobs
    
    @property
    def killer_only(self):
        return self._killer_only
    
    @property
    def use_msg(self):
        return self._use_msg
    
    @use_msg.setter
    def use_msg(self, msg):
        if not isinstance(msg, str):
            raise ValueError('message must be a formatted string')
        self._use_msg = msg
        
    @property
    def info(self):
        """Returns a string containing information on this current item."""
        info_ = self._name + '\n'
        info_ += self._discription + '\n'
        info_ += 'User: '
        if not self._user_jobs:
            if self._killer_only:
                info_ += 'Killer only'
            else:
                info_ += 'Everyone'
        else:
            for j in self._user_jobs:
                info_ += j.name + ' '
        info_ += '\n'
        return info_
    
    def make_item(self):
        pass
    
    def use(self, player):
        if eligible_itemuse(player, self):
            if self.run_item(player):
                player.addscore(self._itemuse_score,
                                self._use_msg.format(name=self._name))
                
    def run_item(self, player):
        """Runs the item and returns result.
        
        This method is meant to be overridden when subclassed.
        
        Important note: When overridden, this method must return True if the run
        was successful, otherwise return False.
        """
        raise NotImplementedError('run_item() method has not been overridden')
        
        
class InvestigationItem(DGItem):
    def __init__(self, name, *user_jobs):
        super().__init__(name, user_jobs)
        self._inspect_messages = {}
        
    def add_inspect_messages(self, **kwmsg):
        self._inspect_messages.update(kwmsg)
        
    # Override
    def run_item(self, player):
        # Investigation process
        pass
    
    
class DGFood(DGItem):
    __cooked = False
    def __init__(self, rawfood, rawfood_value, cookedfood, cookedfood_value):
        super().__init__(name=rawfood, itemuse_score=0)
        self._cookedfood = cookedfood
        self._food_value = self._rawfood_value = rawfood_value
        self._cookedfood_value = cookedfood_value
    
    # Override
    def run_item(self, player):
        # fill player hunger based on food value
        pass
    
    def cook(self):
        self._name = self._cookedfood
        self._food_value = self._cookedfood_value
        # itemstack substitution here
        self.make_item()
        self.__cooked = True
    
    @property
    def cooked(self):
        return self.__cooked
        
