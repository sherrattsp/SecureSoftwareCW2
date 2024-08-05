if __name__ == "__main__":
	main_bank_account = ReserveAccount()
	account1 = Account()
	account2 = Account()
	main_bank_account.add_balance(Currency(100000))
	transfer1 = BankTransaction(main_bank_account, account1, Currency(500))
	try:
		transfer1.do()
	except Exception as msg:
		print(msg)
		transfer1.undo()