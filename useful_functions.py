def get_valid_input_text(text):
    """Check that text inputs are valid"""
    while True:
        try:
            user_input = input(text).lower()
            if user_input == "yes":
                return True
            elif user_input == "no":
                return False
            else:
                print("\nTypo Error, please type 'yes' or 'no'")
        except Exception as e:
            print(f"\nAn error occurred: {e}, please enter 'yes' or 'no'")

def get_valid_balance(bank_amount_text):
    """Check that balance inputs are valid"""
    while True:
        try:
            balance = int(float(input(bank_amount_text)))
            if balance <= 0:
                print("\nThe bid must be a positive number. Please try again.")
            else:
                print(f"\nYour amount of ${balance} is accepted.")
                return balance
        except Exception as e:
            print(f"\nAn error occurred: {e}, please enter a valid amount")

def get_valid_bid(balance, bid_amount_text):
    """Check that bid inputs are valid"""
    while True:
        try:
            bid_check = int(float(input(bid_amount_text)))
            if bid_check <= 0:
                print("\nThe bid must be a positive number. Please try again.")
            elif bid_check > balance :
                print(f"\nYou cannot bid more than your bank amount (${balance}). Try again.")
            else:
                print(f"\nYour bid of ${bid_check} is accepted.")
                return bid_check 
        except Exception as e:
            print(f"\nAn error occurred: {e}, please enter a valid amount")
