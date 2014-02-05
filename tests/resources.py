import random

from . import settings

from mangopay.api import MangopayAPI

handler = MangopayAPI(settings.API_CLIENT_ID,
                      settings.API_PASSPHRASE,
                      sandbox=settings.API_USE_SANDBOX,
                      host=settings.API_HOST)

from mangopay.resources import *  # noqa @UnusedWildImport


def get_bank_account():
    return settings.API_BANK_ACCOUNTS[random.randint(0,len(settings.API_BANK_ACCOUNTS) - 1)]  # @IgnorePep8
