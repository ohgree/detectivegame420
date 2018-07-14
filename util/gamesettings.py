# -*- coding: utf-8 -*-

"""A module containing every constant used in detectivegame420 package"""

from detectivegame420.professions.dgprofession import DGProfessionSet 
from detectivegame420.professions.dgprofessionlist import *

# main module constants
RANDOM_VOTE = -1
PROFESSIONS = [
	# Necessary jobs are advised to go first
	DGProfessionSet('Detective roles', {
		Detective():25, Police():25,
		Doctor():25, Student():25
	}, essential=True),
	DGProfessionSet('Soldier roles', {
		Serviceman():75, DeltaForce():25
	}),
	Engineer(), Clerk(), Chef(), Unemployed()
]

# DGPlayer constants
SANITATION_LOWEST_INITVALUE = 50
SANITATION_DROP_INTERVAL = 10.0
SANITATIONDROP_BLOODY = -50
SANITATIONDROP_SOAK = -20
SCOREDROP_SANITATION_COUNT = 5
DRYING_TIME = 30.0
SANITATION_SCOREDROP = -3

# DGItem constants
ITEMUSE_DEFAULT_SCORE = 5