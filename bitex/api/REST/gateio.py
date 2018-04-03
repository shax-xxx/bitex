"""Gate.io REST API backend.

Documentation available here:
    https://gateio.io/api2
"""
# Import Built-ins
import logging
import hashlib
import hmac
import warnings
import time,urllib
# Import Third-Party

# Import Homebrew
from bitex.api.REST import RESTAPI
from bitex.exceptions import IncompleteCredentialsError
from bitex.exceptions import IncompleteCredentialConfigurationWarning

log = logging.getLogger(__name__)


class GateioREST(RESTAPI):
    """Gateio REST API class."""

    def __init__(self, addr=None, user_id=None, key=None, secret=None, version=None, timeout=5, config=None):
        """Initialize the class instance."""
        addr = addr or 'https:/'
        super(GateioREST, self).__init__(addr=addr, version=version,
                                           key=key, secret=secret,
                                           timeout=timeout, config=config)

    def check_auth_requirements(self):
        """Check if authentication requirements are met."""
        try:
            super(GateioREST, self).check_auth_requirements()
        except IncompleteCredentialsError:
            raise

        #if self.user_id is None: # if need user_id, remove #
        #    raise IncompleteCredentialsError

    def load_config(self, fname):
        """Load configuration from a file."""
        conf = super(GateioREST, self).load_config(fname)
        try:
            self.user_id = conf['AUTH']['user_id']
        except KeyError:
            if self.user_id is None:
                warnings.warn("'user_id' not found in config!",
                              IncompleteCredentialConfigurationWarning)
        return conf

    def getSign(self, params, secretKey):
        bSecretKey = bytes(secretKey, encoding='utf8')

        sign = ''
        for key in params.keys():
            value = str(params[key])
            sign += key + '=' + value + '&'
        bSign = bytes(sign[:-1], encoding='utf8')

        mySign = hmac.new(bSecretKey, bSign, hashlib.sha512).hexdigest()
        return mySign

    def sign_request_kwargs(self, endpoint, **kwargs):
        """Sign the request."""
        req_kwargs = super(GateioREST, self).sign_request_kwargs(endpoint, **kwargs)

        # Parameters go into headers & data, so pop params key and generate signature
        params = req_kwargs.pop('params')

        # Update headers and data
        req_kwargs['headers'] = {
            "Content-type": "application/x-www-form-urlencoded",
            "KEY": self.key,
            "SIGN": self.getSign(params,self.secret)
            }
        #req_kwargs['data'] = params

        return req_kwargs
