package cgi.blurr.loggingsserver.Service;

import cgi.blurr.loggingsserver.Model.RefreshToken;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public interface RefreshTokenService {
    Optional<RefreshToken> findByToken(String token);
    RefreshToken createRefreshToken(Long userId);
    RefreshToken createRefreshToken(String email);
    RefreshToken verifyExpiration(RefreshToken token);
    int deleteByUserId(Long userId);
}
