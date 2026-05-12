/**
 * @file Zone.h
 * @brief Generic container for cards
 */

#ifndef ZONE_H
#define ZONE_H

#include <string>
#include <vector>
#include <Card.h>

namespace GCB::State {
    using Core::Card;

    enum class ZoneVisibility {
        HIDDEN, ///< Visible to no one
        OWNER,  ///< Visible to only the owner
        PUBLIC  ///< Visible to everyone
    };

    class Zone {
        private:
            std::string name;
            std::vector<Card> cards;
            ZoneVisibility visibility;

        public:
            /**
             * @brief Construct new zone.
             * @param
             */
            Zone(const std::string& name, ZoneVisibility vis);

            /**
             * @brief Adds card to zone.
             * @param card Ref to added card
             */
            void addCard(const Card& card);

            /**
             * @brief Removes & returns card from zone by index.
             * @param index Index of card to remove.
             */
            Card removeCard(size_t index);

            void shuffle();
            void clear();

            //Getters & setters
            const std::string& getName() const;
            size_t getCount() const;
            const std::vector<Card>& getCards() const;

            /**
             * @brief Return pointer to card at index if exists, else nullptr.
             * @param index Index of card.
             */
            const Card* getCardAt(size_t index) const;

            ZoneVisibility getVisibility() const;
            void setVisibility(ZoneVisibility vis);
    };
}
#endif