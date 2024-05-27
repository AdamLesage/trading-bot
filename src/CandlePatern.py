##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## CandlePatern
##

from ActionState import Action_state

import sys

class CandlePatern:
    def __init__(self):
        pass
    def useCandlePatern(candle : Candle) -> Action_state:
        print(f'{candle.close=} {candle.open=} {candle.high=} {candle.low=}', file=sys.stderr)
        return Action_state.NEUTRAL
