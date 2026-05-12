#include "GameState.h"
#include <assert.h>

namespace GCB::State {
    GameState::GameState() : currentTurnIndex(0), gameRunning(false) {}

    void GameState::addZone(const std::string& id, ZoneVisibility vis) {
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

    //Variable management
    void GameState::setGlobal(const std::string& name, const Core::GameValue value) {
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

    //Player mangement
    void GameState::addPlayer(int uuid, const std::string& name) {
        players.emplace_back(uuid, name);
    };

    Player* GameState::getPlayer(int uuid) {
        for(Player& p : players) {
            if(p.getId() == uuid) {
                return &p;
            }
            return nullptr;
        }
    };

    Player* GameState::getCurrentPlayer() {
        if (players.empty()) {
            return nullptr;
        }
        return &players[currentTurnIndex];
    };

    void GameState::nextTurn() {
        if (players.empty()) {
            return;
        }
        //Find first player IN_PLAY
        int attempts = 0; //prevent inf looping
        do {
            currentTurnIndex = (currentTurnIndex + 1) % players.size();
        } while (attempts < players.size() && 
            players[currentTurnIndex].getStatus() != PlayerStatus::IN_PLAY);
    };

    GameValue GameState::getSystemValue(const std::string& name) const {
        /// TODO
    };
}