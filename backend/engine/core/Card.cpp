#include "Card.h"
#include <cassert>

namespace GCB::Core {
    Card::Card(uint16_t id) : cardId(id) {}

    void Card::setPropety(const std::string& name, const GameValue& value) {
        properties[name] = value;
    };

    const GameValue* Card::getProperty(const std::string& name) const {
        auto it = properties.find(name);
        //debug checking
        assert(it != properties.end() && "Accessing nonexistent property."); 
        if (it == properties.end()) {
            //didnt find it
            return nullptr;
        }
        return &(it->second); //return value pointer, skip key
    };

    bool Card::hasProperty(const std::string& name) const {
        //if not equal to end of map
        return properties.find(name) != properties.end();
    };

    const std::unordered_map<std::string, GameValue>& Card::getProperties() {
        return properties;
    };
    }