package cgi.blurr.loggingsserver.Controller;

import cgi.blurr.loggingsserver.Model.User;
import cgi.blurr.loggingsserver.Service.UserService;
import cgi.blurr.loggingsserver.payload.AdminController.AuthorizeRequest;
import cgi.blurr.loggingsserver.payload.AdminController.AuthorizeResponse;
import net.bytebuddy.utility.RandomString;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpServerErrorException;

import javax.validation.Valid;

@CrossOrigin
@RestController
@RequestMapping("/api/admin")
public class AdminController {

    @Autowired
    private UserService userService;

    @Autowired
    private PasswordEncoder encoder;

    @PostMapping("/authorizeuser")
    public ResponseEntity<?> authorize(@Valid @RequestBody AuthorizeRequest request) {
        if(!userService.existsByEmail(request.getEmail())){
            return ResponseEntity.badRequest().body(new AuthorizeResponse(false, null));
        }

        User user = userService.findByEmail(request.getEmail()).orElseThrow(() -> new HttpServerErrorException(HttpStatus.BAD_REQUEST));
        
        if(user.isEnabled()){
            return ResponseEntity.badRequest().body(new AuthorizeResponse(false, null));
        }

        String pwd = RandomString.make(12);
        //TODO: send email to the user
        user.setPassword(encoder.encode(pwd));
        user.setEnabled(true);
        userService.saveUser(user);
        return ResponseEntity.ok(new AuthorizeResponse(true, pwd));
    }
}
