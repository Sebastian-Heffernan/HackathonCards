/**
 * @file Instruction.h
 * @brief Container class, stores simple opcode & operands
 */
#include <string>
#include <vector>
#include "GameValue.h"

namespace GCB::Engine {
    struct Instruction {
        std::string opcode;
        std::vector<Core::GameValue> operands;
    };
};