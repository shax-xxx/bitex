"""CEX.IO Interface class."""
# Import Built-Ins
import logging

# Import Third-party
import requests

# Import Homebrew
from bitex.api.REST.cexio import CEXioREST

from bitex.interface.rest import RESTInterface
from bitex.utils import check_and_format_pair, format_with
from bitex.formatters import CEXioFormattedResponse

# Init Logging Facilities
log = logging.getLogger(__name__)


class CEXio(RESTInterface):
    """CEXio REST API Interface Class."""

    def __init__(self, **api_kwargs):
        """Initialize Interface class instance."""
        if 'key' in api_kwargs: key = api_kwargs['key']
        super(CEXio, self).__init__('CEXio', CEXioREST(**api_kwargs))

    def request(self, endpoint, authenticate=False, **req_kwargs):
        """Generate a request to the API."""
        if not authenticate:
            return super(CEXio, self).request('GET', endpoint, authenticate=authenticate,
                                                 **req_kwargs)
        return super(CEXio, self).request('POST', endpoint, authenticate=authenticate,
                                             **req_kwargs)


    def _get_supported_pairs(self):
        """Return a list of supported pairs."""
        r = requests.request('GET', 'https://cex.io/api/currency_limits').json()
        pairs = [item['symbol1']+item['symbol2'] for item in r['data']['pairs']]
        return pairs

    ###############
    # Basic Methods
    ###############
    @format_with(CEXioFormattedResponse)
    @check_and_format_pair
    def ticker(self, pair, *args, **kwargs):
        """Return the ticker for the given pair."""
        return self.request('ticker/%s/%s' % (pair[:-3],pair[-3:]))

    @check_and_format_pair
    @format_with(CEXioFormattedResponse)
    def order_book(self, pair, *args, **kwargs):
        """Return the order book for a given pair."""
        return self.request('order_book/%s/%s' % (pair[:-3],pair[-3:]))

    @check_and_format_pair
    @format_with(CEXioFormattedResponse)
    def trades(self, pair, *args, **kwargs):
        """Return the trades for the given pair."""
        payload = {'market': pair}
        payload.update(kwargs)
        return self.request('trades/', params=payload)

    # Private Endpoints
    @check_and_format_pair
    @format_with(CEXioFormattedResponse)
    def ask(self, pair, price, size, *args, **kwargs):
        """Place an ask order."""
        payload = {'market': pair, 'quantity': size, 'rate': price}
        payload.update(kwargs)
        return self.request('market/selllimit', params=payload, authenticate=True)

    @check_and_format_pair
    @format_with(CEXioFormattedResponse)
    def bid(self, pair, price, size, *args, **kwargs):
        """Place a bid order."""
        payload = {'market': pair, 'quantity': size, 'rate': price}
        payload.update(kwargs)
        return self.request('market/buylimit', params=payload, authenticate=True)

    @format_with(CEXioFormattedResponse)
    def order_status(self, order_id, *args, **kwargs):
        """Return order status of order with given id."""
        payload = {'uuid': order_id}
        payload.update(kwargs)
        return self.request('account/getorder', params=payload, authenticate=True)

    @format_with(CEXioFormattedResponse)
    def open_orders(self, *args, **kwargs):
        """Return all open orders."""
        return self.request('market/getopenorders', params=kwargs, authenticate=True)

    @format_with(CEXioFormattedResponse)
    def cancel_order(self, *order_ids, **kwargs):
        """Cancel order(s) with given ID(s)."""
        results = []
        payload = kwargs
        for uuid in order_ids:
            payload.update({'uuid': uuid})
            r = self.request('market/cancel', params=payload, authenticate=True)
            results.append(r)
        return results if len(results) > 1 else results[0]

    @format_with(CEXioFormattedResponse)
    def wallet(self, *args, currency=None, **kwargs):  # pylint: disable=arguments-differ
        """Return the account wallet."""
        payload = kwargs
        return self.request('balance/', params=payload, authenticate=True)

    ###########################
    # Exchange Specific Methods
    ###########################

    def deposit_address(self, currency, **kwargs):
        """Return the deposit address for given currency."""
        payload = {'currency': currency}
        payload.update(kwargs)
        return self.request('account/getdepositaddress', params=payload, authenticate=True)

    def withdraw(self, **kwargs):
        """Issue a withdrawal."""
        return self.request('account/withdraw', params=kwargs)

    def trade_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's trade history."""
        return self.request('account/getorderhistory', params=kwargs, authenticate=True)

    def withdrawal_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's withdrawal history."""
        return self.request('account/getwithdrawalhistory', params=kwargs)

    def deposit_history(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Return the account's deposit history."""
        return self.request('account/getdeposithistory', params=kwargs)

    def pairs(self, **kwargs):
        """Return the available pairs."""
        return self.request('public/getmarkets', params=kwargs)

    def currencies(self, **kwargs):
        """Return traded currencies."""
        return self.request('public/getcurrencies', params=kwargs)

    def simple_ticker(self, **kwargs):
        """Return a simple ticker for a given pair."""
        return self.request('public/getticker', params=kwargs)
