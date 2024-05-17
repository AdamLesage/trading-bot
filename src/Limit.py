##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## Limit
##

class RSI:
    def __init__(self, Gain : float, Loss : float):
        """ Constructor """
        self.last_buy = []
        self.Loss = Loss
        self.Gain = Gain

    def loss_limit(self, value : float) -> bool:
        if (len(self.last_buy) == 0):
            return False
        if value < self.last_buy[-1] * self.Loss:
            return True
        else:
            return False
    
    def update_limit_buy(self, new_value : float) -> None:
        self.last_buy.append(new_value)
