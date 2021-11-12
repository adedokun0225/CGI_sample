package cgi.blurr.loggingsserver.Repository;

import cgi.blurr.loggingsserver.Model.RefreshToken;
import cgi.blurr.loggingsserver.Model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RefreshTokenRepository extends JpaRepository<RefreshToken, Long> {
    Optional<RefreshToken> findById(Long id);
    Optional<RefreshToken> findByToken(String token);
    int deleteByUser(User user);
}
