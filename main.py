from art import logo
from player import Player, cards_dictionnary
from bank import Bank
from game import Game
from useful_functions import UsefulFunctions

def main():
    """Main function"""
    validator = UsefulFunctions()
    game_start = validator.get_valid_input_text("Do you want to play a game of Blackjack ? Type 'yes' or 'no'\n")
    if game_start:
        print(logo)
        player_name = input("What's your name ?\n")
        initial_balance = validator.get_valid_balance("\nHow much do you want to put in bank ?\n$")
        total_balance = initial_balance
        bank = Bank(initial_balance)
        refill_count = 0
    else:
        print("\nHave a good day, re-run the script to play")
    while game_start:
        deck = list(cards_dictionnary.keys())
        irl_player = Player(player_name, False, validator)
        computer = Player("Computer", True, validator)
        game = Game(irl_player, computer, bank, validator)
        bid_amount = game.start_round(deck)
        game.player_turn(deck)
        if irl_player.calculate_score() > 21:
            game_start, refill_count, total_balance = game.wants_replay(refill_count, total_balance, balance_update=game.compare_scores(bid_amount))
        else: 
            game.computer_turn(deck)
            game_start, refill_count, total_balance = game.wants_replay(refill_count, total_balance, balance_update=game.compare_scores(bid_amount))

if __name__ == "__main__":
    main()
