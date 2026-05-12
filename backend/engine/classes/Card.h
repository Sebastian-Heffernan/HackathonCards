/** 
 * @file GameValue.h
 * @brief Game card with ID and dynamic inner properties.
 */

#ifndef CARD_H
#define CARD_H

#include <string>
#include <expected>
#include <unordered_map>
#include "GameValue.h"

class Card {
    private:
        uint16_t cardId;
        std::unordered_map<std::string, GameValue> properties;

    public:
        /**
         * @brief construct new card.
         * @param id Unique ID of card.
         */
        explicit Card(uint16_t);

        /**
         * @brief Assigns/updates card property.
         * @param name Key of property, as name.
         * @param value Stored value.
         */
        void setPropety(const std::string& name, const GameValue& value);

        /**
         * @brief Retrieve pointer to property.
         * @param name Key of property, as name.
         * @return Pointer to value, if not found then nullptr.
         */
        const GameValue* getProperty(const std::string& name) const;

        /**
         * @brief Check property existence.
         * @param name Key of property, as name.
         * @return true if exists, else false.
         */
        bool hasProperty(const std::string& name) const;

        /**
         * @brief Access entire properties map.
         * @return Const reference to map.
         */
        const std::unordered_map<std::string, GameValue>& getProperties();
};

#endif //CARD_H