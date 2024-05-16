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
        self.macd_line.append(short_ema[-1] - long_ema[-1])
        self.signal_line = self.calculate_ema(self.macd_line, self.signal_period)
        # print(f"{self.macd_line[-1]=}, {self.signal_line[-1]=}", file=sys.stderr)
        self.histogram.append(self.macd_line[-1] - self.signal_line[-1])

    def get_macd_state(self) -> Action_state:
        """ Get MACD state """
        # print(f"{self.epsilon:.6f}, {self.histogram[-1]=}", file=sys.stderr)
        if not self.histogram:
            return Action_state.NEUTRAL
        if self.histogram[-1] > self.epsilon:
            return Action_state.BUY
        elif self.histogram[-1] < -self.epsilon:
            return Action_state.SELL
        else:
            return Action_state.NEUTRAL

    def do_action(self, bot_action: BotAction, affordable: float, bitcoin: float) -> None:
        """ Do action """
        state = self.get_macd_state()
        # print(f'{state=}', file=sys.stderr)
        if state == Action_state.BUY and affordable > 0.001:
            bot_action.buyAction(affordable * 0.4)
        elif state == Action_state.SELL and bitcoin > 0.001:
            bot_action.sellAction(bitcoin * 0.4)
        else:
            bot_action.passAction()
