package cgi.blurr.loggingsserver.Model;

import javax.persistence.*;
import javax.validation.constraints.NotNull;

@Entity
@Table(name = "computers", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"user_id", "mac"})
})
public class Computer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @NotNull
    @Column(name="mac")
    private String mac;

    @Column(name="name")
    private String name;

    @ManyToOne
    @JoinColumn(name="user_id")
    private User user;

    public Computer(){

    }

    public Computer(String mac, User user) {
        this.mac = mac;
        this.user = user;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getMac() {
        return mac;
    }

    public void setMac(String mac) {
        this.mac = mac;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }
}
