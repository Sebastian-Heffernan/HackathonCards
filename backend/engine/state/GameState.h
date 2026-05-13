#ifndef GAMESTATE_H
#define GAMESTATE_H

#include <unordered_map>
#include <string>
#include "InputRequest.h"
#include "Entity.h"
#include "Player.h"
#include "Zone.h"
#include "GameRegisters.h"
#include "GameAction.h"

namespace GCB::State {
    using Core::GameValue;

    class GameState {
        private:
            // CORE
            // Name: Zone
            std::unordered_map<std::string, Zone> zones;
            // Global variables
            std::unordered_map<std::string, Core::GameValue> globals;
            // Players
            std::vector<Player> players;

            // RUNTIME
            // Input requests
            std::unordered_map<uint32_t, InputRequest> requests;
            // Stack of actions
            std::vector<GameAction> actionStack;
            // store next accessible id of both stacks. 
            uint32_t nextRequestId = 1;
            uint32_t nextActionId = 1;

            // ENTITIES
            std::unordered_map<Core::EntityId, Core::Entity> entities;
            Core::EntityId nextEntityId = 1;

        public:
            //Registers
            GameRegisters registers;

            /**
             * @brief Default constructor.
             */
            GameState();

            ///////////////////////////////////////////////////////////////////
            // ZONE MANAGEMENT
            ///////////////////////////////////////////////////////////////////

            void addZone(const std::string& id, ZoneVisibility vis);
            Zone* getZone(const std::string& id);
            void removeZone(const std::string& id);

            ///////////////////////////////////////////////////////////////////
            // Globals
            ///////////////////////////////////////////////////////////////////

            void setGlobal(const std::string& name, const Core::GameValue& value);
            Core::GameValue getGlobal(const std::string& name) const;
            bool hasGlobal(const std::string& name) const;

            ///////////////////////////////////////////////////////////////////
            // Players
            ///////////////////////////////////////////////////////////////////

            void addPlayer(uint32_t uuid, const std::string& name);
            Player* getPlayer(uint32_t uuid);
            Player* getCurrentPlayer();

            void nextTurn();

            ///////////////////////////////////////////////////////////////////
            // Entities
            ///////////////////////////////////////////////////////////////////

            /**
             * @brief create entity
             * @param type - type of created entity
             * @return id of created entity
             */
            Core::EntityId createEntity(Core::EntityType type);

            Core::Entity* getEntity(Core::EntityId id);
            const Core::Entity* getEntity(Core::EntityId id) const;

            ///////////////////////////////////////////////////////////////////
            // Actions
            ///////////////////////////////////////////////////////////////////

            uint32_t pushAction(const GameAction& action);
            GameAction* getAction(uint32_t id);

            /// @brief Return next highest priority action. Works on an already
            /// sorted stack.
            GameAction* getNextRunnableAction();

            /// @brief Sorts by placing lowest priority num. first.
            /// Lowest priority num. = highest actiual priority.
            void sortActionStack();

            std::vector<GameAction>& getActionStack();

            ///////////////////////////////////////////////////////////////////
            // Input requests
            ///////////////////////////////////////////////////////////////////

            /**
             * @brief create input request
             * @param request - ref. to request to create
             * @return id of created request
             */
            uint32_t createInputRequest(const InputRequest& request);
            InputRequest* getInputRequest(uint32_t id);
            
            /**
             * @brief Resolves request, sets it's selected target, and queues
             *  up game action if present.
             * @param id - id of input to resolve
             * @param selected - target that was selected. Request's target is 
             * set to this.
             */
            void resolveInputRequest(uint32_t id, Core::EntityId selected);
    };
}

#endif //GAMESTATE_H