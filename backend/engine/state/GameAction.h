/**
 * @file GameAction.h
 * @brief Generic modifiable game event.
 */

#ifndef GAMEACTION_H
#define GAMEACTION_H

#include <cstdint>
#include "Entity.h"
#include "GameValue.h"

namespace GCB::State
{
    struct GameAction {

        enum class Phase {
            READY,      ///< runnable
            PENDING,    ///< most likely for input
            RESOLVED,   ///< finished
            CANCELLED
        };

        struct Origin {
            /// @brief who the request was made by
            enum class Type {
                PLAYER, 
                ENTITY,
                SYSTEM
            };

            Type type = Type::SYSTEM;
            Core::EntityId entityId = 0; //valid if ENTITY
            uint32_t playerUuid = 0;     //valid if PLAYER
        };

        uint32_t id;    ///id of action
        Origin source;  /// what initiated action

        //uint32_t instructionPointer = 0;
        
        /// @brief order in which actions will be run by engine
        /// Lower number - higher priority
        int priority = 0;

        std::vector<Core::GameValue> args;
        Phase phase = Phase::READY;

        /// @brief choice blocking action
        uint32_t blockedByChoiceId = 0;
    };
} // namespace GCB::State


#endif //GAMEACTION_H