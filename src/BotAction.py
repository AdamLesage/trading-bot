##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## Action
##

class BotAction:
    def __init__(self):
        pass

    def passAction(self):
        print("no_moves", flush=True)
        
    def sellAction(self, currency : float):
        print(f"sell USDT_BTC {currency}", flush=True)

    def buyAction(self, currency : float):
        print(f"buy USDT_BTC {currency}", flush=True)
