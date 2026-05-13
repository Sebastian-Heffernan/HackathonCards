/**
 * @file InputRequest.h
 * @brief Represents pending player input.
 */

#ifndef INPUTREQUEST_H
#define INPUTREQUEST_H

#include <string>
#include <vector>
#include "Entity.h"

namespace GCB::State {
    
    struct InputRequest {

        enum class Status {
            PENDING,
            RESOLVED,
            CANCELLED
        };

        uint32_t id = 0;

        /// @brief GameAction this choice is attached to
        uint32_t actionId = 0;

        /// @brief prompted player
        uint32_t playerUuid = 0;

        /// @brief Display UI message
        std::string prompt;

        /// @brief selectable targets
        std::vector<Core::EntityId> targets;
        Core::EntityId selectedTarget = 0;

        Status status = Status::PENDING;
    };
}

#endif //INPUTREQUEST_H