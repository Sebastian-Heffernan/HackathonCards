#include <iostream>
#include "card.h"

class Hand {
    private:
        Card cards[];
    public:
        void addCard(Card card);
        void removeCard(int card);
        void removeCard(Card card);
        void getCard(int card);
        friend void displayCards(Hand hand);
};

void displayCards(Hand hand) {
    std::cout << "Hand: " << hand.cards.size() << " cards";
};

// void Hand::test() {

// };