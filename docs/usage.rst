.. _ref-usage:

=====
Usage
=====

Creating a handler
------------------

To manipulate resources (Users, Wallets, etc.) from this api you will have to
instanciate a new handler which is basically a connection authentification.

To create a new handler, you have to provide several parameters.

``API_CLIENT_ID``
..................

This is the client identifier used by mangopay_ to identify you.

``API_PASSPHRASE``
...................

This is the passphrase used in each requests.

``API_HOST``
............

The host used to call the API. We will see later
when you are creating a new handler you can choose between
multiple environment hosts already registered.

Let's get to work, we will create our first handler with the sandbox host ::

    client_id = 'dummy'
    passphrase = '$ecret'

    from mangopay.api import MangopayAPI

    handler = MangopayAPI(client_id,
                          passphrase,
                          sandbox=True)

Now we have a new handler which is using the `sandbox host`_.

If you are not specifying that you are using the `sandbox host`_
nor an existing host, it will use the `production host`_.

Specific host for mangopay_ endpoint ::

    handler = MangopayAPI(client_id,
                          passphrase,
                          host='http://dummy.api.prod.mangopay.com')

Using resources
---------------

To manipulate resources, this library is heavily inspired from peewee_,
so every operations will be like manipulating a ORM.
In fact, python-mangopay is a port of python-leetchi

For required parameters you have to refer to the `reference api`_.

Users
.....

Creating a new natural user ::

    from mangopay.resources import NaturalUser
    from datetime import date
    user = NaturalUser(first_name='Stephane',
                       last_name='Planquart',
                       email='stephane@test.test',
                       ip_address='127.0.0.1',
                       nationality='FR',
                       birthday=date.today(),
                       country_of_residence='fr')

    user.save(handler) # save the new user

    print user.get_pk() # retrieve the primary key

Retrieving an existing user ::

    user = NaturalUser.get(1)

    print user.first_name # Stephane

Detecting user that does not exist ::

    try:
        user = NaturalUser.get(2, handler)
    except NaturalUser.DoesNotExist:
        print 'The user 2 does not exist'

Wallets
.......

Affecting a wallet to an existing user ::

    user = NaturalUser.get(1, handler)

    from mangopay.resources import Wallet

    wallet = Wallet(tag='wallet for user n.1',
                    name='Stephane Planquart wallet',
                    description='A new wallet for Stephane Planquart',
                    currency='EUR',
                    owners=[user])
    wallet.save(handler) # save the new wallet

    print wallet.get_pk() # 1

Retrieving all wallets for an existing user ::

    user = User.get(1, handler)

    wallet_list = user.wallet_set

Payin
.....

A pay-in is a way to put money on a wallet.

Creating a new pay-in for a dedicated wallet ::

    from mangopay.resources import Payin, Wallet, NaturalUser

    user = NaturalUser.get(1, handler)
    wallet = Wallet.get(1, handler)

    payin = Payin(author=user,
                  credited_wallet_id=wallet.id,
                  debited_funds=(200, 'EUR'),
                  fees=(4, 'EUR'),
                  return_url='http://www.google.fr',
                  culture='fr')
    payin.save(handler)

    print payin.is_success() # False

Use template_url ::

    from mangopay.resources import Payin, Wallet, NaturalUser

    user = NaturalUser.get(1, handler)
    wallet = Wallet.get(1, handler)

    payin = Payin(author=user,
                  credited_wallet_id=wallet.id,
                  debited_funds=(200, 'EUR'),
                  fees=(4, 'EUR'),
                  return_url='http://www.google.fr',
                  culture='fr',
                  template_url_options=('https://www.mysite.com/templatePayline', 
                                        'https://www.mysitecom/templateOgone'))
    payin.save(handler)

    print payin.is_success() # False

Refunds
.......

If you want to refund a payin and move back the money from
a wallet to a credit card account ::

    from mangopay.resources import Payin, User, Refund

    user = NaturalUser.get(1, handler)
    payin = Payin.get(1, handler)

    refund = Refund(initial_transaction=payin,
                    author=user)
    refund.save(handler)

Transfers
.........

Creating a transfer from a personal wallet to another wallet ::

    from mangopay.resources import User, Transfer, Wallet

    user = NaturalUser.get(1, handler)

    origin_wallet = Wallet.get(2, handler)

    beneficiary_wallet = Wallet.get(3, handler)

    transfer = Transfer(author=user,
                        cretited_wallet=beneficiary_wallet,
                        debited_wallet=origin_wallet,
                        debited_funds=(100, 'EUR'),
                        fees=('2', 'EUR'))
    transfer.save(handler)

    print transfer.get_pk() # 1

    print beneficiary_wallet.credited_funds # 98

Payout
......

If you want to transfer funds on a bank account you must create a Payout ::

    from mangopay.resources import NaturalUser, Payout, BankAccount

    user = NaturalUser.get(1, handler)

    bank_account = BankAccount.get(1547373,
                                   handler,
                                   resource_model=user)

    bank_transfer = Payout(author=user,
                           debited_wallet=wallet,
                           debited_funds=(20,'EUR'),
                           fees=(1,'EUR'),
                           bank_account=bank_account)

    bank_transfer.save(handler)

    print bank_transfer.get_pk() # 1

BankAccount
...........

For create a BankAccount ::

    from mangopay.resources import NaturalUser, BankAccount

    bank_account = BankAccount(user=user,
                               owner_name='Stephane Planquart',
                               owner_address='1 rue de paris, 75006 Paris',
                               iban='FR3020041010124530725S03383',
                               bic='CRLYFRPP')

    bank_account.save(handler)

    print bank_account.get_pk() # 1


For get a BankAccount, don't forget that in MangoPay V2's model, a BankAccount is inside a user.
You must have a User object to get a bank_account ::

    from mangopay.resources import NaturalUser, BankAccount

    user = NaturalUser.get(1, handler)

    bank_account = BankAccount.get(1, handler, resource_model=user)

Transfer refunds
................

If you want to cancel a transfer and move back the money
from one wallet to another ::

    from mangopay.resources import TransferRefund, Transfer, User

    user = User.get(1, handler)
    transfer = Transfer.get(1, handler)

    transfer_refund = TransferRefund(user=user, transfer=transfer)

    wallet = transfer.beneficiary_wallet

    print wallet.collected_amount # 1000
    print wallet.remaining_amount # 0

    print user.personal_wallet_amount # 1000

Operations
..........

Retrieving all operations for a dedicated user ::

    from mangopay.resources import User

    user = User.get(1, handler)

    operation_list = user.operation_set

.. _mangopay: http://www.mangopay.com/
.. _sandbox host: https://api.sandbox.mangopay.com
.. _production https://api.mangopay.com
.. _python-leetchi: https://github.com/thoas/python-leetchi
.. _peewee: https://github.com/coleifer/peewee
.. _reference api: http://www.mangopay.com/api-references/
