from .base import BaseApiModel

from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     IntegerField, ManyToManyField,
                     ForeignKeyField, AmountField, OneToOneField)

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
    legal_representative_first_name = CharField(api_name='LegalRepresentativeFirstName', required=True)
    legal_representative_last_name = CharField(api_name='LegalRepresentativeLastName', required=True)
    legal_representative_address = CharField(api_name='LegalRepresentativeAddress', required=False)
    legal_representative_email = EmailField(api_name='LegalRepresentativeEmail', required=False)
    legal_representative_birthday = DateField(api_name='LegalRepresentativeBirthday', required=True)
    legal_representative_nationality = CharField(api_name='LegalRepresentativeNationality', required=True)
    legal_representative_country_of_residence = CharField(api_name='LegalRepresentativeCountryOfResidence', required=True)
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
    #amount = AmountField(api_name='Amount')
    is_closed = BooleanField(api_name='IsClosed')

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
    author_id = IntegerField(api_name='AuthorId', required=True)
    debited_funds = AmountField(api_name='DebitedFunds', required=True)
    fees = AmountField(api_name='Fees')
    credited_wallet_id = IntegerField(api_name='CreditedWalletId',
                                      required=True)
    culture = CharField(api_name='Culture')
    card_type = CharField(api_name='CardType')
    secure_mode = CharField(api_name='SecureMode')
    credited_funds = AmountField(api_name='CreditedFunds', required=False)
    credited_user_id = IntegerField(api_name='CreditedUserId', required=False)
    status = CharField(api_name='Status', required=False,
                       choices=STATUS_CHOICES, default=STATUS_CHOICES.created)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type')
    nature = CharField(api_name='Nature')
    payment_type = CharField(api_name='PaymentType')
    execution_type = CharField(api_name='ExecutionType')
    redirect_url = CharField(api_name='RedirectURL', required=False)
    return_url = CharField(api_name='ReturnURL', required=True)
    template_url = CharField(api_name='TemplateURL', required=False)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins/card/web'


