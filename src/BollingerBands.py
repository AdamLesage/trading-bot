##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## BollingerBands
##

class BollingerBands:
    def __init__(self, period):
        """ Constructor """
        self.upper_band = []
        self.lower_band = []
        self.middle_band = []
        self.standard_deviation = []
        self.period = period
        
    def calculate_moving_average(self, data) -> float:
        if len(data) <= self.period:
            return None            
        return sum(data[-self.period:]) / self.period

    def calculate_bollinger_bands(self, data) -> None:
        """ Calculate the Bollinger Bands """
        self.middle_band.append(self.calculate_moving_average(data))
        pass