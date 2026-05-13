#include "CommandRegistry.h"
#include "core/HashUtils.h"

namespace GCB::GameEngine {

    CommandRegistry& CommandRegistry::get() {
        //static - keep alive
        static CommandRegistry instance; //make instance
        return instance;
    }

    void CommandRegistry::registerCommand(const std::string& name, 
        std::shared_ptr<Command> cmd) {
        uint32_t hash = Core::hash_opcode(name);
        registry[hash] = cmd;
    }

    std::shared_ptr<Command> CommandRegistry::getCommand(uint32_t hash) const {
        auto it = registry.find(hash);
        if (it == registry.end()) {
            return nullptr;
        }
        return it->second; 
    }
}