##
## EPITECH PROJECT, 2024
## trading-bot
## File description:
## test_MACD
##

# Imports
import sys
sys.path.append("./../src/")
import unittest
from MACD import MACD
from ActionState import Action_state
from TradeTendency import TradeTendency


# tests
class TestMACD(unittest.TestCase):
    def test_calculate_macd(self):
        macd = MACD(3, 5, 2)
        closing_prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        macd.calculate_macd(closing_prices)
        self.assertEqual(macd.macd_line, [-1.25, -1.7916666666666665, -2.1736111111111107, -2.4386574074074074, -2.6205632716049383, -2.7444380144032916, -2.828323259602195, -2.8848977980681294])

    def test_reset_MACD(self):
        macd = MACD(3, 5, 2)
        closing_prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        macd.calculate_macd(closing_prices)
        macd.reset()
        self.assertEqual(macd.macd_line, [])
        self.assertEqual(macd.signal_line, [])
        self.assertEqual(macd.histogram, [])
        self.assertEqual(macd.short_emas, [])
        self.assertEqual(macd.long_emas, [])

    def test_calculate_period_too_short(self):
        macd = MACD(3, 5, 2)
        closing_prices = [1, 2, 3]
        macd.calculate_macd(closing_prices)
        self.assertEqual(macd.signal_line, [None, None, None])
        self.assertEqual(macd.histogram, [None, None, None])

    def test_get_macd_state(self):
        macd = MACD(3, 5, 2)
        closing_prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        macd.calculate_macd(closing_prices)
        self.assertEqual(macd.get_macd_state(0.0, 0.0), Action_state.NEUTRAL)

    def test_get_macd_state_2(self):
        macd = MACD(3, 5, 2)
        self.assertEqual(macd.get_macd_state(0.0, 0.0), Action_state.CALCULATING)

    def test_get_macd_tendency(self):
        macd = MACD(3, 5, 2)
        closing_prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        macd.calculate_macd(closing_prices)
        self.assertEqual(macd.get_macd_tendency(), TradeTendency.UP)


if __name__ == "__main__":
    unittest.main()
