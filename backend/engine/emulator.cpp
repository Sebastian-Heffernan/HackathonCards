#include "engine.h"

int main() {
    //spin upp engine
    GCB::GameEngine::GameEngine engine;
    GCB::State::GameState& state = engine.getState();
    GCB::GameEngine::VirtualMachine& vm = engine.getVM();

    state.addPlayer(1, "P1");
    state.addPlayer(1, "P2");

    while (true) {
        vm.run();

        if(state)
    }
}