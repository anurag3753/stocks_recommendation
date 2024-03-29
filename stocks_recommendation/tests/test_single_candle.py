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

def test_uptrend_doji(run_before_all_tests):
    from indicators.candles.Doji import Doji
    trend = Doji(210, 230, 188, 207, "x", uptrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "doji_in_uptrend"

def test_downtrend_doji(run_before_all_tests):
    from indicators.candles.Doji import Doji
    trend = Doji(207, 230, 188, 210, "x", downtrend=True)
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "doji_in_downtrend"

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

def test_bullish_harami(run_before_all_tests):
    from indicators.candles.Harami import Harami
    trend = Harami(824,847,818,835,"x", days=5, downtrend=True, previous_day=[868,874,810,815,958])
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "bullish_harami"

def test_bearish_harami(run_before_all_tests):
    from indicators.candles.Harami import Harami
    trend = Harami(126.9,129.70,125,124.80,"x",days=5,uptrend=True,previous_day=[124,129,122,127,958])
    candle, tr_st = trend.run()
    assert tr_st['candle'] == "bearish_harami"

def test_bullish_volume(run_before_all_tests):
    from indicators.Volume import Volume
    trend = Volume(126.9,129.70,125,129.80,4003,"x",avg=400,previous_day=[124,129,122,127,"anyvolume"])
    signal = trend.run()
    assert signal=="bullish"

def test_bearish_volume(run_before_all_tests):
    from indicators.Volume import Volume
    trend = Volume(126.9,129.70,125,126.80,4003,"x",avg=400,previous_day=[124,129,122,127,"anyvolume"])
    signal = trend.run()
    assert signal=="bearish"

def test_bullish_engulfing(run_before_all_tests):
    from indicators.candles.Engulfing import Engulfing
    trend = Engulfing(122,129.70,125,135,"x",downtrend=True,previous_day=[129,129,122,125,"anyvolume"])
    candle, tr_st = trend.run()
    assert tr_st['candle'] =="bullish_engulfing"

def test_bearish_enulfing(run_before_all_tests):
    from indicators.candles.Engulfing import Engulfing
    trend = Engulfing(132,129.70,125,123,"x",uptrend=True,previous_day=[125,133,122,129,"anyvolume"])
    candle, tr_st = trend.run()
    assert tr_st['candle']=="bearish_engulfing"

def test_piercing_pattern(run_before_all_tests):
    from indicators.candles.Engulfing import Engulfing
    trend = Engulfing(122,129.70,125,130,"x",downtrend=True,previous_day=[135,129,122,125,"anyvolume"])
    candle, tr_st = trend.run()
    assert tr_st['candle']=="piercing_pattern"

def test_dark_cloud(run_before_all_tests):
    from indicators.candles.Engulfing import Engulfing
    trend = Engulfing(130,129.70,125,125,"x",uptrend=True,previous_day=[125,133,122,135,"anyvolume"])
    candle, tr_st = trend.run()
    assert tr_st['candle']=="dark_cloud_cover"
