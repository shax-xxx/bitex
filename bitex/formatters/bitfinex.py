"""FormattedResponse Class for Standardized methods of the Bitfinex Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class BitfinexFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)

        bid = data["bid"]
        ask = data["ask"]
        high = data["high"]
        low = data["low"]
        last = data["last_price"]
        volume = data["volume"]
        timestamp = datetime.utcfromtimestamp(float(data["timestamp"]))

        return super(BitfinexFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        pair = self.method_args[1]
        data = self.json()
        bids = []
        asks = []
        if 'bids' in data: # api version 1
            for i in data['bids']:bids.append([i['price'],i['amount'],i['timestamp']])
            for i in data['asks']:asks.append([i['price'],i['amount'],i['timestamp']])
        else:   # api version 2
            for i in data:
                if float(i[2])>0:
                    bids.append([float(i[0]), float(i[2])])
                else:
                    asks.append([float(i[0]),-float(i[2])])
        timestamp = datetime.utcnow()
        return super(BitfinexFormattedResponse, self).order_book(bids, asks, timestamp)

    def trades(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def ask(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def order_status(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def cancel_order(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def open_orders(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def wallet(self):
        """Return namedtuple with given data."""
        raise NotImplementedError
