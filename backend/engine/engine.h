/**
 * @file engine.cpp
 * @brief main engine class
 */
#include "GameState.h"
#include "Command.h"
#include <stack>
#include <memory>
#include <map>

namespace GCB::GameEngine {

    class GameEngine {
        private:
            State::GameState state;

            //navigation
            std::string currentLabel;
            size_t pointer = 0;
            std::stack<std::pair<std::string, size_t>> callStack;

        public:
            GameEngine();

            void loadScript();

            /// @brief Run single instruction.
            void step();
            /// @brief Run until BREAK or end of label.
            void run();

            /// Pointer controll in Engine
            /// @brief Jump to label
            void jumpTo(const std::string& label, size_t newPointer = 0);
            /// @brief call 
            void call(const std::string& label);
            void returnFromCall();

            //getters & setters
            State::GameState getState();
    };
}