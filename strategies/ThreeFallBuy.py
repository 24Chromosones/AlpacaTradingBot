import backtrader as bt


class ThreeFallBuy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        print(self.dataclose[0])

        if self.dataclose[0] < self.dataclose[-1]:

            if self.dataclose[-1] < self.dataclose[-2]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()

        if self.dataclose[0] > self.dataclose[-1]:

            if self.dataclose[-1] > self.dataclose[-2]:
                self.log('SELl CREATE, %.2f' % self.dataclose[0])
                self.sell()