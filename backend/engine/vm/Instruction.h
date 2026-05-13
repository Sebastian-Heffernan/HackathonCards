/**
 * @file Instruction.h
 * @brief Container class, stores simple opcode & operands
 */

#include <string>
#include <vector>
#include "GameValue.h"

namespace GCB::GameEngine {
    struct Instruction {
        uint32_t opcode;
        std::vector<Core::GameValue> args;
    };
};