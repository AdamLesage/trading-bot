##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## CandlePatern
##

from ActionState import Action_state
from Chart import Chart
import sys
from typing import Tuple

class CandlePatern:
    def __init__(self):
        pass
    
    def getCandleInfo(self, chart: Chart) -> Tuple[float, float, float]:
        upper_wick = 0.0
        lower_wick = 0.0
        volume = 0.0
        if (chart.opens[-1] < chart.closes[-1]):
            upper_wick = chart.highs[-1] - chart.closes[-1]
            lower_wick = chart.opens[-1] - chart.lows[-1]
            volume = abs(chart.closes[-1] - chart.opens[-1])
        else:
            upper_wick = chart.highs[-1] - chart.opens[-1]
            lower_wick = chart.closes[-1] - chart.lows[-1]
            volume = abs(chart.closes[-1] - chart.opens[-1])
        return volume, upper_wick, lower_wick

    def Hammer(self, chart: Chart) -> bool:
        if (chart.opens[-1] < chart.closes[-1]):
            if (chart.closes[-1] == chart.highs[-1]):
                if (chart.opens[-1] - chart.closes[-1] < (chart.opens[-1] - chart.lows[-1]) * 0.5):
                    return True
        return False
        
    def InverseHammer(self, chart: Chart) -> bool:
        volume, upper_wick, lower_wick = self.getCandleInfo(chart)
        if chart.opens[-1] < chart.closes[-1]:
            if lower_wick < volume and upper_wick > volume * 2:
                return True
        return False

    def useCandlePatern(self, chart: Chart) -> Action_state:
        if (self.Hammer(chart) == True):
            print(f'Hammer candle', file=sys.stderr)
            return Action_state.BUY
        if (self.InverseHammer(chart) == True):
            print(f'InverseHammer candle', file=sys.stderr)
            return Action_state.BUY
        return Action_state.NEUTRAL
