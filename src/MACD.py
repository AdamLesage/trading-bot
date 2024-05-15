##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## MACD
##

from enum import Enum

class MACD_state(Enum):
    """ Enum for MACD states """
    BULLISH = 1
    BEARISH = 2
    NEUTRAL = 3

class MACD():
    def __init__(self, short_period: int, long_period: int, signal_period: int):
        """ Constructor """
        self.emas = []
        self.macd_line = []
        self.signal_line = []
        self.histogram = []
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

    def calculate_ema(self, data, period) -> float:
        """ Calculate the Exponential Moving Average """
        return data.ewm(span=period, adjust=False).mean()

    def calculate_macd(self, data: list) -> None:
        """ Calculate MACD """
        self.emas.append(self.calculate_ema(data, self.short_period))
        self.emas.append(self.calculate_ema(data, self.long_period))
        self.macd_line = self.emas[0] - self.emas[1]
        self.signal_line = self.calculate_ema(self.macd_line, 9)
        self.histogram = self.macd_line - self.signal_line

    def get_macd_state(self) -> MACD_state:
        """ Get MACD state """
        if self.histogram[-1] > 0:
            return MACD_state.BULLISH
        elif self.histogram[-1] < 0:
            return MACD_state.BEARISH
        else:
            return MACD_state.NEUTRAL
