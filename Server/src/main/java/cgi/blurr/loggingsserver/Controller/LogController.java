package cgi.blurr.loggingsserver.Controller;

import cgi.blurr.loggingsserver.Service.LogEntryService;
import cgi.blurr.loggingsserver.payload.LogController.LogRequest;
import cgi.blurr.loggingsserver.payload.LogController.OldLogsRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class LogController {

    @Autowired
    LogEntryService logService;

    @CrossOrigin
    @PostMapping(path="log")
    public void log(@RequestBody LogRequest logRequest) {
        logService.log(logRequest.getCode(), logRequest.getComment(), logRequest.getMilis(), logRequest.getMac());
    }

    @CrossOrigin
    @PostMapping(path="oldLog")
    public void oldLog(@RequestBody OldLogsRequest logsRequest){
        if(logsRequest.getLogs() == null) return;
        for(LogRequest req: logsRequest.getLogs()){
            logService.log(req.getCode(), req.getComment(), req.getMilis(), req.getMac());
        }
    }

    @CrossOrigin
    @GetMapping(path="ownLogs")
    public ResponseEntity<?> getOwnLogs(@RequestParam(defaultValue = "-1") long fromMilis, @RequestParam(defaultValue = "-1") long toMilis){
        return ResponseEntity.ok(logService.getOwnLogs(fromMilis, toMilis));
    }

}
