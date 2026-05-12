#ifndef VARIABLE_H
#define VARIABLE_H

#include <string>
#include "GameValue.h"

namespace GCB::Core {
    class Variable {
        private:
            std::string name;
            GameValue value;
            
        public:
            /**
             * @brief construct new variable.
             * @param varName name of variable.
             */
            explicit Variable(const std::string& varName);

            //Getters & setters
            const std::string& getName() const;
            const GameValue& getValue() const;

            void setValue(const GameValue& newValue);
    };
}

#endif //VARIABLE_H