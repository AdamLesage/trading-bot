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


# tests
class TestMACD(unittest.TestCase):
    def test_calculate_macd(self):
        macd = MACD(6, 13, 9)
        closing_prices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        macd.calculate_macd(closing_prices)
        self.assertEqual(macd.macd_line, [])


if __name__ == "__main__":
    unittest.main()
