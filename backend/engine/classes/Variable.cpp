#include "Variable.h"

//Init
Variable::Variable(const std::string& varName) : name(varName), value() {}

const std::string& Variable::getName() const {
    return name;
}

const GameValue& Variable::getValue() const {
    return value;
}

void Variable::setValue(const GameValue& newValue) {
    value = newValue;
}