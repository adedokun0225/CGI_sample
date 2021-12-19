package cgi.blurr.loggingsserver.payload.AuthenticationController;

public class TokenRefreshResponse {

    private String refreshToken;

    private String type = "Bearer";

    private String jwtToken;

    public TokenRefreshResponse() {

    }

    public TokenRefreshResponse(String refreshToken, String jwtToken) {
        this.refreshToken = refreshToken;
        this.jwtToken = jwtToken;
    }

    public String getRefreshToken() {
        return refreshToken;
    }

    public void setRefreshToken(String refreshToken) {
        this.refreshToken = refreshToken;
    }

    public String getJwtToken() {
        return jwtToken;
    }

    public void setJwtToken(String jwtToken) {
        this.jwtToken = jwtToken;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
