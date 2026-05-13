#include "Logger.h"
#include <iostream>

namespace GCB::Core {
    Logger& Logger::get() {
        //Global access point, perform action on existing instance
        static Logger instance; //not destroyed when func ends
        return instance;
    }

    void Logger::log(LogLevel level, const std::string& message) {
        //del 1st elem. when full
        if (history.size() >= MAX_LOG_SIZE) {
            history.erase(history.begin());
        }

        //change from enum to string
        std::string prefix;
        switch (level) {
            case LogLevel::DEBUG:
                prefix = "[DEBUG] ";
                break;
            case LogLevel::ERROR:
                prefix = "[ERROR] ";
                break;
            case LogLevel::WARNING:
                prefix = "[WARNING] ";
                break;
            //treat INFO as default as well
            default:
                prefix = "[INFO] ";
                break;
        }

        history.push_back(prefix + message);

        //DEBUGGING
        std::cout << prefix + message << std::endl;
    }

    const std::vector<std::string>& Logger::getHistory() const {
        return history;
    }

    void Logger::clear() {
        history.clear();
    }
}