# class Beneficiary(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='beneficiaries')
#     bank_account_owner_name = CharField(api_name='BankAccountOwnerName', required=True)
#     bank_account_owner_address = CharField(api_name='BankAccountOwnerAddress', required=True)
#     bank_account_iban = CharField(api_name='BankAccountIBAN', required=True)
#     bank_account_bic = CharField(api_name='BankAccountBIC', required=True)
# 
#     class Meta:
#         verbose_name = 'beneficiary'
#         verbose_name_plural = 'beneficiaries'
# 
# 
# class StrongAuthentication(BaseModel):
#     user = OneToOneField(User, api_name='UserID',
#                          required=True,
#                          related_name='strong_authentication')
#     beneficiary = ForeignKeyField(Beneficiary, api_name='BeneficiaryID')
#     is_transmitted = BooleanField(api_name='IsDocumentsTransmitted')
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
#     message = CharField(api_name='Message')
#     url_request = CharField(api_name='UrlRequest')
# 
#     class Meta:
#         verbose_name = 'strongAuthentication'
#         verbose_name_plural = 'strongAuthentication'
# 
#         urls = {
#             InsertQuery.identifier: lambda params: '/users/%s/strongAuthentication' % params['user_id'],
#             UpdateQuery.identifier: lambda params, reference: '/users/%s/strongAuthentication' % params['user_id']
#         }
# 
# 
# @python_2_unicode_compatible
# class Wallet(BaseModel):
#     name = CharField(api_name='Name', required=True)
# 
#     description = CharField(api_name='Description', required=True)
#     raising_goal_amount = AmountField(api_name='RaisingGoalAmount', required=True)
#     expiration_date = DateTimeField(api_name='ExpirationDate', required=True)
# 
#     spent_amount = AmountField(api_name='SpentAmount')
#     amount = AmountField(api_name='Amount')
#     collected_amount = AmountField(api_name='CollectedAmount')
#     remaining_amount = AmountField(api_name='RemainingAmount')
#     contribution_limit_date = DateTimeField(api_name='ContributionLimitDate')
#     is_closed = BooleanField(api_name='IsClosed')
# 
#     users = ManyToManyField(User, api_name='Owners', related_name='wallets')
# 
#     class Meta:
#         verbose_name = 'wallet'
#         verbose_name_plural = 'wallets'
# 
#     def __str__(self):
#         return self.name
# 
# 
# class PaymentCard(BaseApiModel):
#     id = PrimaryKeyField(api_name='ID')
#     tag = CharField(api_name='Tag', required=True)
#     owner = ForeignKeyField(User, api_name='OwnerID', required=True,
#                             related_name='payment_cards')
#     card_number = CharField(api_name='CardNumber', required=True)
#     redirect_url = CharField(api_name='RedirectURL')
#     return_url = CharField(api_name='ReturnURL', required=True)
#     payment_url = CharField(api_name='PaymentURL')
# 
#     class Meta:
#         verbose_name = 'card'
#         verbose_name_plural = 'cards'
# 
# 
# class Transfer(BaseModel):
#     payer = ForeignKeyField(User, api_name='PayerID', required=True)
#     beneficiary = ForeignKeyField(User, api_name='BeneficiaryID', required=True)
# 
#     amount = AmountField(api_name='Amount', required=True)
# 
#     payer_wallet = ForeignKeyField(Wallet,
#                                    api_name='PayerWalletID',
#                                    related_name='payer_transfers',
#                                    required=True)
#     beneficiary_wallet = ForeignKeyField(Wallet,
#                                          api_name='BeneficiaryWalletID',
#                                          required=True,
#                                          related_name='beneficiary_transfers_set')
# 
#     class Meta:
#         verbose_name = 'transfer'
#         verbose_name_plural = 'transfers'
# 
# 
# class TransferRefund(BaseModel):
#     transfer = ForeignKeyField(Transfer,
#                                api_name='TransferID',
#                                required=True,
#                                related_name='transfer_refunds')
#     user = ForeignKeyField(User,
#                            api_name='UserID',
#                            required=True,
#                            related_name='transfer_refunds')
# 
#     class Meta:
#         verbose_name = 'transfer-refund'
#         verbose_name_plural = 'transfer-refunds'
# 
# 
# class WithdrawalContribution(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='withdrawal_contributions')
#     wallet = ForeignKeyField(Wallet, api_name='WalletID',
#                              related_name='withdrawal_contributions')
#     status = CharField(api_name='Status')
#     amount = AmountField(api_name='Amount')
#     amount_declared = AmountField(api_name='AmountDeclared', required=True)
#     generated_reference = CharField(api_name='GeneratedReference')
#     commentary = CharField(api_name='Commentary')
#     bank_account_owner = CharField(api_name='BankAccountOwner', required=True)
#     bank_account_iban = CharField(api_name='BankAccountIBAN', required=True)
#     bank_account_bic = CharField(api_name='BankAccountBIC', required=True)
# 
#     class Meta:
#         verbose_name = 'contributions-by-withdrawal'
#         verbose_name_plural = 'contributions-by-withdrawal'
# 
# 
# class Contribution(BaseModel):
#     wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
#                              related_name='contributions')
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='contributions')
#     amount = AmountField(api_name='Amount', required=True)
#     client_fee_amount = AmountField(api_name='ClientFeeAmount')
#     leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
#     payment_url = CharField(api_name='PaymentURL')
#     template_url = CharField(api_name='TemplateURL')
#     return_url = CharField(api_name='ReturnURL', required=True)
#     register_mean_of_payment = BooleanField(api_name='RegisterMeanOfPayment')
#     error = CharField(api_name='Error')
#     payment_card = ForeignKeyField(PaymentCard, api_name='PaymentCardID')
#     type = CharField(api_name='Type')  # type of transaction: payline, ogone
#     culture = CharField(api_name='Culture')
#     answer_code = CharField(api_name='AnswerCode')
#     answer_message = CharField(api_name='AnswerMessage')
# 
#     class Meta:
#         verbose_name = 'contribution'
#         verbose_name_plural = 'contributions'
# 
#     def is_success(self):
#         return self.is_succeeded and self.is_completed
# 
# 
# class ImmediateContribution(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='immediate_contributions')
#     wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
#                              related_name='immediate_contributions')
#     amount = AmountField(api_name='Amount', required=True)
#     client_fee_amount = AmountField(api_name='ClientFeeAmount')
#     leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
#     error = CharField(api_name='Error')
#     payment_card = ForeignKeyField(PaymentCard, api_name='PaymentCardID')
#     type = CharField(api_name='Type')
#     answer_code = CharField(api_name='AnswerCode')
#     answer_message = CharField(api_name='AnswerMessage')
#     culture = CharField(api_name='Culture')
# 
#     class Meta:
#         verbose_name = 'immediate-contribution'
#         verbose_name_plural = 'immediate-contributions'
# 
#     def is_success(self):
#         return self.is_succeeded and self.is_completed
# 
# 
# class RecurrentContribution(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='recurrent_contributions')
#     wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
#                              related_name='recurrent_contributions')
#     amount = AmountField(api_name='Amount', required=True)
#     client_fee_amount = AmountField(api_name='ClientFeeAmount')
#     leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
#     is_enabled = BooleanField(api_name='IsEnabled')
#     payment_url = CharField(api_name='PaymentURL')
#     template_url = CharField(api_name='TemplateURL')
#     return_url = CharField(api_name='ReturnURL', required=True)
#     error = CharField(api_name='Error')
#     culture = CharField(api_name='Culture')
#     start_date = DateTimeField(api_name='StartDate', required=True)
#     frequency_code = CharField(api_name='FrequencyCode', required=True)
#     number_of_executions = IntegerField(api_name='NumberOfExecutions', required=True)
# 
#     class Meta:
#         verbose_name = 'recurrent-contribution'
#         verbose_name_plural = 'recurrent-contributions'
# 
#     def is_success(self):
#         return self.is_succeeded and self.is_completed
# 
# 
# class Withdrawal(BaseModel):
#     wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
#                              related_name='withdrawals')
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='withdrawals')
#     amount = AmountField(api_name='Amount', required=True)
#     amount_without_fees = AmountField(api_name='AmountWithoutFees')
#     client_fee_amount = AmountField(api_name='ClientFeeAmount')
#     leetchi_fee_amount = AmountField(api_name='LeetchiFeeAmount')
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
# 
#     bank_account_owner_name = CharField(api_name='BankAccountOwnerName')
#     bank_account_owner_address = CharField(api_name='BankAccountOwnerAddress')
#     bank_account_iban = CharField(api_name='BankAccountIBAN')
#     bank_account_bic = CharField(api_name='BankAccountBIC')
# 
#     beneficiary = ForeignKeyField(Beneficiary, required=True, api_name='BeneficiaryID')
# 
#     error = CharField(api_name='Error')
# 
#     class Meta:
#         verbose_name = 'withdrawal'
#         verbose_name_plural = 'withdrawals'
# 
# 
# class Refund(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='refunds')
#     contribution = ForeignKeyField(Contribution,
#                                    api_name='ContributionID',
#                                    required=True,
#                                    related_name='refunds')
# 
#     is_succeeded = BooleanField(api_name='IsSucceeded')
#     is_completed = BooleanField(api_name='IsCompleted')
# 
#     error = CharField(api_name='Error')
# 
#     class Meta:
#         verbose_name = 'refund'
#         verbose_name_plural = 'refunds'
# 
#     def is_success(self):
#         return self.is_succeeded and self.is_completed
# 
# 
# @python_2_unicode_compatible
# class Operation(BaseModel):
#     user = ForeignKeyField(User, api_name='UserID', required=True,
#                            related_name='operations')
#     wallet = ForeignKeyField(Wallet, api_name='WalletID', required=True,
#                              related_name='operations')
#     amount = AmountField(api_name='Amount', required=True)
# 
#     transaction_type = CharField(api_name='TransactionType')
#     transaction_id = IntegerField(api_name='TransactionID')
# 
#     class Meta:
#         verbose_name = 'operation'
#         verbose_name_plural = 'operations'
# 
#     def __str__(self):
#         return '<Operation n.%s: %s> %d' % (self.transaction_id,
#                                             self.transaction_type,
#                                             self.amount)
