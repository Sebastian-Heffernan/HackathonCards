/**
 * @file Command.h
 * @brief Command interface.
 */

#ifndef COMMAND_H
#define COMMAND_H

#include "GameState.h"
#include "GameValue.h"

namespace GCB::GameEngine {
    class Command {
        public:
            //Virtual destruct - can delete derived class instances through base
            //class pointer.
            virtual ~Command() = default;
            
            //=0 must be implemented
            //virtual - overridden in dervied classes
            virtual void execute(State::GameState& state, 
                const std::vector<Core::GameValue>& args) = 0;
    };
}

#endif //COMMAND_H