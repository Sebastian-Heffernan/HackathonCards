#include "GameState.h"
#include <assert.h>
#include <algorithm>

namespace GCB::State {
    GameState::GameState() = default;

    ///////////////////////////////////////////////////////////////////
    // ZONE MANAGEMENT
    ///////////////////////////////////////////////////////////////////

    void GameState::addZone(const std::string& id, 
        ZoneVisibility vis) {
        zones.emplace(id, Zone(id, vis));
    };

    Zone* GameState::getZone(const std::string& id) {
        auto it = zones.find(id);
        if (it == zones.end()) {
            return nullptr;
        }
        return &(it->second); 
    };

    void GameState::removeZone(const std::string& id) {
        //returns end() if not found
        zones.erase(id);
    };

    ///////////////////////////////////////////////////////////////////
    // Globals
    ///////////////////////////////////////////////////////////////////

    void GameState::setGlobal(const std::string& name, const Core::GameValue& value) {
        globals[name] = value;
    };

    GameValue GameState::getGlobal(const std::string& name) const {
        auto it = globals.find(name);
        if (it == globals.end()) {
            //Return empty
            return GameValue();
        }
        return it->second; 
    };

    bool GameState::hasGlobal(const std::string& name) const {
        return globals.find(name) != globals.end();
    };

    ///////////////////////////////////////////////////////////////////////////
    // Players
    ///////////////////////////////////////////////////////////////////////////

    void GameState::addPlayer(uint32_t uuid, const std::string& name) {
        players.emplace_back(uuid, name);
    };

    Player* GameState::getPlayer(uint32_t uuid) {
        for(Player& p : players) {
            if(p.getId() == uuid) {
                return &p;
            }
        }
        return nullptr;
    };

    Player* GameState::getCurrentPlayer() {
        if (players.empty()) {
            return nullptr;
        }
        return &players[registers.turnIndex];
    };

    void GameState::nextTurn() {
        if (players.empty()) {
            return;
        }

        //Find first player IN_PLAY
        int attempts = 0; //prevent inf looping
        do {
            registers.turnIndex = (registers.turnIndex + 1) % players.size();
            attempts++;
        } while (attempts < players.size() && 
            players[registers.turnIndex].getStatus() != PlayerStatus::IN_PLAY);
    };

    ///////////////////////////////////////////////////////////////////////////
    // Entities
    ///////////////////////////////////////////////////////////////////////////

    Core::EntityId GameState::createEntity(Core::EntityType type) {
        Core::EntityId id = nextEntityId++;
        entities.emplace(id, Core::Entity{
            id, type, {}
        });
        return id;
    }

    Core::Entity* GameState::getEntity(Core::EntityId id) {
        auto it = entities.find(id);
        if (it == entities.end())
            return nullptr;
        return &it->second;
    }

    const Core::Entity* GameState::getEntity(Core::EntityId id) const {
        auto it = entities.find(id);
        if (it == entities.end())
            return nullptr;
        return &it->second;
    }

    ///////////////////////////////////////////////////////////////////
    // Actions
    ///////////////////////////////////////////////////////////////////

    uint32_t GameState::pushAction(const GameAction& action) {
        GameAction copy = action;
        copy.id = nextActionId++;
        actionStack.push_back(copy);

        sortActionStack();
        return copy.id;
    };

    GameAction* GameState::getAction(uint32_t id) {
        for (GameAction& action : actionStack) {
            if (action.id == id) {
                return &action;
            }
        }
        return nullptr;
    };

    GameAction* GameState::getNextRunnableAction() {
        for (GameAction& action : actionStack) {
            // get first ready action
            if (action.phase == GameAction::Phase::READY) {
                return &action;
            }
        }
        return nullptr;
    };

    void GameState::sortActionStack() {
        //uses a compare func.
        std::sort(actionStack.begin(), actionStack.end(),
            [](const GameAction& a, const GameAction& b) {
                return a.priority < b.priority;
            });
    };

    std::vector<GameAction>& GameState::getActionStack() {
        return actionStack;
    };

    ///////////////////////////////////////////////////////////////////
    // Input requests
    ///////////////////////////////////////////////////////////////////

    uint32_t GameState::createInputRequest(const InputRequest& request) {
        InputRequest copy = request;
        copy.id = nextRequestId++;
        requests[copy.id] = copy;
        return copy.id;
    };

    InputRequest* GameState::getInputRequest(uint32_t id) {
        auto it = requests.find(id);
        if (it == requests.end()) {
            return nullptr;
        }
        return &it->second;
    };
    
    void GameState::resolveInputRequest(uint32_t id, Core::EntityId selected) {
        InputRequest* request = getInputRequest(id);
        if (!request) {
            return;
        }

        request->selectedTarget = selected;
        request->status = InputRequest::Status::RESOLVED;

        GameAction* action = getAction(request->actionId);
        // if action present, set it to ready
        if (action) {
            action->phase = GameAction::Phase::READY;
        }
    };
}