##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## RSI
##

from BotAction import BotAction
from ActionState import Action_state

class RSI:
    def __init__(self, period):
        """ Constructor """
        self.H = []
        self.A = []
        self.rsi = []
        self.gain = []
        self.loss = []
        self.signalState = []
        self.period = period
        self.overbought = False
        self.oversold = False

    def calculate_exponential_moving_average(self, value : float, exp_moving_average : list) -> float:
        MME = 0.0
        k = 0.0
        k = 2 / (1 + self.period)
        if exp_moving_average[-1] != None:
            MME = value * k + exp_moving_average[-1] * (1 - k)
        else:
            MME = value * k + value * (1 - k)
        return MME

    def calculate_rsi(self, data) -> None:
        if len(data) > 1:
            R = data[-1] - data[len(data) - 2]
            if R > 0:
                self.gain.append(R)
                self.loss.append(0)
            else:
                self.loss.append(abs(R))
                self.gain.append(0)
        else:
            self.gain.append(0)
            self.loss.append(0)
        if len(self.gain) > self.period:
            self.H.append(sum(self.gain[-(self.period):]) / self.period)
            self.A.append(sum(self.loss[-(self.period):]) / self.period)
        else:
            self.H.append(None)
            self.A.append(None)
        if self.A[-1] != None:
            if self.A[-1] != 0 and (1 + (self.H[-1] / self.A[-1]) != 0):
                self.rsi.append(100 - (100 / (1 + (self.H[-1] / self.A[-1]))))
            else:
                self.rsi.append(50)
        else:
            self.rsi.append(None)

    def get_rsi_state(self, affordable: float, bitcoin : float, botAction: BotAction) -> Action_state:
        if len(self.rsi) == 0:
            self.signalState.append(Action_state.NEUTRAL)
            return Action_state.NEUTRAL

        if self.rsi[-1] == None:
            self.signalState.append(Action_state.CALCULATING)
            return Action_state.CALCULATING
        if self.rsi[-1] > 60 and bitcoin > 0.001:
            self.signalState.append(Action_state.SELL)
            return Action_state.SELL
        if self.rsi[-1] < 40 and affordable > 0.001:
            self.signalState.append(Action_state.BUY)
            return Action_state.BUY
        self.signalState.append(Action_state.NEUTRAL)
        return Action_state.NEUTRAL
    
    def get_rsi_state_on_period(self, affordable: float, bitcoin : float, period : int) -> Action_state:
        if len(self.rsi) == 0:
            self.signalState.append(Action_state.NEUTRAL)
            return Action_state.NEUTRAL

        if self.rsi[-1] == None:
            self.signalState.append(Action_state.CALCULATING)
            return Action_state.CALCULATING
        elif self.rsi[-1] > 80 and bitcoin > 0.001:
            self.signalState.append(Action_state.SELL)
        elif self.rsi[-1] < 40 and affordable > 0.001:
            self.signalState.append(Action_state.BUY)
        else:
            self.signalState.append(Action_state.NEUTRAL)
        i = 1
        
        if (self.signalState[-1] != Action_state.SELL and self.signalState[-2] == Action_state.SELL):
            return Action_state.SELL
        # return (self.signalState[-1])
        # for i in range(period + 1):
        #     if (self.signalState[-i] == Action_state.BUY):
        #         return Action_state.BUY
        #     if (self.signalState[-i] == Action_state.SELL):
        #         return Action_state.SELL
        return Action_state.NEUTRAL
