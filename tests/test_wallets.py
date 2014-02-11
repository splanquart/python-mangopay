import unittest

from datetime import date

from tests.resources import handler, NaturalUser, Wallet


class WalletsTest(unittest.TestCase):
    def test_create_wallet(self):
        params = {
            'first_name': 'Mark',
            'last_name': 'Zuckerberg',
            'email': 'mark@leetchi.com',
            'ip_address': '127.0.0.1',
            'tag': 'custom_information',
            'nationality': 'FR',
            'birthday': date.today(),
            'country_of_residence': 'FR'
        }

        user = NaturalUser(**params)
        user.save(handler)

        wallet_params = {
            'tag': 'user',
            'name': 'Mark Zuckerberg wallet',
            'description': 'Wallet of Mark Zuckerberg',
            'owners': [user]
        }

        wallet = Wallet(**wallet_params)
        wallet.save(handler=handler)
        print "wallet %r" % wallet.__dict__
        params = dict(wallet_params, **{
            'currency': 'EUR',
            'balance': (0, 'EUR')
        })

        from mangopay.signals import request_started

        def print_infos(signal, **kw):
            print("Before send data : %r" % kw)
        request_started.connect(print_infos)

        for k, v in params.items():
            self.assertEqual(getattr(wallet, k), v)

        w = Wallet.get(wallet.get_pk(), handler)

        for k, v in wallet_params.items():
            self.assertEqual(getattr(w, k), v)

        self.assertEqual(w.get_pk(), wallet.get_pk())

        self.assertEqual(w.users, [user])

    def test_related_wallet(self):
        user = NaturalUser(**{
            'first_name': 'Mark',
            'last_name': 'Zuckerberg',
            'email': 'mark@leetchi.com',
            'ip_address': '127.0.0.1',
            'tag': 'custom_information',
            'nationality': 'FR',
            'birthday': date.today(),
            'country_of_residence': 'FR'
        })
        user.save(handler)

        wallet = Wallet(**{
            'tag': 'user',
            'name': 'Mark Zuckerberg wallet',
            'description': 'Wallet of Mark Zuckerberg',
            'owners': [user]
        })

        wallet.save(handler=handler)

        user = NaturalUser.get(user.get_pk(), handler=handler)

        self.assertEqual(user.wallets, [wallet])
