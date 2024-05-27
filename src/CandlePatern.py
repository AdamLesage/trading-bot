##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## CandlePatern
##

from ActionState import Action_state
from Chart import Chart
import sys

class CandlePatern:
    def __init__(self):
        pass
    def useCandlePatern(self, chart: Chart) -> Action_state:
        print(f'close = {chart.closes[-1]} opens = {chart.opens[-1]} highs = {chart.highs[-1]} lows = {chart.lows[-1]}', file=sys.stderr)
        return Action_state.NEUTRAL
