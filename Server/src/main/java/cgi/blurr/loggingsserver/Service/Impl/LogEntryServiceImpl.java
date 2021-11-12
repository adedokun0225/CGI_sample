package cgi.blurr.loggingsserver.Service.Impl;

import cgi.blurr.loggingsserver.Model.Computer;
import cgi.blurr.loggingsserver.Model.LogEntry;
import cgi.blurr.loggingsserver.Model.User;
import cgi.blurr.loggingsserver.Repository.ComputerRepository;
import cgi.blurr.loggingsserver.Repository.LogEntryRepository;
import cgi.blurr.loggingsserver.Repository.UserRepository;
import cgi.blurr.loggingsserver.Security.Services.UserDetailsImpl;
import cgi.blurr.loggingsserver.Service.LogEntryService;
import cgi.blurr.loggingsserver.payload.LogController.LogsResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
public class LogEntryServiceImpl implements LogEntryService {

    @Autowired
    private LogEntryRepository logRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ComputerRepository computerRepository;

    @Override
    public void log(short code, String comment, long milis, String mac) {
        UserDetailsImpl details = (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByEmail(details.getEmail()).orElseThrow(() -> new RuntimeException("Error: User not found"));
        Computer computer = computerRepository.findByUserAndMac(user, mac).orElseGet(() -> {
            Computer c = new Computer(mac, user);
            return computerRepository.save(c);
        });
        LogEntry logEntry = new LogEntry(computer, code, comment, milis);
        logRepository.save(logEntry);
    }

    @Override
    public LogsResponse getOwnLogs(long from, long to) {

        UserDetailsImpl details = (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        User user = userRepository.findByEmail(details.getEmail()).orElseThrow(() -> new RuntimeException("Error: User not found"));

        List<LogEntry> logEntries = logRepository.findByLogDateBetween(new Date(from), new Date(to), user);

        LogsResponse response = new LogsResponse();
        for(LogEntry entry: logEntries){
            response.add(entry);
        }

        return response;
    }
}
