/**
 * @file HashUtils.h
 * @brief Hashing algorythm functions
 */

#include <cstdint>
#include <string_view>

namespace GCB::Core {
    /**
     * @brief 32-bit hash function. Convert bytecode to hash. [FNV-1a]
     * Evaluates at compile time (constexpr)
     * Strinv_view - read only handle.
     * @param str bytecode command. 
     */
    constexpr uint32_t hash_opcode(std::string_view str) {
        uint32_t hash = 2166136261; //offset basis
        uint32_t prime = 16777619;
        for (char c : str) {
            hash = hash ^ static_cast<uint32_t>(c);
            hash = hash * prime;
        }
        return hash;
    }

 }