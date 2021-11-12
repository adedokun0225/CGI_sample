package cgi.blurr.loggingsserver.Controller;

import cgi.blurr.loggingsserver.Service.UserService;
import cgi.blurr.loggingsserver.payload.UserController.BlurrEnabledResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
@RequestMapping("/api/user")
public class UserController {

    @Autowired
    private UserService userService;

    @GetMapping("/isBlurrEnabled")
    public ResponseEntity<?> isBlurrEnabled() {
        return ResponseEntity.ok(new BlurrEnabledResponse(userService.isBlurrEnabled()));
    }

}
