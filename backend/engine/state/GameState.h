#ifndef GAMESTATE_H
#define GAMESTATE_H

#include <unordered_map>
#include <string>
#include "Zone.h"

namespace GCB::State {

    class GameState {
        private:
            //Name: Zone
            std::unordered_map<std::string, Zone> zones;
            //Global variables
            std::unordered_map<std::string, Core::GameValue> globals;

        public:
            /**
             * @brief Default constructor.
             */
            GameState();

            //Zone management
            void addZone(const std::string& id, ZoneVisibility vis);
            Zone* getZone(const std::string& id);
            void removeZone(const std::string& id);

            //Variable management
            void setGlobal(const std::string& name, const Core::GameValue value);
            Core::GameValue getGlobal(const std::string& name) const;
    };
}

#endif //GAMESTATE_H