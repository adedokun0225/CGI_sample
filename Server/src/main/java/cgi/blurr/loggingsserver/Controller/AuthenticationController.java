package cgi.blurr.loggingsserver.Controller;

import cgi.blurr.loggingsserver.Exception.TokenRefreshException;
import cgi.blurr.loggingsserver.Model.RefreshToken;
import cgi.blurr.loggingsserver.Security.Services.UserDetailsImpl;
import cgi.blurr.loggingsserver.Security.jwt.JwtUtils;
import cgi.blurr.loggingsserver.Service.RefreshTokenService;
import cgi.blurr.loggingsserver.Service.UserService;
import cgi.blurr.loggingsserver.payload.AuthenticationController.*;
import cgi.blurr.loggingsserver.payload.MessageResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@CrossOrigin
@RestController
@RequestMapping("/api/auth")
public class AuthenticationController {

    @Autowired
    AuthenticationManager authenticationManager;

    @Autowired
    JwtUtils tokenUtils;

    @Autowired
    UserService userService;

    @Autowired
    RefreshTokenService refreshTokenService;

    @PostMapping("/signin")
    public ResponseEntity<?> authenticate(@Valid @RequestBody LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String token = tokenUtils.generateJwtToken(authentication);

        UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getDetails();

        RefreshToken refreshToken = refreshTokenService.createRefreshToken(request.getEmail());

        return ResponseEntity.ok(new LoginResponse(token, refreshToken.getToken()));
    }

    @PostMapping("/refreshToken")
    public ResponseEntity<?> refreshToken(@Valid @RequestBody TokenRefreshRequest request){
        String refreshToken = request.getRefreshToken();
        return refreshTokenService.findByToken(refreshToken)
                .map(token -> refreshTokenService.verifyExpiration(token))
                .map(RefreshToken::getUser)
                .map(user -> {
                    String jwtToken = tokenUtils.generateJwtToken(user);
                    return ResponseEntity.ok(new TokenRefreshResponse(refreshToken, jwtToken));
                }).orElseThrow(() -> new TokenRefreshException(refreshToken, "Refresh token was not found in the database!"));
    }

    @PostMapping("/signup")
    public ResponseEntity<?> register(@Valid @RequestBody SignupRequest request) {
        if(userService.existsByEmail(request.getEmail())) {
            return ResponseEntity.badRequest().body(new MessageResponse("User with this email already exists!"));
        }

        userService.addUser(request.getEmail());

        //TODO: send email to me
        return ResponseEntity.ok(new MessageResponse("Succesfully registered!"));
    }



}
