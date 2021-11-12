package cgi.blurr.loggingsserver.Model;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.Date;

@Entity
@Table(name="log_entries", uniqueConstraints = {
        @UniqueConstraint(columnNames = {
                "log_date", "computer_id", "type"
        })
})
public class LogEntry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="id")
    private Long id;

    @Column(name="log_date")
    @Temporal(TemporalType.TIMESTAMP)
    private Date logDate;

    @ManyToOne
    @NotNull
    @JoinColumn(name="computer_id")
    private Computer computer;

    @NotNull
    @Column(name="type")
    private short type;

    @Column(name="comment")
    private String comment;

    public LogEntry(){
    }

    public LogEntry(Computer user, short type, String comment, long milis){
        this.computer = user;
        this.type = type;
        this.comment = comment;
        this.logDate = new Date(milis);
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Date getLogDate() {
        return logDate;
    }

    public void setLogDate(Date logDate) {
        this.logDate = logDate;
    }

    public short getType() {
        return type;
    }

    public void setType(short type) {
        this.type = type;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public Computer getComputer() {
        return computer;
    }

    public void setComputer(Computer computer) {
        this.computer = computer;
    }
}
