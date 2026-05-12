/** 
 * @file GameValue.h
 * @brief Container class, wraps multiple datatypes for use in game script.
 */
#ifndef GAMEVALUE_H
#define GAMEVALUE_H

#include <variant>
#include <string>

class GameValue {
    private:
        std::variant<int, std::string, bool, std::nullptr_t> value;

    public:
        GameValue();
        explicit GameValue(int v);
        explicit GameValue(const std::string& v);
        explicit GameValue(bool v);

        int asInt() const;
        const std::string& asString() const;
        bool asBool() const;
};


#endif //GAMEVALUE_H