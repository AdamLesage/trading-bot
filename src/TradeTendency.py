##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## TradeTendency
##

from enum import Enum

class TradeTendency(Enum):
    """ Enum for Action states """
    NONE = 1
    UP = 2
    DOWN = 3