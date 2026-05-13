/**
 * @file Zone.cpp
 * @brief Implementation of generic container for entities
 */

#include "Zone.h"
#include <chrono>
#include <algorithm>
#include <random>

namespace GCB::State {
    Zone::Zone(const std::string& zoneName, ZoneVisibility vis) 
        : name(zoneName), visibility(vis) {}

    void Zone::add(const Core::EntityId id) {
        entities.push_back(id);
    }

    std::optional<Core::EntityId> Zone::remove(size_t index) {
        if (index >= entities.size()) {
            std::optional<Core::EntityId>;
        }
        Core::EntityId id = entities[index]; //copy
        entities.erase(entities.begin() + index);
        return id;
    }

    void Zone::shuffle() {
        //(using time)
        unsigned seed = std::chrono::system_clock::now()
            .time_since_epoch()
            .count();
        std::default_random_engine engine(seed);
        std::shuffle(entities.begin(), entities.end(), engine);
    }

    void Zone::clear() {
        entities.clear();
    }

    const std::string& Zone::getName() const {
        return name;
    }

    size_t Zone::getCount() const {
        return entities.size();
    }

    std::optional<Core::EntityId> Zone::at(size_t index) const {
        if (index >= entities.size()) {
            std::optional<Core::EntityId>;
        }
        return entities[index];
    }

    ZoneVisibility Zone::getVisibility() const {
        return visibility;
    }

    void Zone::setVisibility(ZoneVisibility vis) {
        visibility = vis;
    }
}