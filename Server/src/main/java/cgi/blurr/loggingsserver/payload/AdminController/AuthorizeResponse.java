package cgi.blurr.loggingsserver.payload.AdminController;

public class AuthorizeResponse {

    private boolean success;

    private String password;

    public AuthorizeResponse(boolean success, String password) {
        this.success = success;
        this.password = password;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }
}
