##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## StochasticOscillator
##

class StochasticOscillator:
    def __init__(self):
        """ Constructor """
        self.k = []
        self.d = []
        self.overbought = 0
        self.oversold = 0

    def calculate_stochastic_oscillator(self, data, period) -> None:
        """ Calculate the Stochastic Oscillator """
        pass