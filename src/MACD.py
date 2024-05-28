##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## MACD
##

from BotAction import BotAction
import sys
from ActionState import Action_state

class MACD():
    def __init__(self, short_period: int, long_period: int, signal_period: int, epsilon: float = 1e-5):
        """ Constructor """
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.epsilon = epsilon
        self.macd_line = []
        self.signal_line = []
        self.histogram = []
        self.short_emas = []
        self.long_emas = []

    def reset(self):
        """ Reset the MACD """
        self.macd_line = []
        self.signal_line = []
        self.histogram = []
        self.short_emas = []
        self.long_emas = []

    def ewm(self, data: list, span: int) -> list:
        """ Exponential Weighted Moving Average """
        weight = 2 / (span + 1)
        ema = [data[0]]
        for i in range(1, len(data)):
            ema.append(data[i] * weight + ema[i - 1] * (1 - weight))
        return ema

    def calculate_ema(self, data: list, period: int) -> list:
        """ Calculate the Exponential Moving Average """
        return self.ewm(data, period)

    def calculate_macd(self, data: list) -> None:
        """Calculate MACD"""
        if len(data) < self.long_period:
            self.signal_line.extend([None] * len(data))
            self.histogram.extend([None] * len(data))
            return

        self.short_emas = self.calculate_ema(data, self.short_period)
        self.long_emas = self.calculate_ema(data, self.long_period)

        for i in range(len(self.long_emas)):
            if i + self.long_period - self.short_period >= len(self.short_emas):
                break
            macd_value = self.long_emas[i] - self.short_emas[i + self.long_period - self.short_period]
            self.macd_line.append(macd_value)

        # Calculate the signal line
        if len(self.macd_line) >= self.signal_period:
            signal_ema = self.calculate_ema(self.macd_line, self.signal_period)
            self.signal_line = signal_ema

            for i in range(len(signal_ema)):
                if i + self.signal_period - 1 >= len(self.macd_line):
                    break
                self.histogram.append(self.macd_line[i + self.signal_period - 1] - self.signal_line[i])
        else:
            # Append None if not enough data to calculate signal line and histogram
            self.signal_line.extend([None] * (len(self.macd_line) - len(self.signal_line)))
            self.histogram.extend([None] * (len(self.macd_line) - len(self.histogram)))


    def get_macd_state(self, affordable: float, bitcoin: float) -> Action_state:
        """ Get MACD state """
        # print(f"{self.epsilon:.6f}, {self.histogram[-1]=}", file=sys.stderr)
        if not self.histogram or self.histogram[-1] == None: # If histogram is empty or None
            return Action_state.CALCULATING

        if self.short_emas[-1] > self.long_emas[-1] and self.short_emas[-2] < self.long_emas[-2]: # If MACD line crosses signal line and should buy
            return Action_state.BUY
        if self.short_emas[-1] < self.long_emas[-1] and self.short_emas[-2] > self.long_emas[-2]: # If MACD line crosses signal line and should sell
            return Action_state.SELL
        return Action_state.NEUTRAL
