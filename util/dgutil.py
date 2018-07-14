#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of DGUtil class in the planned plugin DetectiveGame420"""

__all__ = [
    'DGScheduler', 'DGDelayedScheduler', 'elect_key_with_modifier',
    'allocate_jobs_to_players', 'get_killer', 'eligible_itemuse',
]

from threading import Thread as _Thread
from random import randint as _randint
from time import sleep as _sleep

from detectivegame420.professions.dgprofession import DGProfessionSet


class DGScheduler(_Thread):
    """Not implemented as of now. Raises NotImplementedError if called."""
    def __init__(self, target):
        raise NotImplementedError
        super().__init__(target=target)
        self.setDaemon(True)
    
    def run(self):
        pass
    
    
class DGDelayedScheduler(_Thread):
    """Schedules a repeated delayed task.
    
    Important note: The target object is called after the specified delay. For
    other means of schduling, please refer to (WIP)DGScheduler.
    
    This class inherits threading.Thread
    """
    __initialized = False
    def __init__(self, target, interval=0, repeat=1, args=(), kwargs=None,
                 endmessage=None, endtarget=None, eargs=(), ekwargs=None):
        """This constructor should be called with keyword arguments.
        Arguments are:
        
        *target* is the callable object to be invoked.
        
        *interval* is an integer representing the interval(in seconds) between
        each *target* calls. Defaults to 0.
        
        *repeat* is the number of times that the *target* object needs to be
        called. Defaults to 1.
        
        *endmessage* is the message printed when the thread is terminated. It
        defaults to None.
        
        *args*, *kwargs* is arguments passed on to threading.Thread. Refer to
        threading.Thread pydoc for more information.
        """
        super().__init__()
        if kwargs is None:
            kwargs = {}
        if ekwargs is None:
            ekwargs = {}
        if endmessage is None:
            endmessage = ''
        self._target = target
        self._interval = interval
        self._repeat = repeat
        self._args = args
        self._kwargs = kwargs
        self._endmessage = endmessage
        self._endtarget = endtarget
        self._eargs = eargs
        self._ekwargs = ekwargs
        self.setDaemon(True)
        self.__finished = False
        self.__initialized = True
        
    def run(self):
        self._remainingrepeats = self._repeat
        while True:
            if self._remainingrepeats is 0:
                if self._endmessage:
                    print(self._endmessage)
                if self._endtarget:
                    self._endtarget(*self._eargs, **self._ekwargs)
                break
            
            _sleep(self._interval)
            
            if self.__finished:
                break
            
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            except TypeError:
                pass
            
            self._remainingrepeats -= 1
        self.__finished = True
        
    @property
    def remainingrepeats(self):
        """Returns the amount of repeats left
        
        Throws RuntimeError if the thread has already been terminated.
        """
        assert self.__initialized, 'DGScheduler.__init__() has not been called'
        if self.__finished:
            raise RuntimeError('The thread has already been terminated')
            
        return self._remainingrepeats
    
    def cancel(self):
        """Stops the scheduler if it hasn't finished yet"""
        assert self.__initialized, 'DGScheduler.__init__() has not been called'
        
        self.__finished = True
        
def elect_key_with_modifier(target, preference, multiplier=10):
    """Chooses a pseudo-random key in dictionary, affected by preference
    
    *target* is the value in *preference* that we are trying to get electors
    for
    
    *preference* is a dictionary containing *target*'s preference for the
    result. The format is:
    {<key>: <target name>, ...}
    
    *multiplier* is a modifier for prioritizing the whole preferences.
    Defaults to 10 as it is the supposed optimum value, yielding approx. 70%
    election chance. Value of 1 makes all keys to have equal probabilities,
    regardless of their preferences.
    
    Returns elected key.
    """
    assert isinstance(preference, dict), '*preference* should be a dictionary'
    
    candidate = []
    for key in preference.keys():
        if preference[key] is target:
            candidate.extend([key] * multiplier)
        else:
            candidate.append(key)
    return candidate[_randint(0, len(candidate)-1)]

def allocate_jobs_to_players(professions, default_profession, vote):
    assert isinstance(vote, dict), '*vote* should be a dictionary'
    
    # list of assigned players
    assigned_players = []
    
    for prof in professions:
        player = elect_key_with_modifier(prof, vote)
        
        # part for ensuring jobs with essential=True to elect a non-assigned
        # player. This implementation does not overwrite elected players,
        # therefore is prone to cause unexpected results, such as infinite
        # loops, if there's no unassigned player left
        # the initial programmer was too lazy to fix this
        if prof.essential:
            while player in assigned_players:
                player = elect_key_with_modifier(prof, vote)
        
        if player not in assigned_players:
            if isinstance(prof, DGProfessionSet):
                prof = prof.choose_job()
            player.job = prof
            assigned_players.append(player)
    
    for player in vote.keys():
        if player not in assigned_players:
            # warning! creating a new instance of DGProfession like this could
            # lead to unexpected results. keep in mind that every job instances
            # other than this one has been already initialized in PROFESSIONS
            player.job = default_profession
            assigned_players.append(player)
    
    return assigned_players

def get_killer(player_list):
    """Finds all killers in the specified list
    
    *player_list* is a list of DGPlayer instances
    
    Returns a tuple containing all killers found.
    """
    killers = []
    for p in player_list:
        if p.iskiller:
            killers.append(p)
    
    return tuple(killers)

def eligible_itemuse(player, item):
    """Checks whether the *player* is eligible to use specified *item*.
    
    *player* is a DGPlayer instance
    
    *item* is a DGItem instance
    
    Returns True if eligible, and False if not.
    """
    if player.job.name in [j.name for j in item.user_jobs]:
        return True
    else:
        return False
    
# Self-test code
def _test():
    from detectivegame420.players.dgplayer import DGPlayer
    from detectivegame420.util.gamesettings import PROFESSIONS
    
    player_list = [DGPlayer('Minjun Shin'), DGPlayer('Gree Oh')]
    print([p.name for p in player_list])
    
if __name__ == '__main__':
    _test()
