package cgi.blurr.loggingsserver.Service;

import cgi.blurr.loggingsserver.Model.Role;
import cgi.blurr.loggingsserver.Model.RoleEnum;
import cgi.blurr.loggingsserver.Model.User;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public interface UserService {

    void addUser(String email, String password, RoleEnum... roles);

    void addUser(String email, RoleEnum... roles);

    boolean existsByEmail(String email);

    Optional<User> findByEmail(String email);

    void saveUser(User user);

    boolean isBlurrEnabled();

    User getCurrentUser();

}
