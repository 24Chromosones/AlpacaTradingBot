from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import yfinance as yf


class DollarCostAvgSPY(bt.Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.week = None
        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)

        print('%s, %s' % (dt.isoformat(), txt))

    def update_week(self, new_week):
        if new_week != self.week:
            self.week = new_week
        return True

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.update_week(self.datas[0].datetime.date(0).isocalendar()[1]):
            if self.order:
                if self.order.status == bt.Order.Accepted:
                    print("Order accepted")
                elif self.order.status == bt.Order.Rejected:
                    print("Order rejected")
            self.order = self.buy()

            print(self.broker.get_cash())


def test_spy():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DollarCostAvgSPY)

    # The comment below is meant for PyCharm to ignore the false positive warning code
    # noinspection PyArgumentList
    data = bt.feeds.PandasData(dataname=yf.download('SPY', '2010-01-01', '2022-01-01'))

    # Starting conditions
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()
    cerebro.plot()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
