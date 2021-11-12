package cgi.blurr.loggingsserver.Service;

import cgi.blurr.loggingsserver.Model.LogEntry;
import cgi.blurr.loggingsserver.payload.LogController.LogsResponse;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface LogEntryService {
    void log(short code, String comment, long milis, String mac);
    LogsResponse getOwnLogs(long from, long to);
}
