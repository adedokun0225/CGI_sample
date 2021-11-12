package cgi.blurr.loggingsserver.payload.UserController;

public class BlurrEnabledResponse {

    private boolean blurrEnabled;

    public BlurrEnabledResponse() {

    }

    public BlurrEnabledResponse(boolean blurrEnabled) {
        this.blurrEnabled = blurrEnabled;
    }

    public boolean isBlurrEnabled() {
        return blurrEnabled;
    }

    public void setBlurrEnabled(boolean blurrEnabled) {
        this.blurrEnabled = blurrEnabled;
    }

}
