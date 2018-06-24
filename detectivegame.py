#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Demonstration of the main class in the planned plugin DetectiveGame420"""

# Python default modules
from random import randint as _randint

from detectivegame420.dgplayer import DGPlayer
from detectivegame420.dgutil import allocate_jobs_to_players
from detectivegame420.professions.dgprofession import DGProfessionSet
from detectivegame420.professions.dgprofessionlist import *

# Constants
from detectivegame420.gamesettings import RANDOM_VOTE, PROFESSIONS

def main():
    # Prompt
    for index, prof in enumerate(PROFESSIONS):
        print('{:>19}: {}'.format(prof.name, index))
    print('{:>19}: {}'.format('RANDOM', 'Any other numbers'))

    # Voting
    vote_result = {}
    player_num = int(input('Number of players: '))
    for i in range(player_num):
        player_name = input('{}th player name: '.format(i+1))
        try:
            prof_vote = int(input('{}\'s vote: '.format(player_name)))
        except ValueError as e:
            vote_result[DGPlayer(player_name)] = RANDOM_VOTE
        else:
            if 0 <= prof_vote < len(PROFESSIONS):
                vote_result[DGPlayer(player_name)] = PROFESSIONS[prof_vote]
            else:
                vote_result[DGPlayer(player_name)] = RANDOM_VOTE
    
    # Assign jobs to players
    assigned_players = allocate_jobs_to_players(PROFESSIONS, Unemployed(),
            vote_result)

    # Choose killer
    assigned_players[_randint(0, len(assigned_players)-1)].setkiller()

    # Print results
    # Before
    print()
    print('{:=^79}'.format(' Vote '))
    for player in assigned_players:
        if vote_result[player] == RANDOM_VOTE:
            print('{:15}-> {}'.format(player.name, 'Random roles'))
        else:
            print('{:15}-> {}'.format(player.name, vote_result[player].name))
    print()

    # After
    print('{:=^79}'.format(' Result '))
    for player in assigned_players:
        print('{:15}-> {}'.format(player.name, player.job.name))
    print()

    # Successful voters
    match = 0
    for player in vote_result.keys():
        if vote_result[player] == RANDOM_VOTE:
            match += 1
        elif vote_result[player] is player.job:
            match += 1
        elif isinstance(vote_result[player], DGProfessonSet):
            if player.job.name in [j.name for j in vote_result[player].jobs()]:
                match += 1
    print('matches: {}'.format(match))

    # Show killer
    for p in assigned_players:
        if p.iskiller:
            print('Killer: {}'.format(p.name))

    return assigned_players

# Self-test code
if __name__ == '__main__':
    import sys

    try:
        sys.stdin = open(r'./input.txt', 'r')
    except IOError:
        print('input.txt not found', file=sys.stderr)
    _ret = _main()
    sys.stdin.close()
    
