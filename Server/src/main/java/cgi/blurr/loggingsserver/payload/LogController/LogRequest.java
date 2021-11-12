package cgi.blurr.loggingsserver.payload.LogController;

import javax.validation.constraints.NotBlank;

public class LogRequest {

    @NotBlank
    private Short code;

    private String comment;

    private long milis;

    private String mac;

    public Short getCode() {
        return code;
    }

    public void setCode(Short code) {
        this.code = code;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public long getMilis() {
        return milis;
    }

    public void setMilis(long milis) {
        this.milis = milis;
    }

    public String getMac() {
        return mac;
    }

    public void setMac(String mac) {
        this.mac = mac;
    }
}
