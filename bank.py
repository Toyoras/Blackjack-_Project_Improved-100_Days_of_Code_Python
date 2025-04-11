class Bank:
    """Manages the player's bank"""
    def __init__(self, balance):
        self.balance = balance

    def refill(self, amount_to_refill):
        """Calculation function to refill the player balance"""
        self.balance += amount_to_refill

    def can_place_bid(self, bid_input):
        """Find out if the bid is higher than the current balance"""
        if bid_input > self.balance:
            return False
        else: 
            return True

    def update_after_win(self, bid_input):
        """Balance update after a win"""
        self.balance += bid_input
        return self.balance

    def update_after_loss(self, bid_input):
        """Balance update after a defeat"""
        self.balance -= bid_input
        return self.balance