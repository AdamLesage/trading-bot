##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## RiskIndicator
##

from ActionState import Action_state

class RiskIndicator():
    def __init__(self, period: int = 20):
        self.period = period

    def get_risk_state(self, closing_prices: list) -> str:
        """Returns the risk state"""
        if len(closing_prices) < self.period:
            return "MEDIUM"
        mean_close = sum(closing_prices) / len(closing_prices)
        standard_deviation = (sum([(x - mean_close) ** 2 for x in closing_prices]) / len(closing_prices)) ** 0.5
        if closing_prices[-1] < mean_close - standard_deviation:
            return "HIGH"
        elif closing_prices[-1] > mean_close + standard_deviation:
            return "LOW"
        return "MEDIUM"
