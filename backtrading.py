from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import yfinance as yf

from strategies.ThreeFallBuy import ThreeFallBuy
from strategies.ExponentialMovingAverage import EMAStrategy
from strategies.DollarCostAvgSpy import DollarCostAvgSPY


class Strategy(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):

        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        print(f'{self.datas}')

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        print(self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:

            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DollarCostAvgSPY)

    # The comment below is meant for PyCharm to ignore the false positive warning code
    # noinspection PyArgumentList
    data = bt.feeds.PandasData(dataname=yf.download('SPY', '2010-01-01', '2023-01-01'))
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.set_shortcash(False)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
