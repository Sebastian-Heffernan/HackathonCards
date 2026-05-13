/**
 * @file VirtualMachine.h
 * @brief Main engine logic.
 */

#ifndef VIRTUALMACHINE_H
#define VIRTUALMACHINE_H

#include "Instruction.h"
#include "GameState.h"
#include <vector>
#include <stack>
#include "core/Logger.h"

namespace GCB::GameEngine {
    using Core::Logger;

    class VirtualMachine {
        private:
            std::vector<Instruction> program;
            /// @brief Store pointers from CALL.
            std::stack<size_t> callStack;

            size_t pointer = 0;
            bool running = false;

            State::GameState& gameState; //reference to it in Engine

            /**
             * @brief handle jumps/calls/returns internally
             * @param instr - Instruction to process
             * @return true if executed system instruction, else false.
             */
            bool handleSysInstr(const Instruction& instr);

        public:
            VirtualMachine(State::GameState& state);

            /**
             * @brief Load program into VM as set of Instructions
             * @param instrSet set of instructions
             */
            void loadProgram(const std::vector<Instruction>& instrSet);

            /// @brief Stat up the VM.
            void run();

            /// @brief Executes 1 instruction.
            void step();

            /// @brief Stops the VM.
            void stop();
    };
}

#endif //VIRTUALMACHINE_H