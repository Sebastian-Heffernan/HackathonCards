/** 
 * @file GameValue.cpp
 * @brief Class storing game value available to user script.
 */
#include "GameValue.h"

GameValue::GameValue() : value(std::nullptr_t{}) {}
GameValue::GameValue(int v) : value(v) {}
GameValue::GameValue(const std::string& v) : value(v) {}
GameValue::GameValue(bool v) : value(v) {}


int GameValue::asInt() const {
    return std::get<int>(value);
}
const std::string& GameValue::asString() const {
    return std::get<std::string>(value);
}
bool GameValue::asBool() const {
    return std::get<bool>(value);
}