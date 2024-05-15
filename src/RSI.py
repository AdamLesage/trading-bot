##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## RSI
##

class RSI:
    def __init__(self, period):
        """ Constructor """
        self.H = []
        self.A = []
        self.rsi = []
        self.period = period
        self.overbought = False
        self.oversold = False

    def calculate_exponential_moving_average(self, data) -> float:
        
        pass

    def calculate_rsi(self, data) -> None:
        self.H.append(self.calculate_exponential_moving_average(float, data))
        self.A.append(self.calculate_exponential_moving_average(float, data))
        if self.A[-1] != None:
            self.rsi.append(100 - (100 / 1 + (self.H[-1] / self.B[-1])))
        pass