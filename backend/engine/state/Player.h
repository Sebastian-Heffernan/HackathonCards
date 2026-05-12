/**
 * @file Player.h
 * @brief 
 */
#ifndef PLAYER_H
#define PLAYER_H

#include <string>
#include <unordered_map>
#include "GameValue.h"

namespace GCB::State {
    using Core::GameValue;

    enum class PlayerStatus {
        IN_PLAY,    ///< Currenly their turn
        INACTIVE,   ///< Not participating (like skipping a turn etc)
        ELIMINATED, ///< No longer in play (skipped)
        SPECTATING, ///< Was never playing
        LEFT        ///< Disconnected players
    };

    class Player {
        private:
            int uuid;
            std::string username;
            PlayerStatus status = PlayerStatus::IN_PLAY; //set as def

            //key: value
            std::unordered_map<std::string, GameValue> properties;
        
        public:
            Player(int uuid, const std::string& username);

            //Getters & setters
            int getId() const;
            const std::string& getName() const;

            void setStatus(PlayerStatus status);
            PlayerStatus getStatus() const;

            void setProperty(const std::string& key, const GameValue& val);
            const GameValue* getProperty(const std::string& key) const;
            bool hasProperty(const std::string& key) const;
    };
}

#endif //PLAYER_H