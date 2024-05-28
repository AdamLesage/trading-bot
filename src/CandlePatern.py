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
    
    def getCandleInfo(self, high, low, close, open) -> Tuple[float, float, float]:
        upper_wick = 0.0
        lower_wick = 0.0
        volume = 0.0
        if (open < close):
            upper_wick = high - close
            lower_wick = open - low
            volume = abs(close - open)
        else:
            upper_wick = high - open
            lower_wick = close - low
            volume = abs(close - open)
        return volume, upper_wick, lower_wick

    def Hammer(self, chart: Chart) -> bool:
        if (chart.opens[-1] < chart.closes[-1]):
            if (chart.closes[-1] == chart.highs[-1]):
                if (chart.opens[-1] - chart.closes[-1] < (chart.opens[-1] - chart.lows[-1]) * 0.5):
                    return True
        return False

    def InverseHammer(self, chart: Chart) -> bool:
        volume, upper_wick, lower_wick = self.getCandleInfo(chart.highs[-1], chart.lows[-1], chart.closes[-1], chart.opens[-1])
        if chart.opens[-1] < chart.closes[-1]:
            if lower_wick < volume and upper_wick > volume * 2:
                return True
        return False
    
    def BullishEngulfing(self, chart: Chart):
        if len(chart.closes) < 2:
            return False
        if chart.closes[-2] < chart.opens[-2] and chart.closes[-1] > chart.opens[-1]:
            if chart.lows[-1] <= chart.lows[-2] and chart.closes[-1] >= chart.highs[-2]:
                return True
        return False
                
    def useCandlePatern(self, chart: Chart) -> Action_state:
        if (self.Hammer(chart) == True):
            print(f'Hammer candle', file=sys.stderr)
            return Action_state.BUY
        if (self.InverseHammer(chart) == True):
            print(f'InverseHammer candle', file=sys.stderr)
            return Action_state.BUY
        if (self.BullishEngulfing(chart) == True):
            print(f'BullishEngulfing candle', file=sys.stderr)
            return Action_state.BUY
        return Action_state.NEUTRAL
