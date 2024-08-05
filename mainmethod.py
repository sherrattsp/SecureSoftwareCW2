if __name__ == '__main__':
    #negative balance test
    main_bank_account = ReserveAccount()
    account1 = Account()
    account2 = Account()
    main_bank_account.add_balance(Currency(1000000))
    transfer1 = BankTransaction(main_bank_account, account1, Currency(500))

    try:
        transfer1.do()
    except Exception as msg:
        print(msg)
        transfer1.undo()
    print("Expected for account1: 500, Actual:", account1._balance)
    print("Expected for account2: 0, Actual:", account2._balance)

    transfer2 = BankTransaction(account1, account2, Currency(500))

    try:
        transfer2.do()
    except Exception as msg:
        print(msg)
        transfer2.undo()
    print("Expected for account1: 0, Actual:", account1._balance)
    print("Expected for account2: 500, Actual:", account2._balance)
    try:
        transfer2.do()
    except Exception as msg:
        print(msg)
        transfer2.undo()
    print("Expected for account1: 0, Actual:", account1._balance)
    print("Expected for account2: 500, Actual:", account2._balance)

    account3 = Account()
    account4 = Account()
    transfer3 = BankTransaction(main_bank_account, account3, Currency(500))
    try:
        transfer3.do()
    except Exception as msg:
        print(msg)
        transfer3.undo()
    print("Expected for account3: 500, Actual:", account3._balance)
    print("Expected for account4: 0, Actual:", account4._balance)

    transfer4 = BankTransaction(account4, account3, Currency(500))
    try:
        transfer4.do()
    except Exception as msg:
        print(msg)
        transfer4.undo()
    print("Expected for account3: 500, Actual:", account3._balance)
    print("Expected for account4: 0, Actual:", account4._balance)

    #multilple main account test
    main_bank_account2 = ReserveAccount()
    main_bank_account2.add_balance(Currency(1000000))
    transfer5 = BankTransaction(main_bank_account2, account3, Currency(500))
    try:
        transfer5.do()
    except Exception as msg:
        print(msg)
        transfer5.undo()
    print("Expected for account3: 1000, Actual:", account3._balance)

    print(f"main_bank_account balance: {main_bank_account._balance}, main bank account number: {main_bank_account.id()}")
    print(f"main_bank_account2 balance: {main_bank_account2._balance}, main bank account number: {main_bank_account2.id()}")

    # non-integer currency test
    transfer6 = BankTransaction(account3, account4, Currency(500))

    # large currency test
    transfer7 = BankTransaction(main_bank_account, account4, Currency(100000))
    try:
        transfer7.do()
    except Exception as msg:
        print(msg)
        transfer7.undo()

    print("Expected for account4: 100000, Actual:", account4._balance)
    print("Expected for account3: 1000, Actual:", account3._balance)

    # self transfer test
    transfer8 = BankTransaction(account4, account4, Currency(500))
    try:
        transfer8.do()
    except Exception as msg:
        print(msg)
        transfer8.undo()
    print("Expected for account4: 100000, Actual:", account4._balance)



    # negative transfer test
    transfer9 = BankTransaction(account4, account3, Currency(-500))
    try:
        transfer9.do()
    except Exception as msg:
        print(msg)
        transfer9.undo()
    print("Expected for account4: 100000, Actual:", account4._balance)
    print("Expected for account3: 1000, Actual:", account3._balance)

    #
    #
    # main_bank_account = ReserveAccount()
    # account1 = Account()
    # account2 = Account()
    # main_bank_account.add_balance(Currency(100000))
    # transaction1 = Account()
    # transaction1.transfer_out(Currency(500), main_bank_account, account1)
    # transaction1.commit()
    # print(f"Value of account one is {account1._balance}")
    #
    # transaction2 = Account()
    # transaction2.transfer_in(Currency(250), account1, account2)
    # transaction2.commit()
    # print(f"The value of account two is {account2._balance}")
    #
    # badTransaction = Account()
    # badTransaction.transfer_out(100, main_bank_account, account1)
    # badTransaction.commit()
    #
    #
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
