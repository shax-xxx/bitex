"""FormattedResponse Class for Standardized methods of the Coinnest Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class CoinnestFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)

        bid = float(data["buy"])
        ask = float(data["sell"])
        high = float(data["high"])
        low = float(data["low"])
        last = float(data["last"])
        volume = float(data["vol"])
        timestamp = datetime.utcfromtimestamp(float(data["time"]))
        return super(CoinnestFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        data = self.json()
        asks = []
        bids = []
        for i in data['asks']:
            asks.append([float(i[0]), float(i[1])])
        for i in data['bids']:
            bids.append([float(i[0]), float(i[1])])
        timestamp = datetime.utcnow()
        return super(CoinnestFormattedResponse, self).order_book(bids, asks, timestamp)

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

    def open_orders(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def cancel_order(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def wallet(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        balances = {}
        for i in data:
            if i[-8:] == '_balance':
                if (i[:-8] == 'btc') | (i[:-8] == 'krw') | (float(data[i]) > 0):
                    balances[i[:-8].upper()] = float(data[i])
        return super(CoinnestFormattedResponse, self).wallet(balances, self.received_at)
