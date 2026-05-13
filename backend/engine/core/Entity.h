#include <cstdint>
#include <unordered_map>
#include <string>
#include "GameValue.h"

namespace GCB::Core
{
    using EntityId = uint32_t;

    enum class EntityType {
        CARD,
        PLAYER,
        DICE,
        TOKEN,
        EFFECT
    };

    struct Entity {
        EntityId id;
        EntityType type;

        std::unordered_map<std::string, GameValue> properties;
    };

    
} // namespace GCB::Core