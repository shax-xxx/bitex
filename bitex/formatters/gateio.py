"""FormattedResponse Class for Standardized methods of the Gateio Interface class."""
# Import Built-ins
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class GateioFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        pair = self.method_args[1]
        data = self.json(parse_int=str, parse_float=str)

        bid = data["highestBid"]
        ask = data["lowestAsk"]
        high = data["high24hr"]
        low = data["low24hr"]
        last = data["last"]
        volume = data["quoteVolume"] #"quoteVolume"
        timestamp = datetime.utcnow()
        return super(GateioFormattedResponse, self).ticker(bid, ask, high, low, last, volume, timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        data = self.json()
        asks=[]
        bids=[]
        for i in data['asks'][::-1]: asks.append([float(i[0]), float(i[1])])
        for i in data['bids']: bids.append([float(i[0]), float(i[1])])
        timestamp = datetime.utcnow()
        return super(GateioFormattedResponse, self).order_book(bids, asks, timestamp)

    def trades(self):
        """Return namedtuple with given data."""
        raise NotImplementedError

    def bid(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(GateioFormattedResponse, self).bid(oid, price, size, side, 'N/A', ts)

    def ask(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(GateioFormattedResponse, self).ask(oid, price, size, side, 'N/A', ts)

    def order_status(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        state = data['status']
        oid = self.method_args[0]
        ts = self.received_at
        return super(GateioFormattedResponse, self).order_status(
            oid, 'N/A', 'N/A', 'N/A', 'N/A', state, ts)

    def cancel_order(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=float)
        extracted_data = (data['id'], True if ('error' in data and data['error']) else False,
                          data['datetime'], data['error'] if 'error' in data else None)
        return super(GateioFormattedResponse, self).cancel_order(*extracted_data)

    def open_orders(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        unpacked_orders = []
        for order in data:
            if order['type']:
                side = 'ask'
            else:
                side = 'bid'
            if 'pair' in self.method_kwargs:
                unpacked_order = (data['id'], self.method_kwargs['pair'], data['price'],
                                  data['amount'], side, data['datetime'])
            else:
                unpacked_order = (data['id'], data['currency_pair'], data['price'], data['amount'],
                                  side, data['datetime'])
            unpacked_orders.append(unpacked_order)

        ts = self.received_at
        return super(GateioFormattedResponse, self).open_orders(unpacked_orders, ts)

    def wallet(self):
        data = self.json(parse_int=str, parse_float=str)['available']
        balances={}
        for i in data:
            if (i=='BTC')|(i=='USD')|(float(data[i])>0):
                balances[i]=float(data[i])
        return super(GateioFormattedResponse, self).wallet(balances, self.received_at)
