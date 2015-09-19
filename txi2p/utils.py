from twisted.internet.endpoints import clientFromString

from txi2p.sam import api as samApi


DEFAULT_ENDPOINT = {
    'BOB': 'tcp:127.0.0.1:2827',
    'SAM': 'tcp:127.0.0.1:7656',
    }

DEFAULT_API = 'SAM'

def getApi(api, apiEndpoint, apiDict):
    if not api:
        if apiEndpoint:
            raise ValueError('api must be specified if apiEndpoint is given')
        else:
            api = DEFAULT_API

    if api not in apiDict:
        raise ValueError('Specified I2P API is invalid or unsupported')

    if not apiEndpoint:
        apiEndpoint = DEFAULT_ENDPOINT[api]

    return (api, apiEndpoint)


_apiGenerators = {
    'SAM': samApi.generateDestination,
}

def generateDestination(reactor, keyfile, api=None, apiEndpoint=None):
    """Generate a new I2P Destination.

    The function returns a :class:`twisted.internet.defer.Deferred`; register
    callbacks to receive the return value or errors.

    Args:
        keyfile (str): Path to a local file where the keypair for the new
            Destination should be stored.
        api (str): The API to use.
        apiEndpoint (twisted.internet.interfaces.IStreamClientEndpoint): An
            endpoint that will connect to the API.

    Returns:
        txi2p.I2PAddress: The new Destination. Once this is received via the
        Deferred callback, the ``keyfile`` will have been written.

    Raises:
        ValueError: if the API doesn't support this method.
        ValueError: if the ``keyfile`` already exists.
        IOError: if the ``keyfile`` write fails.
    """
    api, apiEndpoint = getApi(api, apiEndpoint, _apiGenerators)
    if isinstance(apiEndpoint, str):
        apiEndpoint = clientFromString(reactor, apiEndpoint)
    return _apiGenerators[api](keyfile, apiEndpoint)
