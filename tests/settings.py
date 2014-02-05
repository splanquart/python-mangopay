import sys

try:
    from . import credentials
except ImportError as e:
    sys.stderr.write('Error: Can\'t find the file credentials.py')
    raise e

API_CLIENT_ID = getattr(credentials, 'API_CLIENT_ID', 'clientID')
API_PASSPHRASE = getattr(credentials, 'API_PASSPHRASE', '$ecret')
API_USE_SANDBOX = getattr(credentials, 'API_USE_SANDBOX', True)
API_HOST = getattr(credentials, 'API_HOST', None)
API_BANK_ACCOUNTS = getattr(credentials, 'API_BANK_ACCOUNTS', [
    {
        'number': 'XXXXXXXXXXXXXXXX',
        'expiration': {
            'year': 'XX',
            'month': 'XX'
        },
        'cvv': 'XXX'
    },
])
