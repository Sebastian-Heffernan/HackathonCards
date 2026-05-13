#ifndef LOGGER_H
#define LOGGER_H

#include <vector>
#include <string>

namespace GCB::Core {
    enum LogLevel { DEBUG, INFO, WARNING, ERROR };

    class Logger {
        private:
            std::vector<std::string> history;
            const size_t MAX_LOG_SIZE = 1000; //make sure it dosen't grow too big

            Logger() = default;
        
        public:
            //called from anywhere
            static Logger& get();

            void log(LogLevel level, const std::string& message);
            const std::vector<std::string>& getHistory() const;
            void clear();
    };
}

#endif //LOGGER_H