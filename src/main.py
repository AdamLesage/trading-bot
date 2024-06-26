#!/usr/bin/python3
# -*- coding: iso-8859-1 -*
""" Python starter bot for the Crypto Trader games, from ex-Riddles.io """
__version__ = "1.0"

import sys
from MACD import MACD
from RSI import RSI
from BollingerBands import BollingerBands
from BotAction import BotAction
from ActionState import Action_state
from Limit import Limit
from RiskIndicator import RiskIndicator
from BotState import BotState
from CandlePatern import CandlePatern

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.rsi = RSI(13)
        self.botAction = BotAction()
        self.macd = MACD(6, 13, 9)
        self.limit = Limit(1.2, 0.925)
        self.risk = RiskIndicator(13)
        self.bollinger = BollingerBands(13, 2)
        self.candlePatern = CandlePatern()

    def run(self):
        while True:
            reading = input()
            if len(reading) == 0:
                continue
            if reading == "quit":
                exit(0)
            self.parse(reading)

    def parse(self, info: str):
        tmp = info.split(" ")
        if tmp[0] == "settings":
            self.botState.update_settings(tmp[1], tmp[2])
        if tmp[0] == "update":
            if tmp[1] == "game":
                self.botState.update_game(tmp[2], tmp[3])
        if tmp[0] == "action":
            bitcoin = self.botState.stacks["BTC"]
            current_closing_price = self.botState.charts["USDT_BTC"].closes[-1]
            if self.botState.isAboveFeeToSell == True:
                self.botState.money_can_spend = self.botState.feeToSell - 1000
            else:
                self.botState.money_can_spend = self.botState.stacks["USDT"]
            self.botState.closing_prices.append(current_closing_price)
            # print(f"{dollars=}, {bitcoin=} current total value: {dollars + bitcoin * current_closing_price}", file=sys.stderr)
            if self.botAction.sellEverything(bitcoin, self.botState.money_can_spend, current_closing_price, self.botState.feeToSell) == True:
                self.limit.update_sell()
                self.botState.isAboveFeeToSell = True

            self.rsi.calculate_rsi(self.botState.closing_prices)
            self.macd.calculate_macd(self.botState.closing_prices)
            self.bollinger.calculate_bollinger_bands(self.botState.closing_prices)
            affordable = self.botState.money_can_spend / current_closing_price

            macd_state = self.macd.get_macd_state(affordable, bitcoin)
            macd_tendency = self.macd.get_macd_tendency()
            rsi_state = self.rsi.get_rsi_state(affordable, bitcoin, self.botAction)
            candle_patern_state = self.candlePatern.useCandlePatern(self.botState.charts["USDT_BTC"], macd_tendency)
            bollinger_state = self.bollinger.get_bollinger_state(self.botState.closing_prices[-1])
            if candle_patern_state == Action_state.BUY:
                self.botAction.buyAction(affordable, self.risk.get_risk_state(self.botState.closing_prices))
                return
            elif candle_patern_state == Action_state.SELL and bitcoin >= 0.001:
                self.botAction.sellAction(bitcoin, self.risk.get_risk_state(self.botState.closing_prices))
                return

            # print(f"{bollinger_state=}", file=sys.stderr)

            if self.limit.loss_limit(self.botState.closing_prices[-1]):
                self.botAction.sellAction(bitcoin, self.risk.get_risk_state(self.botState.closing_prices))
                self.limit.update_sell()
                return

            # print(f"rsi: {rsi_state} macd: {macd_state}", file=sys.stderr)
            # print(f"risk indicator: {self.risk.get_risk_state(self.botState.closing_prices)}, current price: {current_closing_price}", file=sys.stderr)
            # if macd_state == Action_state.BUY:
            #     self.botAction.buyAction(affordable, self.risk.get_risk_state(self.botState.closing_prices))
            #     self.limit.update_limit_buy(self.botState.closing_prices[-1])
            #     return
            # elif macd_state == Action_state.SELL :
            #     self.botAction.sellAction(bitcoin, self.risk.get_risk_state(self.botState.closing_prices))
            #     self.limit.update_sell()
            #     return

            self.botAction.passAction()

if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
