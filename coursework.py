class Command: #abstract class
    def do(self):
        pass
    def undo(self):
        pass
class GenerateAccountNumber:
#only one generator allowed (Singleton pattern) and it produces a 14 char (numerals) string
#in the real world, the generator would be more sophisticated
    _instance = None
    def __new__(cls) -> str:
class AccountNumber:
    def __init__(self):
#generates account number. Raises exception if not valid
    def _is_valid(self, account_number:str) -> bool:
#validates that account number has 11-14 digits
    def id(self) -> str: #object return value
#return account number (private attribute)
class Account:pass
class Currency:
    def __init__(self, amount:int):
#takes in amount and validates that it is an appropriate value
    def _is_valid_amount(self, amount:int) -> bool:
#validates that amount is an int and positive
    def value(self):
#returns value (private attribute)
'''We have here a chain of trust:
-we trust that Currency and AccountNumber are able to sanitise untrusted data
-classes that only evoke the above do not need to sanitise anything passed to them, they only need to verify class type
-BankTransaction class implements the Command pattern'''
class Account:
'''Account object performs checks on its own account number and balance transfers.
BTs are logged, but not committed until commit method is called'''
    def __init__(self):
        self._account_number = AccountNumber().id()
        self._balance = 0
        self._log = []
    def id(self):
    #returns account number (private attribute)def _is_valid_account(self, account:Account) -> bool:
    #returns True if valid account
    def _is_valid_currency(self, currency:Currency) -> bool:
    #returns True if valid currency
    #class Account
    def transfer_in(self, currency:Currency, source:Account, destination:Account):
    #check valid source and destination
    #check valid currency
    #if all valid, log transfer in
    def transfer_out(self, currency:Currency, source:Account, destination:Account):#check valid BT and transfer source
    #check valid source and destination
    #check valid currency
    #if all valid, log transfer out
    #class Account
    def commit(self):
    #Balance transfers (in/ out) are logged, but don't actually happen until subject to a commit
    def uncommit(self):
    #uncommit attempts to roll back a commit (invoked if a problem occurs with a commit)def clear_commit_log(self):
    #clears commit log when requested (after a successful commit – i.e. not rolled back)
class ReserveAccount(Account):
    '''Singleton pattern ensures that there will only ever be a single reserve account.
    The reserve account it unique in that it's balance can be set or added to directly
    (i.e. the money can be transferred in from nowhere. All other accounts require you
    to transfer money from a know account'''
    _instance = None
    def __new__(cls):
    #initialise and return single instance
    def __init__(self):
    pass
    def add_balance(self, currency:Currency):
    #checks valid currency and adds to balance
    #commit log not used because this is a side channel to introduce starting capital
class BankTransaction(Command):
    '''BankTransaction attempts to perform an atomic transaction.
    An atomic transaction is a balance transfer between two account that is undone
    ('rolled back') if a problem occurs. This rollback is implemented using the Command pattern'''
    def __init__(self, source_account:Account, destination_account:Account, currency:Currency):#no need to validate: validation performed at an account level
        self._source_account = source_account
        self._destination_account = destination_account
        self._currency = currency
        self._source_commit = False
        self._destination_commit = False
    #class BankTransaction
    def do(self):
    #commit transaction
    def undo(self):
    #uncommit
    self._clear_commit_log()
    def _clear_commit_log(self):
    #clear any commit logs