package cgi.blurr.loggingsserver.Repository;

import cgi.blurr.loggingsserver.Model.Role;
import cgi.blurr.loggingsserver.Model.RoleEnum;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RoleRepository extends JpaRepository<Role, Long> {
    Optional<Role> findByName(RoleEnum name);
}
