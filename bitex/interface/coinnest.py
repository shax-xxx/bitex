"""Coinnest Interface class."""
# pylint: disable=arguments-differ
# Import Built-Ins
import logging

import requests

# Import Homebrew
from bitex.exceptions import UnsupportedPairError
from bitex.api.REST.coinnest import CoinnestREST
from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair, format_with
from bitex.formatters import CoinnestFormattedResponse


# Init Logging Facilities
log = logging.getLogger(__name__)


class Coinnest(RESTInterface):
    """Coinnest REST API Interface Class.

    Since Coinnest doesn't make an explicit differentiation between api versions,
    we do not use a version checker for this interface.
    """

    def __init__(self, **api_kwargs):
        """Initialize the Interface class instance."""
        super(Coinnest, self).__init__('Coinnest', CoinnestREST(**api_kwargs))

    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        pairs=["btc","bch","btg","bcd","ubtc","btn","kst","ltc","act","eth","etc","ada","qtum","xlm","neo","gas","rpx","qlc","hsr","knc","tsl","tron","omg","wtc","mco","storm","gto","npxs","chat","vet","egcc","frec","ink","oc","hlc","ent","qbt","spc","put","hotc"]
        return pairs

    def request(self, endpoint, authenticate=False, **kwargs):
        """Generate a request to the API."""
        verb = 'POST' if authenticate else 'GET'
        return super(Coinnest, self).request(verb, endpoint, authenticate=authenticate, **kwargs)

    ###############
    # Basic Methods
    ###############

    # Public Endpoints

    @check_and_format_pair # Coinnest ticker response all pairs
    @format_with(CoinnestFormattedResponse)
    def ticker(self, pair, *args, **kwargs):
        return self.request('api/pub/ticker?coin=%s' % pair, params=kwargs)

    @check_and_format_pair
    @format_with(CoinnestFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        return self.request('/api/pub/depth?coin=%s' % pair, params=kwargs)

    @check_and_format_pair
    @format_with(CoinnestFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        return self.request('api/pub/trades?coin=%s' % pair, params=kwargs)

    # Private Endpoints
    @check_and_format_pair
    @format_with(CoinnestFormattedResponse)
    def ask(self, pair, price, size, *args, market=False, **kwargs):
        """Place an ask order."""
        return self._place_order(pair, price, size, 'api/trade/add', market=market, **kwargs)

    @check_and_format_pair
    @format_with(CoinnestFormattedResponse)
    def bid(self, pair, price, size, *args, market=False, **kwargs):
        """Place a bid order."""
        return self._place_order(pair, price, size, 'api/trade/add', market=market, **kwargs)

    def _place_order(self, pair, price, size, side, market=None, **kwargs):
        """Place an order with the given parameters."""
        payload = {'amount': size, 'price': price}
        payload.update(kwargs)
        if market:
            return self.request('%s/market/%s/' % (side, pair), authenticate=True, params=payload)
        return self.request('%s/%s/' % (side, pair), authenticate=True, params=payload)

    @format_with(CoinnestFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """Return the order status for the given order's ID."""
        payload = {'id': order_id}
        payload.update(kwargs)
        return self.request('api/order_status/', authenticate=True, params=payload)

    @format_with(CoinnestFormattedResponse)
    def open_orders(self, *args, pair=None, **kwargs):
        """Return all open orders."""
        if pair:
            return self.request('open_orders/%s/' % pair, authenticate=True, params=kwargs)
        return self.request('open_orders/all/', authenticate=True, params=kwargs)

    @format_with(CoinnestFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """Cancel existing order(s) with the given id(s)."""
        results = []
        payload = kwargs
        for oid in order_ids:
            payload.update({'id': oid})
            r = self.request('api/trade/cancel', authenticate=True, params=payload)
            results.append(r)
        return results if len(results) > 1 else results[0]

    @format_with(CoinnestFormattedResponse)
    def wallet(self, *args, **kwargs):
        """Return account's wallet."""
        return self.request('api/account/balance', authenticate=True, params=kwargs)


