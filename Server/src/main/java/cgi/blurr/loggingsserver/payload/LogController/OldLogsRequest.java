package cgi.blurr.loggingsserver.payload.LogController;

import java.util.List;

public class OldLogsRequest {

    private List<LogRequest> logs;

    public List<LogRequest> getLogs() {
        return logs;
    }

    public void setLogs(List<LogRequest> logs) {
        this.logs = logs;
    }
}
