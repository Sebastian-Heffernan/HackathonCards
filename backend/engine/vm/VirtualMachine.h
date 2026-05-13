/**
 * @file VirtualMachine.h
 * @brief Main logic of a running game.
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

            void processAction(State::GameAction& action);

            void setPointer(size_t ptr);
            size_t getPointer() const;
    };
}

#endif //VIRTUALMACHINE_H