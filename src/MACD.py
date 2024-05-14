##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## MACD
##

class MACD():
    def __init__(self):
        """ Constructor """
        self.emas = []
        self.macd_line = []
        self.signal_line = []
        self.histogram = []

    def calculate_ema(self, data, period) -> float:
        """ Calculate the Exponential Moving Average """
        pass
