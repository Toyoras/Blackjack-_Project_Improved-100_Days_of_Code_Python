import random
from useful_functions import UsefulFunctions

cards_dictionnary = {"A":[1,11],"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

class Player:
    """Represents a player"""
    def __init__(self, name, is_computer, validator):
        self.hand = []
        self.name = name
        self.is_computer = is_computer
        self.validator = validator

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
            what_to_do = self.validator.get_valid_input_text("\nType 'yes' to get another card, type 'no' to pass\n")
            if what_to_do: 
                return True
            else:
                return False