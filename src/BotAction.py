##
## EPITECH PROJECT, 2024
## B-CNA-410-NAN-4-1-trade-adam.lesage
## File description:
## Action
##

class BotAction:
    def __init__(self):
        pass

    def passAction(self) -> None:
        """Prints no_moves to stdout"""
        print("no_moves", flush=True)

    def determineHowManyToBuy(self, affordable: float, risk: str) -> float:
        """Returns best amount of bitcoin to buy from the current closing prices"""
        to_buy = 0
        if risk == "HIGH":
            to_buy = 0.2 * affordable
        elif risk == "LOW":
            to_buy = affordable
        else:
            to_buy = 0.4 * affordable
        return to_buy

    def determineHowManyToSell(self, risk: str, bitcoin: float) -> float:
        """Returns best amount of bitcoin to sell"""
        to_sell = 0
        if risk == "HIGH":
            to_sell = bitcoin
        elif risk == "LOW":
            to_sell = 0.2 * bitcoin
        else:
            to_sell = 0.4 * bitcoin
        return to_sell

    def sellAction(self, bitcoin: float, risk: str) -> None:
        """Prints sell USDT_BTC {currency} to stdout"""
        if bitcoin == 0:
            self.passAction()
            return
        value = self.determineHowManyToSell(risk, bitcoin)
        if value > bitcoin:
            value = bitcoin
        if value == 0:
            self.passAction()
            return
        print(f"sell USDT_BTC {value}", flush=True)

    def buyAction(self, affordable: float, risk: str) -> None:
        """Prints buy USDT_BTC {currency} to stdout"""
        if affordable == 0:
            self.passAction()
            return
        value = self.determineHowManyToBuy(affordable, risk)
        if value > affordable:
            value = affordable
        if value == 0:
            self.passAction()
            return
        print(f"buy USDT_BTC {value}", flush=True)
