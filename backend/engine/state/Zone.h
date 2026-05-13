/**
 * @file Zone.h
 * @brief Generic container for entities
 */

#ifndef ZONE_H
#define ZONE_H

#include <string>
#include <vector>
#include "Entity.h"
#include <optional>

namespace GCB::State {

    enum class ZoneVisibility {
        HIDDEN, ///< Visible to no one
        OWNER,  ///< Visible to only the owner
        PUBLIC  ///< Visible to everyone
    };

    class Zone {
        private:
            std::string name;
            std::vector<Core::EntityId> entities;
            ZoneVisibility visibility;

        public:
            /**
             * @brief Construct new zone.
             * @param
             */
            Zone(const std::string& name, ZoneVisibility vis);

            /**
             * @brief Adds entity id to zone.
             * @param id Id of added entity
             */
            void add(const Core::EntityId id);

            /**
             * @brief Removes & returns entity id from zone by index.
             * @param index Index of card to remove.
             */
            std::optional<Core::EntityId> remove(size_t index);

            std::optional<Core::EntityId> at(size_t index) const;

            void shuffle();
            void clear();

            //Getters & setters
            const std::string& getName() const;
            size_t getCount() const;

            ZoneVisibility getVisibility() const;
            void setVisibility(ZoneVisibility vis);
    };
}
#endif