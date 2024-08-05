if __name__ == "__main__":
    main_bank_account = ReserveAccount()
    account1 = Account()
    account2 = Account()
    main_bank_account.add_balance(Currency(100000))
    transaction1 = Account() #Should transactions be of the Account type?
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
