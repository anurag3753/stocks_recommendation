import pytest
from pathlib import Path
from os import path
import sys

@pytest.fixture(scope="module")
def run_before_all_tests():
    base_path = path.abspath('.')
    sys.path.append(base_path)



def test_bullish_marubozu(run_before_all_tests):
    from indicators.candles.Marubozu import Marubozu
    bullish = Marubozu(971.8, 1030.2, 970.1, 1028.4, "x")
    candle, tr_st = bullish.run()
    assert tr_st['candle'] == 'bullish_marubozu'

def test_incorrect_bullish_marubozu(run_before_all_tests):
    from indicators.candles.Marubozu import Marubozu
    bullish = Marubozu(1734, 1836.55, 1726.6, 1816.7, "x")
    candle, tr_st = bullish.run()
    assert tr_st['candle'] != 'bullish_marubozu'

def test_bearish_marubozu(run_before_all_tests):
    from indicators.candles.Marubozu import Marubozu
    bearish = Marubozu(355.4, 356, 341, 341.7, "x")
    candle, tr_st = bearish.run()
    assert tr_st['candle'] == 'bearish_marubozu'

def test_incorrect_bearish_marubozu(run_before_all_tests):
    from indicators.candles.Marubozu import Marubozu
    bullish = Marubozu(1834, 1863.8, 1774, 1783.1, "x")
    candle, tr_st = bullish.run()
    assert tr_st['candle'] != 'bearish_marubozu'

def test_uptrend_spinning_top(run_before_all_tests):
    from indicators.candles.SpinningTop import SpinningTop
    trend = SpinningTop(210, 230, 188, 207, "x", uptrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "spinning_top_in_uptrend"

def test_downtrend_spinning_top(run_before_all_tests):
    from indicators.candles.SpinningTop import SpinningTop
    trend = SpinningTop(207, 230, 188, 210, "x", downtrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "spinning_top_in_downtrend"

def test_paper_umbrella_hangingman(run_before_all_tests):
    from indicators.candles.PaperUmbrella import PaperUmbrella
    trend = PaperUmbrella(100, 103, 94, 102, "x", uptrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "hangingman"

def test_paper_umbrella_hammer(run_before_all_tests):
    from indicators.candles.PaperUmbrella import PaperUmbrella
    trend = PaperUmbrella(100, 103, 94, 102, "x", downtrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "hammer"

def test_shooting_star(run_before_all_tests):
    from indicators.candles.ShootingStar import ShootingStar
    trend = ShootingStar(1426, 1453, 1410, 1417, "x", uptrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "shooting_star"
