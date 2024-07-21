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
            raise Exception("Incorrect value")
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
            self._log.append(BankTransaction(source_account=source, destination_account=destination, currency=currency))
        else:
            raise Exception("Attempted to pass int rather than Currency object")

    def commit(self):
        BankTransaction.do(self._log[-1])

    def uncommit(self):
        #uncommit attempts to roll back a commit (invoked if a problem occurs with a commit)
        BankTransaction.undo(self._log[-1])

    def clear_commit_log(self):
        #clears commit log when requested (after a successful commit – i.e. not rolled back)
        self._log.clear()


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
        self._source_account._balance -= self._currency.value()
        self._source_commit = True
        self._destination_account._balance += self._currency.value()
        self._destination_commit = True

    def undo(self):
        self._source_account._balance += self._currency.value()
        self._source_commit = False
        self._destination_account._balance -= self._currency.value()
        self._destination_commit = False
        self._clear_commit_log()

    def _clear_commit_log(self):
        #clear any commit logs
        self._source_account._log.clear()
        self._destination_account._log.clear()
        self._source_commit = False
        self._destination_commit = False


if __name__ == "__main__":
    main_bank_account = ReserveAccount()
    account1 = Account()
    account2 = Account()
    main_bank_account.add_balance(Currency(100000))
    transaction1 = Account()
    transaction1.transfer_out(Currency(500), main_bank_account, account1)
    transaction1.commit()
    print(f"Value of account one is {account1._balance}")

    transaction2 = Account()
    transaction2.transfer_in(Currency(250), account1, account2)
    transaction2.commit()
    print(f"The value of account two is {account2._balance}")

    badTransaction = Account()
    badTransaction.transfer_out(100, main_bank_account, account1)
    badTransaction.commit()


    # transfer1 = BankTransaction(main_bank_account, account1, Currency(500))
    # try:
    #     transfer1.do()
    # except Exception as msg:
    #     print(msg)
    #     transfer1.undo()
    #
    # intTest = BankTransaction(account1, account2, 45)
    # try:
    #     intTest.do()
    # except Exception as msg:
    #     print(msg)
    #     intTest.undo()
    #     print(f"Value of account one is {account1._balance}")
    #     print(f"The value of account two is {account2._balance}")
    #
    # print(f"Value of account one is {account1._balance}")
    # print(f"The value of account two is {account2._balance}")
