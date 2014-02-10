from .base import BaseApiModel

from .fields import (PrimaryKeyField, EmailField, CharField,
                     DateTimeField, DateField,
                     ManyToManyField, TemplateField,
                     ForeignKeyField, AmountField)

from .utils import Choices
from .compat import python_2_unicode_compatible
from .query import InsertQuery, UpdateQuery


class BaseModel(BaseApiModel):
    id = PrimaryKeyField(api_name='Id')
    tag = CharField(api_name='Tag')
    creation_date = DateTimeField(api_name='CreationDate')
    update_date = DateTimeField(api_name='UpdateDate')


@python_2_unicode_compatible
class User(BaseModel):
    email = EmailField(api_name='Email', required=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email


@python_2_unicode_compatible
class NaturalUser(User):
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    address = CharField(api_name='Address', required=False)
    birthday = DateField(api_name='Birthday', required=False)
    nationality = CharField(api_name='Nationality', required=True)
    country_of_residence = CharField(api_name='CountryOfResidence',
                                     required=True)
    occupation = CharField(api_name='Occupation', required=False)
    income_range = CharField(api_name='IncomeRange', required=False)
    proof_of_identity = CharField(api_name='ProofOfIdentity', required=False)
    proof_of_address = CharField(api_name='ProofOfAddress', required=False)

    class Meta:
        verbose_name = 'natural_user'
        verbose_name_plural = 'users/natural'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


@python_2_unicode_compatible
class LegalUser(User):
    LEGAL_PERSON_TYPE_CHOICES = Choices(
        ('BUSINESS', 'business', 'business'),
        ('ORGANIZATION', 'origanization', 'organization')
    )
    name = CharField(api_name='Name', required=True)
    legal_person_type = CharField(api_name='LegalPersonType', required=True,
                                  choices=LEGAL_PERSON_TYPE_CHOICES,
                                  default=LEGAL_PERSON_TYPE_CHOICES.business)
    headquarters_address = CharField(api_name='HeadquartersAddress',
                                     required=False)
    legal_representative_first_name = CharField(api_name='LegalRepresentativeFirstName', required=True)  # noqa @IgnorePep8
    legal_representative_last_name = CharField(api_name='LegalRepresentativeLastName', required=True)  # noqa @IgnorePep8
    legal_representative_address = CharField(api_name='LegalRepresentativeAddress', required=False)  # noqa @IgnorePep8
    legal_representative_email = EmailField(api_name='LegalRepresentativeEmail', required=False)  # noqa @IgnorePep8
    legal_representative_birthday = DateField(api_name='LegalRepresentativeBirthday', required=True)  # noqa @IgnorePep8
    legal_representative_nationality = CharField(api_name='LegalRepresentativeNationality', required=True)  # noqa @IgnorePep8
    legal_representative_country_of_residence = CharField(api_name='LegalRepresentativeCountryOfResidence', required=True)  # noqa @IgnorePep8
    statute = CharField(api_name='Statute', required=False)
    proof_of_registration = CharField(api_name='ProofOfRegistration',
                                      required=False)
    shareholder_declaration = CharField(api_name='ShareholderDeclaration',
                                        required=False)

    class Meta:
        verbose_name = 'legal_user'
        verbose_name_plural = 'users/legal'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Wallet(BaseModel):
    CURRENCY_CHOICES = Choices(
        ('EUR', 'EUR', 'Euros'),
        ('USD', 'USD', 'US Dollar'),
        ('GBP', 'GBP', 'British Pound'),
        ('PLN', 'PLN', 'Zloty'),
        ('CHF', 'CHF', 'Swiss Franc'),
    )
    description = CharField(api_name='Description', required=True)

    currency = CharField(api_name='Currency',
                         choices=CURRENCY_CHOICES,
                         default=CURRENCY_CHOICES.EUR)
    balance = AmountField(api_name='Balance')

    owners = ManyToManyField(User, api_name='Owners', related_name='wallets')

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'

    def __str__(self):
        return self.description


class Payin(BaseModel):
    STATUS_CHOICES = Choices(
        ('CREATED', 'created', 'Created'),
        ('SUCCEEDED', 'succeeded', 'Succeeded'),
        ('FAILED', 'failed', 'Failed')
    )
    SECUREMODE_CHOICES = Choices(
        ('DEFAULT', 'default', 'Default'),
        ('FORCE', 'force', 'Force')
    )
    TYPE_CHOICES = Choices(
        ('PAY_IN', 'pay_in', 'Pay In'),
        ('PAY_OUT', 'pay_out', 'Pay Out'),
        ('TRANSFER', 'transfer', 'Transfer')
    )
    NATURE_CHOICES = Choices(
        ('REGULAR', 'regular', 'Regular'),
        ('REFUND', 'refund', 'Refund'),
        ('REPUDIATION', 'repudiation', 'Repudiation')
    )
    EXECUTION_TYPE_CHOICES = Choices(
        ('WEB', 'web', 'Payin web'),
        ('DIRECT', 'direct', 'Direct Payin')
    )
    author = ForeignKeyField(User, api_name='AuthorId', required=True,
                             related_name='payins')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId',
                                      related_name='payins', required=True)
    credited_user_id = ForeignKeyField(User, api_name='CreditedUserId',
                                       related_name='payins', required=False)
    debited_funds = AmountField(api_name='DebitedFunds', required=True)
    fees = AmountField(api_name='Fees', required=False)
    credited_funds = AmountField(api_name='CreditedFunds', required=False)
    culture = CharField(api_name='Culture')
    card_type = CharField(api_name='CardType', default='CB_VISA_MASTERCARD')
    secure_mode = CharField(api_name='SecureMode',
                            choices=SECUREMODE_CHOICES,
                            default=SECUREMODE_CHOICES.default)
    status = CharField(api_name='Status', required=False,
                       choices=STATUS_CHOICES, default=STATUS_CHOICES.created)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=TYPE_CHOICES)
    nature = CharField(api_name='Nature')
    payment_type = CharField(api_name='PaymentType', choices=NATURE_CHOICES)
    execution_type = CharField(api_name='ExecutionType',
                               choices=EXECUTION_TYPE_CHOICES,
                               default=EXECUTION_TYPE_CHOICES.web)
    redirect_url = CharField(api_name='RedirectURL', required=False)
    return_url = CharField(api_name='ReturnURL', required=True)
    template_url_options = TemplateField(api_name='TemplateURLOptions',
                                         required=False)
    template_url = CharField(api_name='TemplateURL', required=False)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'

        class get_url:
            def __call__(self, params):
                if params['execution_type'] == 'WEB':
                    return '/payins/card/web'
                elif params['execution_type'] == 'DIRECT':
                    return '/payins/card/direct'
                raise Exception('You must define execution_type')

        urls = {
            InsertQuery.identifier: get_url(),
        }

    def is_success(self):
        return self.status == Refund.STATUS_CHOICES.succeeded


