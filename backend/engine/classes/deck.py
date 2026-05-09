from enum import Enum

class Suit(Enum):
    SPADES = "spades"
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"

VALUES = ['02', '03', '04', '05', '06', '07', '08', '09', '10', 'J', 'Q', 'K', 'A']

class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.populate()

    def populate(self):
        self.cards.clear()
        for suit in Suit:
            for val in VALUES:
                self.cards.append({
                    'suit': suit.value,
                    'value': val
                })

    