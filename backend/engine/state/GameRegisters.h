/**
 * @file GameRegisters.h
 * @brief Contains all registers accecible to the user
 */

#include <cstdint>

namespace GCB::State {
    struct GameRegisters {
        uint32_t turnIndex = 0;
        uint32_t turnNumber = 0;

        uint32_t activePlayerUuid = 0;

        bool gameRunning = false;
    };
}