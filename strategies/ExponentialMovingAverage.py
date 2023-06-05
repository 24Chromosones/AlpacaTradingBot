import backtrader as bt
import yfinance as yf

class ExponentialMovingAverage(bt.Indicator):
    lines = ('ema',)

    def __init__(self, period):
        self.params.period = period  # Set the desired period
        super(ExponentialMovingAverage, self).__init__()


    def next(self):


        if len(self) < self.params.period:  # Wait until enough data points are available
            return

        if len(self) == self.params.period or len(self) == self.params.period + 1:
            self.lines.ema[0] = sum(self.data.get(size=self.params.period)) / self.params.period

        else:
            alpha = 2 / (self.params.period + 1)
            self.lines.ema[0] = alpha * self.data.close[0] + (1 - alpha) * self.lines.ema[-1]




class EMAStrategy(bt.Strategy):
    def __init__(self):
        self.ema = ExponentialMovingAverage(period=10)

    def next(self):
        if self.data.close[0] > self.ema[0]:
            self.buy()
        elif self.data.close[0] < self.ema[0]:
            self.sell()


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.addstrategy(EMAStrategy)
    cerebro.broker.setcash(100000)

    data = bt.feeds.PandasData(dataname=yf.download('SPY', '2010-01-01', '2022-01-01'))  # Replace with your data feed
    cerebro.adddata(data)

    cerebro.run()
    cerebro.plot()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())