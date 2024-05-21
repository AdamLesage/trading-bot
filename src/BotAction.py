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

    def determineHowManyToBuy(self, closing_prices: list, affordable: float) -> float:
        """Returns best amount of bitcoin to buy from the current closing prices"""
        to_buy = 0
        mean_close = sum(closing_prices) / len(closing_prices)
        standard_deviation = (sum([(x - mean_close) ** 2 for x in closing_prices]) / len(closing_prices)) ** 0.5
        if closing_prices[-1] < mean_close - standard_deviation: # current price is below the mean - standard deviation so buy more
            to_buy = 3 * affordable
        elif closing_prices[-1] > mean_close + standard_deviation: # current price is above the mean + standard deviation so buy less
            to_buy = 0.2 * affordable
        elif closing_prices[-1] < mean_close: # current price is below the mean so buy more
            to_buy = 0.8 * affordable
        else: # current price is above the mean so buy less
            to_buy = 0.4 * affordable
        return to_buy

    def determineHowManyToSell(self, closing_prices: list, bitcoin: float) -> float:
        """Returns best amount of bitcoin to sell"""
        to_sell = 0
        mean_close = sum(closing_prices) / len(closing_prices)
        standard_deviation = (sum([(x - mean_close) ** 2 for x in closing_prices]) / len(closing_prices)) ** 0.5
        if closing_prices[-1] < mean_close - standard_deviation: # current price is below the mean - standard deviation so sell less
            to_sell = 0.2 * bitcoin
        elif closing_prices[-1] > mean_close + standard_deviation: # current price is above the mean + standard deviation so sell more
            to_sell = 3 * bitcoin
        elif closing_prices[-1] < mean_close: # current price is below the mean so sell less
            to_sell = 0.4 * bitcoin
        else: # current price is above the mean so sell more
            to_sell = 0.8 * bitcoin
        return to_sell

    def sellAction(self, closing_prices: list, bitcoin: float) -> None:
        """Prints sell USDT_BTC {currency} to stdout"""
        if bitcoin == 0:
            self.passAction()
            return
        value = self.determineHowManyToSell(closing_prices, bitcoin)
        if value > bitcoin:
            value = bitcoin
        print(f"sell USDT_BTC {value}", flush=True)

    def buyAction(self, closing_prices: list, affordable: float, bitcoin: float) -> None:
        """Prints buy USDT_BTC {currency} to stdout"""
        if affordable == 0:
            self.passAction()
            return
        value = self.determineHowManyToBuy(closing_prices, affordable)
        if value > affordable:
            value = affordable
        print(f"buy USDT_BTC {value}", flush=True)
