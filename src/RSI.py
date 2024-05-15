##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## RSI
##

import sys
class RSI:
    def __init__(self, period):
        """ Constructor """
        self.H = []
        self.A = []
        self.rsi = []
        self.gain = []
        self.loss = []
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
            self.H.append(sum(self.gain[-self.period:]) / self.period)
            self.A.append(sum(self.loss[-self.period:]) / self.period)
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