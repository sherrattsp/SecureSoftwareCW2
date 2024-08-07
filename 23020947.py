import sys


class Command:  #abstract class
    def do(self):
        pass

    def undo(self):
        pass


class GenerateAccountNumber:
    #only one generator allowed (Singleton pattern) and it produces a 14 char (numerals) string
    #in the real world, the generator would be more sophisticated
    _instance = None

    def __new__(cls) -> str:
        if cls._instance is None:
            cls._instance = ('0' * (14 - len(str(number))) + str(number) for number in range(0, sys.maxsize))
        return next(cls._instance)


class AccountNumber:
    def __init__(self):
        self._account_number = GenerateAccountNumber()
        if not self._is_valid(self._account_number):
            raise Exception("Invalid account number")

    #generates account number. Raises exception if not valid
    def _is_valid(self, account_number: str) -> bool:
        #validates that account number has 11-14 digits
        return account_number is not None \
            and len(account_number) > 10 \
            and len(account_number) < 15 \
            and account_number.isdigit()

    def id(self) -> str:  #object return value
        #return account number (private attribute)
        return self._account_number


class Account:
    pass


class Currency:
    def __init__(self, amount: int):
        #takes in amount and validates that it is an appropriate value
        if not self._is_valid_amount(amount):
            raise Exception("Incorrect currency value")
        self._value = amount

    def _is_valid_amount(self, amount: int) -> bool:
        #validates that amount is an int and positive
        return isinstance(amount, int) and amount >= 0

    def value(self):
        #returns value (private attribute)
        return self._value


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
        #returns account number (private attribute)
        return self._account_number

    def _is_valid_account(self, account: Account) -> bool:
        #returns True if valid account
        if isinstance(account, Account):
            return True
        else:
            raise Exception(f"Account provided: {account} is not of valid type")

    def _is_valid_currency(self, currency: Currency) -> bool:
        #returns True if valid currency
        if isinstance(currency, Currency):
            return True

    #class Account

    def transfer_in(self, currency: Currency, source: Account, destination: Account):
        #check valid source and destination
        #check valid currency
        #if all valid, log transfer in
        if self._is_valid_account(source) and self._is_valid_account(destination) and self._is_valid_currency(currency):
            self._log.append(BankTransaction(source_account=source, destination_account=destination, currency=currency))

    def transfer_out(self, currency: Currency, source: Account, destination: Account):
        #check valid BT and transfer source
        #check valid source and destination
        #check valid currency
        #if all valid, log transfer out
        #class Account
        if self._is_valid_account(source) and self._is_valid_account(destination) and self._is_valid_currency(currency):
            if source.id() == destination.id():
                raise Exception("Cannot transfer to self")
            self._log.append(BankTransaction(source_account=source, destination_account=destination, currency=currency))
        else:
            raise Exception("Attempted to pass int rather than Currency object")

    def commit(self):
        # BankTransaction.do(self._log[-1])
        if (self._account_number == self._log[-1]._source_account.id()) and (self._willBeNegative(self._log[-1]._currency)):
            raise Exception("Insufficient funds")
        if (self._account_number == self._log[-1]._source_account.id()):
            self._balance -= self._log[-1]._currency.value()
        elif (self._account_number == self._log[-1]._destination_account.id()):
            self._balance += self._log[-1]._currency.value()


        

    def uncommit(self):
        #uncommit attempts to roll back a commit (invoked if a problem occurs with a commit)
        if (self._account_number == self._log[-1]._source_account.id()):
            self._balance += self._log[-1]._currency.value()
        elif (self._account_number == self._log[-1]._destination_account.id()):
            self._balance -= self._log[-1]._currency.value()



    def clear_commit_log(self):
        #clears commit log when requested (after a successful commit – i.e. not rolled back)
        self._log.clear()

    def _willBeNegative(self, currency:Currency) -> bool:
        if (self._balance - currency.value() < 0):
            return True
        else:
            return False


class ReserveAccount(Account):
    '''Singleton pattern ensures that there will only ever be a single reserve account.
    The reserve account it unique in that it's balance can be set or added to directly
    (i.e. the money can be transferred in from nowhere. All other accounts require you
    to transfer money from a know account'''
    _instance = None

    def __new__(cls):
        #initialise and return single instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._account_number = AccountNumber().id()
        self._balance = 0
        self._log = []

    def add_balance(self, currency: Currency):
        #checks valid currency and adds to balance
        #commit log not used because this is a side channel to introduce starting capital
        if self._is_valid_currency(currency):
            self._balance += currency.value()


class BankTransaction(Command):
    '''BankTransaction attempts to perform an atomic transaction.
    An atomic transaction is a balance transfer between two account that is undone
    ('rolled back') if a problem occurs. This rollback is implemented using the Command pattern'''

    def __init__(self, source_account: Account, destination_account: Account, currency: Currency):  #no need to validate: validation performed at an account level
        self._source_account = source_account
        self._destination_account = destination_account
        self._currency = currency
        self._source_commit = False
        self._destination_commit = False

    #class BankTransaction
    def do(self):
        #commit transaction
        # self._source_account._balance -= self._currency.value()
        # self._source_commit = True
        # self._destination_account._balance += self._currency.value()
        # self._destination_commit = True

        self._source_account.transfer_out(self._currency, self._source_account, self._destination_account)
        self._destination_account.transfer_in(self._currency, self._source_account, self._destination_account)
        self._source_account.commit()
        self._source_commit = True
        self._destination_account.commit()
        self._destination_commit = True

        self._clear_commit_log()

    def undo(self):
        if self._source_commit:
            self._source_account.uncommit()
        if self._destination_commit:
            self._destination_account.uncommit()
        self._clear_commit_log()

    def _clear_commit_log(self):
        #clear any commit logs
        self._source_account.clear_commit_log()
        self._destination_account.clear_commit_log()
        self._source_commit = False
        self._destination_commit = False


