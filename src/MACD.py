##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## MACD
##
from enum import Enum
from BotAction import BotAction
import sys

class MACD_state(Enum):
    """ Enum for MACD states """
    BUY = 1
    SELL = 2
    NEUTRAL = 3

class MACD():
    def __init__(self, short_period: int, long_period: int, signal_period: int, epsilon: float = 1e-2):
        """ Constructor """
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.epsilon = epsilon
        self.macd_line = []
        self.signal_line = []
        self.histogram = []

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
        """ Calculate MACD """
        short_ema = self.calculate_ema(data, self.short_period)
        long_ema = self.calculate_ema(data, self.long_period)
        self.macd_line = [short - long for short, long in zip(short_ema, long_ema)]
        self.signal_line = self.calculate_ema(self.macd_line, self.signal_period)
        self.histogram = [macd - signal for macd, signal in zip(self.macd_line, self.signal_line)]

    def get_macd_state(self) -> MACD_state:
        """ Get MACD state """
        print(f"{self.epsilon:.6f}", file=sys.stderr)
        if not self.histogram:
            return MACD_state.NEUTRAL
        if self.histogram[-1] > self.epsilon:
            return MACD_state.BUY
        elif self.histogram[-1] < -self.epsilon:
            return MACD_state.SELL
        else:
            return MACD_state.NEUTRAL

    def do_action(self, bot_action: BotAction) -> None:
        """ Do action """
        state = self.get_macd_state()
        print(f'{state=}', file=sys.stderr)
        # if state == MACD_state.BUY:
        #     print('Buy', file=sys.stderr)
        #     bot_action.buyAction(0.01)
        # elif state == MACD_state.SELL:
        #     print('Sell', file=sys.stderr)
        #     bot_action.sellAction(0.01)
        # else:
        bot_action.passAction()
