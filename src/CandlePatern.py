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
    
    def getCandleVolume(self, close, open) -> float:
        volume = abs(close - open)
        return volume

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
    
    def BullishEngulfing(self, chart: Chart) -> bool:
        if len(chart.closes) < 2:
            return False
        if chart.closes[-2] < chart.opens[-2] and chart.closes[-1] > chart.opens[-1]:
            if chart.lows[-1] <= chart.lows[-2] and chart.closes[-1] >= chart.highs[-2]:
                return True
        return False
    
    def MorningStar(self, chart: Chart) -> bool:
        if len(chart.closes) < 3:
            return False
        if (chart.opens[-3] > chart.closes[-3] and chart.opens[-1] < chart.closes[-1]):
            volume = self.getCandleVolume(chart.closes[-3], chart.opens[-3])
            volume2 = self.getCandleVolume(chart.closes[-2], chart.opens[-2])
            volume3 = self.getCandleVolume(chart.closes[-1], chart.opens[-1])
            if volume2 * 4 < volume and volume2 * 4 < volume3:
                print(volume, volume2, volume3, file=sys.stderr)
                return True
        return False
                
    def ThreeWhiteSoldiers(self, chart: Chart):
        if len(chart.closes) < 3:
            return False
        if chart.opens[-3] < chart.closes[-3] and chart.opens[-2] < chart.closes[-2] and chart.opens[-1] < chart.closes[-1]:
            volume, upper_wick, lower_wick = self.getCandleInfo(chart.highs[-3], chart.lows[-3], chart.closes[-3], chart.opens[-3])
            volume2, upper_wick2, lower_wick2 = self.getCandleInfo(chart.highs[-2], chart.lows[-2], chart.closes[-2], chart.opens[-2])
            volume3, upper_wick3, lower_wick3 = self.getCandleInfo(chart.highs[-1], chart.lows[-1], chart.closes[-1], chart.opens[-1])
            if (upper_wick3 * 2 < volume3 and lower_wick3 * 2 < volume3 and
                upper_wick2 * 2 < volume2 and lower_wick2 * 2 < volume2 and
                upper_wick * 2 < volume and lower_wick * 2 < volume):
                return True
        return False
    
    def HangingMan(self, chart: Chart):
        if (chart.opens[-1] > chart.closes[-1]):
            if (chart.closes[-1] * 1.1 >= chart.highs[-1]):
                if (chart.opens[-1] - chart.closes[-1] < (chart.opens[-1] - chart.lows[-1]) * 0.5):
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
            print(f'BullishEngulfing pattern', file=sys.stderr)
            return Action_state.BUY
        if (self.MorningStar(chart) == True):
            print(f'MorningStar pattern', file=sys.stderr)
            return Action_state.BUY
        if (self.ThreeWhiteSoldiers(chart) == True):
            print(f'ThreeWhiteSoldiers pattern', file=sys.stderr)
            return Action_state.BUY
        if (self.HangingMan(chart) == True):
            print(f'HangingMan pattern', file=sys.stderr)
            return Action_state.SELL
        return Action_state.NEUTRAL
