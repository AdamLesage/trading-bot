##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## BollingerBands
##

import math
class BollingerBands:
    def __init__(self, period : int, gap : float):
        """ Constructor """
        self.upper_band = []
        self.lower_band = []
        self.middle_band = []
        self.standard_deviation = []
        self.period = period
        self.gap = gap
        
    def calculate_moving_average(self, data : list) -> float:
        """ Calculate the moving average """
        if len(data) <= self.period:
            return None            
        return sum(data[-self.period:]) / self.period
    
    def calculate_standard_deviation(self, data : list) -> float:
        """ Calculate the standard deviation """
        if  self.middle_band[-1] == None:
            return None
        S = sum(pow(data[-self.period:] - self.middle_band, 2))
        R = math.sqrt(S / self.period - 1)
        return R

    def calculate_bollinger_bands(self, data : list) -> None:
        """ Calculate the Bollinger Bands """
        self.middle_band.append(self.calculate_moving_average(data))
        self.standard_deviation.append(self.calculate_bollinger_bands(data))
        if (self.middle_band != None):
            self.lower_band.append(self.middle_band[-1] - (self.gap * self.standard_deviation))
            self.upper_band.append(self.middle_band[-1] + (self.gap * self.standard_deviation))
