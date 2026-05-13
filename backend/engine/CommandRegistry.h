#ifndef COMMANDREGISTRY_H
#define COMMANDREGISTRY_H

#include <map>
#include <memory>
#include "Command.h"
#include <string>

namespace GCB::GameEngine {

    class CommandRegistry {
        private:
            std::map<std::uint32_t, std::shared_ptr<Command>> registry; 
            
            CommandRegistry() = default;

        public:
            CommandRegistry& get();
            
            /**
             * @brief Hash opcode * add it to the commandRegistry
             */
            void registerCommand(const std::string& name, std::shared_ptr<Command> cmd);
            std::shared_ptr<Command> getCommand(uint32_t hash) const;

    };
}

#endif //COMMAND_REGISTRY