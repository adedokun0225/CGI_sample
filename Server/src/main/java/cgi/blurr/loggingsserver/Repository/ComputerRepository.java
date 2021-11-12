package cgi.blurr.loggingsserver.Repository;

import cgi.blurr.loggingsserver.Model.Computer;
import cgi.blurr.loggingsserver.Model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ComputerRepository extends JpaRepository<Computer, Long> {
    List<Computer> findByUser(User user);
    Optional<Computer> findByUserAndMac(User user, String mac);
}
