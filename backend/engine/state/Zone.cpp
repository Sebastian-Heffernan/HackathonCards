/**
 * @file Zone.cpp
 * @brief Implementation of generic container for cards
 */

#include "Zone.h"
#include <chrono>
#include <algorithm>
#include <random>

namespace GCB::State {
    Zone::Zone(const std::string& zoneName, ZoneVisibility vis) : name(zoneName), visibility(vis) {}

    void Zone::addCard(const Card& card) {
        cards.push_back(card);
    }

    Card Zone::removeCard(size_t index) {
        if (index >= cards.size()) {
            //return Null card
            return Card(0);
        }
        Card removedCard = cards[index]; //copy
        cards.erase(cards.begin() + index);
        return removedCard;
    }

    void Zone::shuffle() {
        //(using time)
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::default_random_engine engine(seed);
        std::shuffle(cards.begin(), cards.end(), engine);
    }

    void Zone::clear() {
        cards.clear();
    }

    const std::string& Zone::getName() const {
        return name;
    }

    size_t Zone::getCount() const {
        return cards.size();
    }

    const std::vector<Card>& Zone::getCards() const {
        return cards;
    }

    const Card* Zone::getCardAt(size_t index) const {
        if (index >= cards.size()) {
            return nullptr;
        }
        return &cards[index];
    }

    ZoneVisibility Zone::getVisibility() const {
        return visibility;
    }

    void Zone::setVisibility(ZoneVisibility vis) {
        visibility = vis;
    }
}