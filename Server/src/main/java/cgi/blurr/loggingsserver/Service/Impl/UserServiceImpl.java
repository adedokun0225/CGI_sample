package cgi.blurr.loggingsserver.Service.Impl;

import cgi.blurr.loggingsserver.Model.Role;
import cgi.blurr.loggingsserver.Model.RoleEnum;
import cgi.blurr.loggingsserver.Model.User;
import cgi.blurr.loggingsserver.Repository.RoleRepository;
import cgi.blurr.loggingsserver.Repository.UserRepository;
import cgi.blurr.loggingsserver.Security.Services.UserDetailsImpl;
import cgi.blurr.loggingsserver.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    PasswordEncoder encoder;

    @Autowired
    UserRepository userRepository;

    @Autowired
    RoleRepository roleRepository;

    @Override
    public void addUser(String email, String password, RoleEnum... roles) {
        User user = new User(email, encoder.encode(password));
        for(int i=0; i<roles.length; i++){
            Role role = roleRepository.findByName(roles[i]).orElseThrow(() -> new RuntimeException("Error: Role not found"));
            user.getRoles().add(role);
        }
        userRepository.save(user);
    }

    @Override
    public void addUser(String email, RoleEnum... roles) {
        User user = new User(email);
        for(int i=0; i<roles.length; i++){
            Role role = roleRepository.findByName(roles[i]).orElseThrow(() -> new RuntimeException("Error: Role not found"));
            user.getRoles().add(role);
        }
        userRepository.save(user);
    }

    @Override
    public boolean existsByEmail(String email) {
        return this.userRepository.existsByEmail(email);
    }

    @Override
    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Override
    public void saveUser(User user) {
        userRepository.save(user);
    }

    @Override
    public boolean isBlurrEnabled() {
        return getCurrentUser().isBlurrEnabled();
    }

    @Override
    public User getCurrentUser() {
        UserDetailsImpl details = (UserDetailsImpl) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        return userRepository.findByEmail(details.getEmail()).orElseThrow(() -> new RuntimeException("Error: User not found"));
    }
}
