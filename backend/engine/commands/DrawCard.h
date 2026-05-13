#ifndef MOVECOMMAND_H
#define MOVECOMMAND_H

#include "Command.h"
#include "GameState.h"

namespace GCB::GameEngine {
    class DrawCard : public Command {
        public:
            void execute(State::GameState& state, const std::vector<Core::GameValue>& args) override;
    };
}

#endif //MOVECOMMAND_H