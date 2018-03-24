"""FormattedResponse Class for Standardized methods of the CEXio Interface class."""
# Import Built-ins
from datetime import datetime

# Import third-party
import pytz

# Import Home-brewed
from bitex.formatters.base import APIResponse


class CEXioFormattedResponse(APIResponse):
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
        last = data["last"]
        volume = data["volume"]
        timestamp = datetime.utcfromtimestamp(float(data["timestamp"]))

        return super(CEXioFormattedResponse, self).ticker(bid, ask, high, low, last, volume, timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        data=self.json()
        asks=[]
        bids=[]
        for i in data['asks']: asks.append([float(i[0]),float(i[1])])
        for i in data['bids']: bids.append([float(i[0]),float(i[1])])
        return super(CEXioFormattedResponse, self).order_book(bids, asks, int(data['timestamp']))

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
        data = self.json(parse_int=str, parse_float=str)
        data.pop('timestamp')
        data.pop('username')
        balances={}
        for i in data:
            available=float(data[i]['available'])
            if available>0:
                balances[i]=available
        return super(CEXioFormattedResponse, self).wallet(balances, self.received_at)