class Refund(BaseModel):
    STATUS_CHOICES = Choices(
        ('CREATED', 'created', 'Created'),
        ('SUCCEEDED', 'succeeded', 'Succeeded'),
        ('FAILED', 'failed', 'Failed')
    )
    TRANSACTION_TYPE_CHOICES = Choices(
        ('PAY_IN', 'pay_in', 'Pay In'),
        ('TRANSFER', 'transfer', 'Transfer')
    )

    author = ForeignKeyField(User, api_name='AuthorId',
                             required=True, related_name='refunds')
    initial_transaction = ForeignKeyField(Payin,
                                          api_name='InitialTransactionId',
                                          required=True,
                                          related_name='refunds')
    initial_transaction_type = CharField(api_name='InitialTransactionType',
                                         choices=TRANSACTION_TYPE_CHOICES,
                                         required=False)
    credited_user_id = ForeignKeyField(User, api_name='CreditedUserId',
                                       related_name='payins', required=False)
    debited_funds = AmountField(api_name='DebitedFunds', required=False)
    fees = AmountField(api_name='Fees', required=False)
    credited_funds = AmountField(api_name='CreditedFunds', required=False)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId',
                                      related_name='refund', required=False)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId',
                                     related_name='refund', required=False)
    nature = CharField(api_name='Nature')

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'

        class get_url:
            def __call__(self, params):
                ref_id = params['initial_transaction_id']
                #todo: transfert refund url
                url = '/payins/%s/refunds' % ref_id
                return url
                #return '/transfert/%s/refund' % ref_id

        urls = {
            InsertQuery.identifier: get_url(),
            UpdateQuery.identifier: get_url()
        }

    def is_success(self):
        return self.status == Refund.STATUS_CHOICES.succeeded
