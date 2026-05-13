### From GameValue.ccp & .h:
#### Member Initialisation
nullptr_t avoids conversion from nullptr
```c++
GameValue::GameValue() : value(std::nullptr_t{}) {}
```

#### Variant
type-safe union (nullptr_t is nullptr type)
```c++
std::variant<int, std::string, bool, std::nullptr_t> value;
```

#### Explicit
explicit disalows implicit conversions of types (prevents them)
```c++
explicit GameValue(int v);
```

### From Card.cpp:
1st const - doesn't allow caller to modify object<br>
2nd const - Const Member Func. Doesn't modify called object
```c++
const GameValue* getProperty(const std::string& name) const;
```

#### Equivalent:
```c++
Card::Card(uint16_t id) : cardId(id) {}
Card::Card(uint16_t) {
    uint16_t cardId = id;
}
public: Card(uint16_t);
```

#### auto
auto - auto detect var type
```c++
auto it = properties.find(name);
```

#### generation
https://cplusplus.com/reference/random/

#### enum classes
https://stackoverflow.com/questions/18335861/why-is-enum-class-considered-safer-to-use-than-plain-enum

#### push back vs emplace 
https://www.geeksforgeeks.org/cpp/push_back-vs-emplace_back-in-cpp-stl-vectors/

#### shared vs unique pointe
https://stackoverflow.com/questions/6876751/differences-between-unique-ptr-and-shared-ptr

#### =default
https://stackoverflow.com/questions/20828907/the-new-syntax-default-in-c11