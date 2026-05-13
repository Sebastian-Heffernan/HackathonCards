/**
 * @file Command.h
 * @brief Command interface
 */

#ifndef COMMAND_H
#define COMMAND_H

namespace GCB::GameEngine {
    class Command {
        //Virtual destructo - can delete derived class instances through base
        //class pointer.
        virtual ~Command() = default;
        
        public:
            //=0 must be implemented
            //virtual - overridden in dervied classes
            virtual void execute(State::GameState& state, 
                const std::vector<Core::GameValue>& args) = 0;
    };
}

#endif //COMMAND_H