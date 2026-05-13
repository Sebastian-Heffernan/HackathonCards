/**
 * @file engine.h
 * @brief VM manager
 */
#ifndef ENGINE_H
#define ENGINE_H

#include "GameState.h"
#include "VirtualMachine.h"
#include "Command.h"
#include <stack>
#include <memory>
#include <map>

namespace GCB::GameEngine {

    class GameEngine {
        private:
            State::GameState state;
            VirtualMachine vm;

        public:
            GameEngine() : vm(state) {};

            void initLobby(int playerCount);

            State::GameState& getState();
            VirtualMachine& getVM();

            void processTurn();
    };
}

#endif //ENGINE_H