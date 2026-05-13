#include "vm/VirtualMachine.h"
#include "vm/CommandRegistry.h"
#include "HashUtils.h"

namespace GCB::GameEngine {
    VirtualMachine::VirtualMachine(State::GameState& state) : gameState(state) {}

    void VirtualMachine::loadProgram(const std::vector<Instruction>& instrSet) {
        program = instrSet;
        pointer = 0; //reset pointer
    }

    void VirtualMachine::run() {
        running = true;
        //:: since static
        Logger::get().log(Core::LogLevel::INFO, "VM started.");

        //step through all instructions
        while (running && pointer < program.size()) {
            step();
        }

        //finished
        running = false;
        if (pointer >= program.size()) {
            Logger::get().log(Core::LogLevel::INFO, "VM finished.");
        } else {
            Logger::get().log(Core::LogLevel::ERROR, "VM exiting.");
        }
    }

    void VirtualMachine::step() {
        const Instruction& instr = program[pointer];
        if (handleSysInstr(instr))
            return;

        std::shared_ptr<Command> cmd = CommandRegistry::get().getCommand(instr.opCode);
        if (cmd) {
            cmd->execute(gameState, instr.args);
            pointer++;
        } else {
            Logger::get().log(Core::LogLevel::ERROR, 
                "Unknown OpCode: " + std::to_string(instr.opCode));
            running = false;
        }
    }

    void VirtualMachine::stop() {
        running = false;
    }

    bool VirtualMachine::handleSysInstr(const Instruction& instr) {
        //static - don't calc each time
        static const uint32_t HASH_JUMP = Core::hash_opcode("JUMP"); 
        static const uint32_t HASH_CALL = Core::hash_opcode("CALL");
        static const uint32_t HASH_RET  = Core::hash_opcode("RET");

        if (instr.opCode == HASH_RET) {
            if (!callStack.empty()) {
                pointer = callStack.top();
                callStack.pop();
            } else {
                Logger::get().log(Core::LogLevel::ERROR, "VM stack underflow \\
                    on RET: empty stack at index " + std::to_string(pointer));
                running = false;
            }
            return true;
        }
        //otherwise need 2 args
        if (instr.args.empty()) {
            Logger::get().log(Core::LogLevel::ERROR, "VM: JUMP/CALL missing \\
                target index argument at index " + std::to_string(pointer));
            running = false;
        } 
        
        if (instr.opCode == HASH_JUMP) {
            pointer = instr.args[0].asInt();
        } else if (instr.opCode == HASH_CALL) {
            callStack.push(pointer + 1);
            pointer = instr.args[0].asInt();
        } else {
            return false;
        }

        //bounds check
        if (pointer >= program.size() && running) {
            Logger::get().log(Core::LogLevel::ERROR, 
                "VM: Jumped out of bounds at index " + std::to_string(pointer));
            running = false;
        }

        return true;
    }
}