/**
 * @file Player.cpp
 * @brief Implementation of generic Player class
 */
#include "Player.h"
#include <cassert>

namespace GCB::State {
    Player::Player(int uuid, const std::string& username) : uuid(uuid), username(username), status(PlayerStatus::IN_PLAY) {}

    int Player::getId() const {
        return uuid;
    }

    const std::string& Player::getName() const {
        return username;
    }

    void Player::setStatus(PlayerStatus newStatus) {
        status = newStatus;
    }

    PlayerStatus Player::getStatus() const {
        return status;
    }

    void Player::setProperty(const std::string& key, const GameValue& val) {
        properties[key] = val;
    }

    const GameValue* Player::getProperty(const std::string& key) const {
        auto it = properties.find(key);
        //debug checking
        assert(it != properties.end() && "Accessing nonexistent property.");
        if (it == properties.end()) {
            //didnt find it
            return nullptr;
        }
        return &(it->second); 
    }

    bool Player::hasProperty(const std::string& key) const {
        return properties.find(key) != properties.end();
    }
}