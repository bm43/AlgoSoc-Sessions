'''
A momentum strategy with some risk measures.
Uses the signal from the simple MACD and implements
a static stop loss and take profit on top.
'''

from pedlar.agent import Agent
from Agents.signal import Signal
from collections import deque
import numpy as np


class SimpleRiskMACDAgent(Agent):
    name = "Simple_Risk_MACD"

    def __init__(self,
                 stop_loss_scaling,
                 take_profit_scaling,
                 fast_length, slow_length,
                 verbose=False, make_order=True, **kwargs):
        super().__init__(**kwargs)
        self.init_tests(fast_length, slow_length,
                        stop_loss_scaling, take_profit_scaling)

        self.take_profit_scaling = take_profit_scaling
        self.stop_loss_scaling = stop_loss_scaling
        self.fast = deque(maxlen=fast_length)
        self.slow = deque(maxlen=slow_length)
        self.verbose = verbose
        self.make_order = make_order
        self.signal = Signal(False, None, None)

        self.last_spread = None
        self.last_mid = None
        self.last_signal = 0
        self.last_order = -1

    def init_tests(self, fast_length, slow_length,
                   stop_loss_scaling, take_profit_scaling):
        assert fast_length < slow_length, "Fast length must be less than slow length."
        assert stop_loss_scaling > 1.0, "Stop scaling must be large than 1 or else it will instantly close positions."
        assert take_profit_scaling > 0.0, "Take profit must be greater than zero or else it will never make a profit."

    def on_tick(self, bid, ask, time=None):
        """Called on every tick update."""
        mid = (bid + ask) / 2
        spread = ask - bid
        if self.last_mid is None:
            self.last_mid = mid
            self.last_spread = spread
            return
        if self.verbose:
            print(f'Tick: {mid: .05f}, {time}')

        signal = self.set_macd_signal(mid)

        is_new_signal = np.sign(signal) != np.sign(self.last_signal)
        if is_new_signal:
            if self.verbose:
                print(f"New signal: {signal}, {self.last_signal}")
            self.order(signal)
        else:
            signal = 0

        self.check_take_profit_stop_loss(bid, ask)
        self.last_mid = mid
        self.last_spread = spread
        self.last_signal = signal

    def set_macd_signal(self, mid):
        ret = mid-self.last_mid
        self.fast.append(ret)
        self.slow.append(ret)
        slow_mean = np.mean(self.slow)
        fast_mean = np.mean(self.fast)
        signal = fast_mean - slow_mean
        return signal

    def order(self, signal):
        if signal > 0:
            self._buy()
        elif signal < 0:
            self._sell()

    def check_take_profit_stop_loss(self, bid, ask):
        if self.orders:
            o = self.orders[self.last_order]
            diff = bid - o.price if o.type == "buy" else o.price - ask
            if self.verbose:
                print(f"Gross profit: {diff: .05f}")
            if diff > (self.take_profit):
                if self.verbose:
                    print(f"Take profit: \
                        {diff: .05f} > {self.take_profit: .05f}")
                self._close()
                return
            if diff < (self.stop_loss):
                if self.verbose:
                    print(f"Stop loss: \
                        {diff: .05f} < {self.stop_loss: .05f}")
                self._close()
                return

    def on_order(self, order):
        """Called on placing a new order."""
        self.last_order = order.id
        self.on_order_update()
        if self.verbose:
            print("New order:", order)
            print("Orders:", self.orders)  # Agent orders only
            print(f"Order detected; take profit: {self.take_profit: .05f}, stop loss: {self.stop_loss: .05f}")

    def on_order_update(self):
        self.stop_loss = -self.last_spread * self.stop_loss_scaling
        self.take_profit = self.last_spread * self.take_profit_scaling

    def on_order_close(self, order, profit):
        """Called on closing an order with some profit."""
        if self.verbose:
            print("Order closed", order, profit)
            print("Current balance:", self.balance)  # Agent balance only

    def _buy(self, *args, **kwargs):
        '''Overloading the Agent.buy function to add our signal update'''
        if self.make_order:
            self.buy(*args, **kwargs)
        self.signal.open("buy")

    def _sell(self, *args, **kwargs):
        '''Overloading the Agent.sell function to add our signal update'''
        if self.make_order:
            self.sell(*args, **kwargs)
        self.signal.open("sell")

    def _close(self, *args, **kwargs):
        '''Overloading the Agent.close function to add our signal update'''
        if self.make_order:
            self.close(*args, **kwargs)
        self.signal.close()


def main(stop_loss_scaling=2, take_profit_scaling=1.5,
         fast_length=120, slow_length=250,
         verbose=True, backtest=None):
    if backtest is None:
        agent = SimpleRiskMACDAgent(stop_loss_scaling=stop_loss_scaling,
                                    take_profit_scaling=take_profit_scaling,
                                    fast_length=fast_length,
                                    slow_length=slow_length,
                                    verbose=verbose,
                                    username='joe', password='1234',
                                    ticker='tcp://icats.doc.ic.ac.uk:7000',
                                    endpoint='http://icats.doc.ic.ac.uk')
    else:
        agent = SimpleRiskMACDAgent(stop_loss_scaling=stop_loss_scaling,
                                    take_profit_scaling=take_profit_scaling,
                                    fast_length=fast_length,
                                    slow_length=slow_length,
                                    verbose=verbose,
                                    backtest=backtest)
    agent.run()
