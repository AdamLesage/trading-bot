##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## BollingerBands
##
from ActionState import Action_state
import math

class BollingerBands:
    def __init__(self, period: int, gap: float):
        """ Constructor """
        self.upper_band = []
        self.lower_band = []
        self.middle_band = []
        self.standard_deviation = []
        self.period = period
        self.gap = gap
        
    def calculate_moving_average(self, data: list) -> float:
        """ Calculate the moving average """
        if len(data) < self.period:
            return None
        return sum(data[-self.period:]) / self.period
    
    def calculate_standard_deviation(self, data: list) -> float:
        """ Calculate the standard deviation """
        if len(data) < self.period:
            return None
        if len(self.middle_band) == 0 or self.middle_band[-1] is None:
            return None
        S = sum([(x - self.middle_band[-1]) ** 2 for x in data[-self.period:]])
        R = math.sqrt(S / self.period)
        return R

    def calculate_bollinger_bands(self, data: list) -> None:
        """ Calculate the Bollinger Bands """
        moving_average = self.calculate_moving_average(data)
        self.middle_band.append(moving_average)
        if moving_average is None:
            self.standard_deviation.append(None)
            self.lower_band.append(None)
            self.upper_band.append(None)
            return
        
        standard_deviation = self.calculate_standard_deviation(data)
        self.standard_deviation.append(standard_deviation)
        
        if standard_deviation is None:
            self.lower_band.append(None)
            self.upper_band.append(None)
        else:
            self.lower_band.append(moving_average - (self.gap * standard_deviation))
            self.upper_band.append(moving_average + (self.gap * standard_deviation))

    def get_bollinger_state(self, current_closing_price: float) -> Action_state:
        """ Indicator Bollinger Bands """
        if (len(self.upper_band) < self.period or len(self.lower_band) < self.period):
            return Action_state.CALCULATING
        if current_closing_price < self.lower_band[-1]:
            return Action_state.BUY
        if current_closing_price > self.upper_band[-1]:
            return Action_state.SELL
        return Action_state.NEUTRAL
