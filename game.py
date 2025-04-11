from player import cards_dictionnary
from useful_functions import UsefulFunctions

class Game:
    """Manages the complete flow of the game"""
    def __init__(self, player, computer, bank, validator):
        self.player = player
        self.computer = computer
        self.bank = bank
        self.validator = validator
       
    def display_hand_and_score(self):
        """Displays messages for game rounds"""
        print(f"\nYour cards : {self.player.hand}, current score: {self.player.calculate_score()}")
        first_card = self.computer.hand[0]
        if first_card == "A":
            print(f"Computer's first card : {first_card}, current computer score: {cards_dictionnary[first_card][1]}")
        else:
            print(f"Computer's first card : {first_card}, current computer score: {cards_dictionnary[first_card]}")

    def start_round(self, deck):
        """Initial function of the game launch"""
        bid = self.validator.get_valid_bid(self.bank.balance, f"\nHow much do you want to bid ? (Your bank account have ${self.bank.balance})\n$")
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
            print(f"\nIt's a Draw !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYour bid of ${bid_amount} is refunded")
            
        elif player_final_score == 21:
            balance_update = self.bank.update_after_win(bid_amount)
            print(f"\n{self.player.name} win with a Blackjack !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou win ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update
        
        elif (player_final_score > computer_final_score and player_final_score < 21) or computer_final_score > 21:
            balance_update = self.bank.update_after_win(bid_amount)
            print(f"\n{self.player.name} win !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou win ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update
        
        else:
            balance_update = self.bank.update_after_loss(bid_amount)
            print(f"\n{self.player.name} lose !\nYour final hand is : {self.player.hand} with a final score of : {player_final_score} and\nThe computer final hand is {self.computer.hand} with a final score of : {computer_final_score}\nYou lose ${bid_amount}, your bank account will be updated to ${balance_update}")
            return balance_update

    def wants_replay(self, refill_count, total_balance, balance_update):
        """Function to find out if the IRL player wants to play again"""

        def display_end_message():
            """Internal function for displaying end-of-game messages"""
            if refill_count == 0:
                print(f"\nYour total win for this game are ${balance_update - total_balance}\nYour actual bank account is now at ${balance_update}\nPlease re-run the file to play again\nHave a great day!")
            else: 
                print(f"\nYour total win for this game are ${balance_update - total_balance} with a number of {refill_count} refill of your bank account\nYour actual bank account is now at ${balance_update}\nPlease re-run the file to play again\nHave a great day!")

        replay_choice = self.validator.get_valid_input_text("\nDo you want to replay ? Type 'yes' or 'no'\n")
        if replay_choice and self.bank.balance < 1:
            print("\n" * 50)
            if self.validator.get_valid_input_text("Your account level is too low, do you want to refill or stop ? Type 'yes' to refill and 'no' to stop\n"):
                refill_amount = self.validator.get_valid_balance("\nPut the amount of refill\n$")
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