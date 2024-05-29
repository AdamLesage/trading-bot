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

class Bot:
    def __init__(self):
        self.botState = BotState()
        self.rsi = RSI(13)
        self.botAction = BotAction()
        self.macd = MACD(6, 13, 9)
        self.limit = Limit(1.2, 0.925)
        self.risk = RiskIndicator(13)
        self.bollinger = BollingerBands(13, 2)

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
                self.botState.money_can_spend = self.botState.stacks["USDT"] - 1000
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
            rsi_state = self.rsi.get_rsi_state(affordable, bitcoin, self.botAction)
            bollinger_state = self.bollinger.get_bollinger_state(self.botState.closing_prices[-1])
            # print(f"{bollinger_state=}", file=sys.stderr)

            if self.limit.loss_limit(self.botState.closing_prices[-1]):
                self.botAction.sellAction(bitcoin, self.risk.get_risk_state(self.botState.closing_prices))
                self.limit.update_sell()
                return

            # print(f"rsi: {rsi_state} macd: {macd_state}", file=sys.stderr)
            # print(f"risk indicator: {self.risk.get_risk_state(self.botState.closing_prices)}, current price: {current_closing_price}", file=sys.stderr)
            if macd_state == Action_state.BUY:
                canUpdateLimit = self.botAction.buyAction(affordable, self.risk.get_risk_state(self.botState.closing_prices))
                # if canUpdateLimit:
                #     self.limit.update_limit_buy(self.botState.closing_prices[-1])
                return
            elif macd_state == Action_state.SELL:
                canUpdateLimit = self.botAction.sellAction(bitcoin, self.risk.get_risk_state(self.botState.closing_prices))
                # if canUpdateLimit:
                #     self.limit.update_sell()
                return

            self.botAction.passAction()



class Candle:
    def __init__(self, format, intel):
        tmp = intel.split(",")
        for (i, key) in enumerate(format):
            value = tmp[i]
            if key == "pair":
                self.pair = value
            if key == "date":
                self.date = int(value)
            if key == "high":
                self.high = float(value)
            if key == "low":
                self.low = float(value)
            if key == "open":
                self.open = float(value)
            if key == "close":
                self.close = float(value)
            if key == "volume":
                self.volume = float(value)

    def __repr__(self):
        return str(self.pair) + str(self.date) + str(self.close) + str(self.volume)


class Chart:
    def __init__(self):
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.indicators = {}

    def add_candle(self, candle: Candle):
        self.dates.append(candle.date)
        self.opens.append(candle.open)
        self.highs.append(candle.high)
        self.lows.append(candle.low)
        self.closes.append(candle.close)
        self.volumes.append(candle.volume)


class BotState:
    def __init__(self):
        self.timeBank = 0
        self.maxTimeBank = 0
        self.timePerMove = 1
        self.candleInterval = 1
        self.candleFormat = []
        self.candlesTotal = 0
        self.candlesGiven = 0
        self.initialStack = 0
        self.transactionFee = 0.2
        self.date = 0
        self.stacks = dict()
        self.charts = dict()
        self.closing_prices = []
        self.money_can_spend = 0
        self.isAboveFeeToSell = False
        self.feeToSell = 0
        self.mustCalculateFee = True

    def update_chart(self, pair: str, new_candle_str: str):
        if not (pair in self.charts):
            self.charts[pair] = Chart()
        new_candle_obj = Candle(self.candleFormat, new_candle_str)
        self.charts[pair].add_candle(new_candle_obj)

    def update_stack(self, key: str, value: float):
        if self.mustCalculateFee and key == "USDT":
            self.feeToSell = value + value * 2 # 0.4% fee if fee is 1000 then feeToSell = 1400
            print(f"{self.feeToSell=}", file=sys.stderr)
            self.mustCalculateFee = False
        self.stacks[key] = value

    def update_settings(self, key: str, value: str):
        if key == "timebank":
            self.maxTimeBank = int(value)
            self.timeBank = int(value)
        if key == "time_per_move":
            self.timePerMove = int(value)
        if key == "candle_interval":
            self.candleInterval = int(value)
        if key == "candle_format":
            self.candleFormat = value.split(",")
        if key == "candles_total":
            self.candlesTotal = int(value)
        if key == "candles_given":
            self.candlesGiven = int(value)
        if key == "initial_stack":
            self.initialStack = 2404.97
        if key == "transaction_fee_percent":
            self.transactionFee = float(value)

    def update_game(self, key: str, value: str):
        if key == "next_candles":
            new_candles = value.split(";")
            self.date = int(new_candles[0].split(",")[1])
            for candle_str in new_candles:
                candle_infos = candle_str.strip().split(",")
                self.update_chart(candle_infos[0], candle_str)
        if key == "stacks":
            new_stacks = value.split(",")
            for stack_str in new_stacks:
                stack_infos = stack_str.strip().split(":")
                self.update_stack(stack_infos[0], float(stack_infos[1]))


if __name__ == "__main__":
    mybot = Bot()
    mybot.run()
