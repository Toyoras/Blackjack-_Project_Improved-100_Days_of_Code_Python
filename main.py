# ----- Imports -----
from art import logo
import random
cards_dictionnary = {"A":[1,11],"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

# ----- Classes -----
class Player:
    """Represents a player"""
    def __init__(self, name, is_computer):
        self.hand = []
        self.name = name
        self.is_computer = is_computer

    def draw_initial_cards(self, deck):
        """Draw the first cards"""
        for random_choice in range(2):
            self.hand.append(random.choice(deck))

    def draw_card(self, deck):
        """Draw card function"""
        self.hand.append(random.choice(deck))

    def calculate_score(self):
        """Calculate player scores"""
        score = 0
        for card in self.hand:
            if card != "A":
                score += cards_dictionnary[card]
            else:
                if score <= 10:
                    score += 11
                else:
                    score += 1
        return score

    def wants_to_draw(self):
        """Does the player want to draw a card? Only useful for the IRL player"""
        if self.is_computer : 
            if self.calculate_score() < 17:
                return True
        else:
            what_to_do = get_valid_input_text("Type 'yes' to get another card, type 'no' to pass: ")
            if what_to_do: 
                return True
            else:
                return False

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

class Game:
    """Manages the complete flow of the game"""
    def __init__(self, player, computer, bank):
        self.player = player
        self.computer = computer
        self.bank = bank
       
    def display_hand_and_score(self):
        """Displays messages for game rounds"""
        print(f"Your cards : {self.player.hand}, current score: {self.player.calculate_score()}")
        first_card = self.computer.hand[0]
        if first_card == "A":
            print(f"Computer's first card : {first_card}, current computer score: {cards_dictionnary[first_card][1]}")
        else:
            print(f"Computer's first card : {first_card}, current computer score: {cards_dictionnary[first_card]}")

    def start_round(self, deck):
        """Initial function of the game launch"""
        bid = get_valid_bid(self.bank.balance, f"How much do you want to bid ? (Your bank account have ${self.bank.balance})\n$")
        self.player.draw_initial_cards(deck)
        self.computer.draw_initial_cards(deck)
        self.display_hand_and_score()
        return bid

    def player_turn(self, deck):
        """Function when it's the IRL player's turn to play"""
        while self.player.calculate_score() < 21:
            keep_playing = self.player.wants_to_draw()
            if keep_playing:
                self.player.draw_card(deck)
                self.display_hand_and_score()
            else:
                break

    def computer_turn(self, deck):
        """Function when it's the oridanator's turn to play"""
        while self.computer.wants_to_draw():
            self.computer.draw_card(deck)
 
    def compare_scores(self, bid_amount):
        """Function to compare players' scores and determine the winner"""
        player_final_score = self.player.calculate_score()
        computer_final_score = self.computer.calculate_score()
        if player_final_score == computer_final_score:
            print(f"It's a Draw !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYour bid of ${bid_amount} is refunded")
            
        elif player_final_score == 21:
            balance_update = self.bank.update_after_win(bid_amount)
            print(f"{self.player.name} win with a Blackjack !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou win ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update
        
        elif (player_final_score > computer_final_score and player_final_score < 21) or computer_final_score > 21:
            balance_update = self.bank.update_after_win(bid_amount)
            print(f"{self.player.name} win !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou win ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update
        
        else:
            balance_update = self.bank.update_after_loss(bid_amount)
            print(f"{self.player.name} lose !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou lose ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update

    def wants_replay(self, refill_count, total_balance, balance_update):
        """Function to find out if the IRL player wants to play again"""

        def display_end_message():
            """Internal function for displaying end-of-game messages"""
            if refill_count == 0:
                print(f"Your total win for this game are ${balance_update - total_balance}\nYour actual bank account is now at ${balance_update}\nPlease re-run the file to play again\nHave a great day!")
            else: 
                print(f"Your total win for this game are ${balance_update - total_balance} with a number of {refill_count} refill of your bank account\nYour actual bank account is now at ${balance_update}\nPlease re-run the file to play again\nHave a great day!")

        replay_choice = get_valid_input_text("Do you want to replay ? Type 'yes' or 'no'")
        if replay_choice and self.bank.balance < 1:
            print("\n" * 50)
            if get_valid_input_text("Your account level is too low, do you want to refill or stop ? Type 'yes' to refill and 'no' to stop"):
                refill_amount = get_valid_balance("Put the amount of refill")
                self.bank.refill(refill_amount)
                total_balance += refill_amount
                refill_count += 1
                return True, refill_count, total_balance
            else:
                display_end_message()
                return False, refill_count, total_balance
        elif replay_choice:
            print("\n" * 50)
            return True, refill_count, total_balance
        else:
            display_end_message()
            return False, refill_count, total_balance

# ----- Useful global functions -----
def get_valid_input_text(text):
    """Check that text inputs are valid"""
    while True:
        user_input = input(text).lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Typo Error, please type 'yes' or 'no'")

def get_valid_balance(bank_amount_text):
    """Check that balance inputs are valid"""
    while True:
        balance = int(float(input(bank_amount_text)))
        if balance <= 0:
            print("The bid must be a positive number. Please try again.")
        else:
            print(f"Your amount of ${balance} is accepted.")
            return balance

def get_valid_bid(balance, bid_amount_text):
    """Check that bid inputs are valid"""
    while True:
        bid_check = int(float(input(bid_amount_text)))
        if bid_check <= 0:
            print("The bid must be a positive number. Please try again.")
        elif bid_check > balance :
            print(f"You cannot bid more than your bank amount (${balance}). Try again.")
        else:
            print(f"Your bid of ${bid_check} is accepted.")
            return bid_check 

# ----- Main -----
def main():
    """Main function"""
    game_start = get_valid_input_text("Do you want to play a game of Blackjack ? Type 'yes' or 'no'")
    if game_start:
        print(logo)
        player_name = input("What's your name ?")
        initial_balance = get_valid_balance("How much do you want to put in bank ?\n$")
        total_balance = initial_balance
        bank = Bank(initial_balance)
        refill_count = 0
    else:
        print("Have a good day, re-run the script to play")
    while game_start:
        deck = list(cards_dictionnary.keys())
        irl_player = Player(player_name, False)
        computer = Player("Computer", True)
        game = Game(irl_player, computer, bank)
        bid_amount = game.start_round(deck)
        game.player_turn(deck)
        if irl_player.calculate_score() > 21:
            game_start, refill_count, total_balance = game.wants_replay(refill_count, total_balance, balance_update=game.compare_scores(bid_amount))
        else: 
            game.computer_turn(deck)
            game_start, refill_count, total_balance = game.wants_replay(refill_count, total_balance, balance_update=game.compare_scores(bid_amount))

# ----- Launching game -----
if __name__ == "__main__":
    main()
