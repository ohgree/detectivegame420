#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of DGPlayer class in the planned plugin DetectiveGame420"""

__all__ = ['DGPlayer']

# Python default modules
from threading import Thread as _Thread
from random import randint as _randint
from time import sleep as _sleep

# Modules in current package
from detectivegame420.dgutil import DGDelayedScheduler
from detectivegame420.professions.dgprofession import DGProfession

# Constants
from detectivegame420.gamesettings import *

class DGPlayer(object):
    """A class that represents a player in DetectiveGame420.
    
    *To be implemented: outofbreath functions
    """
    # thought it'd be cool to have a attribute like this
    __initialized = False
    
    def __init__(self, name, job=None):
        """Class initialization.
        
        *name* is the name of the player.
        
        *job* is a DGProfession instance
        
        Note: *name* must be changed to Player object when implemented in
        DetectiveGame420 java plugin.
        """
        self._name = name
        self._job = job
        self._iskiller = False
        self._score = 0
        self._sanitation = _randint(SANITATION_LOWEST_INITVALUE, 99)
        self._soaked = False
        self._invisible = False
        self._breath = 0
        self._bloody = False
        self._alive = True
        # this variable must have no other means of setting its value to False
        self._bloody_once = False
        # sanitation drop start
        self.__sanitation_fall_thread = _Thread(target=self.__fsanitation)
        self.__sanitation_fall_thread.setDaemon(True)
        self.__sanitation_fall_thread.start()
        self.__initialized = True
        
    def __repr__(self):
        assert self.__initialized, 'DGPlayer.__init__() was not called'
        return '{0}({1}, {2})'.format(self.__class__.__name__,
                                      repr(self._name), repr(self._job))
    
    def __del__(self):
        # TODO: find a way to terminate self.__sanitation_fall_thread
        pass
    
    def __setattr__(self, attr, value):
        try:
            super().__setattr__(attr, value)
        except AttributeError:
            raise AttributeError('readonly attribute')
    
    def __delattr__(self, attr):
        try:
            super().__delattr__(attr, value)
        except AttributeError:
            raise AttributeError('readonly attribute')
    @property
    def alive(self):
        return self._alive
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        assert isinstance(name, str), 'name must be a string'
        self._name = name
        
    @property
    def job(self):
        return self._job
    
    @job.setter
    def job(self, job):
        assert isinstance(job, DGProfession), \
            'job must be a DGProfession instance'
        self._job = job
        
    @property
    def iskiller(self):
        return self._iskiller
    
    def setkiller(self):
        """Sets the player to be a killer.
        
        This method has no means of knowing whether there's more than one killer
        in the game, so use with caution.
        """
        self._iskiller = True
        
    @property
    def score(self):
        return self._score
    
    @property
    def bloody(self):
        """Returns a boolean value of bloody variable
        
        Use setbloody() to set the value to True
        """
        return self._bloody
    
    @property
    def bloody_once(self):
        return self._bloody_once
    
    @property
    def invisible(self):
        return self._invisible
    
    @property
    def soaked(self):
        return self._soaked
    
    @property
    def sanitationlevel(self):
        """Returns an integer representing current sanitation level.
        
        0 : filthy   (0 <= sanitation < 25)
        1 : unclean  (25 <= sanitation < 50)
        2 : mediocre (50 <= sanitation < 75)
        3 : clean    (75 <= sanitation < 100)
        """
        return self._sanitation // 25
    
    @property
    def sanitation(self):
        """The value must be in range 0<= *value* < 100.
        
        Worry not, the program will correct itself it the value is out of
        range.
        """
        return self._sanitation
    
    @sanitation.setter
    def sanitation(self, value):
        assert isinstance(value, int), 'value must be an integer'
        self._setsanitation(value)
    
    def addscore(self, score, msg=''):
        """Adds scores to player. Also sends a message to player. No message
        is shown if *score* is 0
        
        *score* is an integer. Can be a negative value.
        
        *msg* is the optional message sent after the score's been applied.
        """
        if score is 0:
            return None
        self._score += score
        score_message = '(To {0}) {1:+}pts'.format(self._name, score)
        if msg:
            msg = score_message + ': ' + msg
        print(score_message)
        
    def _setdry(self):
        # private! This method should not be accessed directly since
        # the drying process must be scheduled only by soak() method.
        print('{0} is now fully dried'.format(self._name))
        self._soaked = False
        
    def _setsanitation(self, value):
        """Safely sets sanitation value
        
        *value* is a signed integer
        
        This method will check if total sum of current sanitation and *value*
        exceeds the limit and adds given *value* to sanitation accordingly.
        """
        if value < 0:
            value = 0
        elif value >= 100:
            value = 99
        self._sanitation = value
        
    def soak(self):
        """Sets the player's soaked state
        
        This method calls DGUtil.DGDelayedScheduler to schedule a call to
        _setdry() method after DRYING_TIME has passed. Also drops sanitation
        based on SANITATIONDROP_SOAK value
        """
        if not self._soaked:
            self._soaked = True
            self._setsanitation(self._sanitation + SANITATIONDROP_SOAK)
            
        try:
            self._soaktimer.cancel()
        except AttributeError:
            pass
        
        self._soaktimer = DGDelayedScheduler(target=self._setdry,
                                             interval=DRYING_TIME)
        self._soaktimer.start()
        
    def wash(self):
        """Washes the player, adds soaked state and removes bloody state.
        
        soak() method is called before restoring sanitation, since soak() method
        decreases sanitation. This method won't remove bloody_once state
        """
        self._bloody = False
        self.soak()
        self._setsanitation(100)
        
    def kill(self):
        """Kills the player.
        
        This method must kill the player in-game, and also set kill flag inside
        this class.
        """
        if not self._alive:
            raise RuntimeError('The player is dead already')
        
        # bukkit plugin process goes here
        
        self._alive = False
        
        # player death message
        print('{}\'s been killed.'.format(self._name))
        
    def setbloody(self):
        """Sets bloody flag on the player.
        
        bloody_once is also set to True. This value cannot be set back to False.
        Sanitation is dropped significantly, by SANITATIONDROP_BLOODY
        """
        if not self._bloody:
            self._bloody = self._bloody_once = True
            self._setsanitation(self._sanitation + SANITATIONDROP_BLOODY)
    
    def __fsanitation(self):
        # private! This method should not be called independently. Otherwise
        # the program will be stuck in a permanent loop
        """A target method for threading.Thread
        
        Drops sanitation with max interval being SANITATION_DROP_INTERVAL. If
        sanitation value is 0, the score is dropped every maximum ticks of 
        SCOREDROP_SANITATION_COUNT.
        """
        SCOREDROPCOUNT = SCOREDROP_SANITATION_COUNT
        # To add more randomness, uncomment following:
        SCOREDROPCOUNT = _randint(0, SCOREDROP_SANITATION_COUNT)
        while True:
            #_sleep(SANITATION_DROP_INTERVAL)
            # To add more randomness, uncomment following:
            _sleep(_randint(1, SANITATION_DROP_INTERVAL))
            self._setsanitation(self._sanitation-1)
            if self._sanitation is 0:
                SCOREDROPCOUNT -= 1
                if SCOREDROPCOUNT <= 0:
                    #SCOREDROPCOUNT = SCOREDROP_SANITATION_COUNT
                    # To add more randomness, uncomment following:
                    SCOREDROPCOUNT = _randint(1, SCOREDROP_SANITATION_COUNT)
                    self.addscore(SANITATION_SCOREDROP,
                                 'Low sanitation. Use a water tap nearby.')
    
    def _setinvisible(self, invisible):
        # private! This method should not be called independently.
        
        # sound effect goes here
        
        self._invisible = invisible
    
    def setinvisible(self, time):
        """Sets invisible flag and disables it after *time* seconds have passed.
        
        Using DGUtil.DGDelayedScheduler, this method reads remaining repeats if
        an invisibility scheduler is running atm and sets a new scheduler with
        durations combined.
        """
        remainingtime = 0
        try:
            remainingtime = self.__invisibletimer.remainingrepeats
            self.__invisibletimer.cancel()
        except AttributeError:
            # __invisibletimer has not been set yet.
            pass
        except RuntimeError:
            # __invisibletimer has already been terminated.
            pass
        
        self._setinvisible(True)
        self.__invisibletimer = DGDelayedScheduler(target=self._setinvisible,
                                interval=1, repeat=time+remainingtime,
                                args=(True,), endtarget=self._setinvisible,
                                eargs=(False,))
        self.__invisibletimer.start()
        
# Self-test code
def _test():
    p = DGPlayer('OhGree')
    print(p._DGPlayer__sanitation_fall_thread)
    print(p.sanitation)
    _sleep(10)
    print(p.sanitation)
    p.setbloody
    print(p.sanitation)

if __name__ == '__main__':
    _test()