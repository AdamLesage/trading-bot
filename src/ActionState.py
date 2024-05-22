##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## ActionState
##

from enum import Enum

class Action_state(Enum):
    """ Enum for Action states """
    BUY = 1
    SELL = 2
    NEUTRAL = 3
