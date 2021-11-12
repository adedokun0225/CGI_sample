package cgi.blurr.loggingsserver.Model;


import com.sun.istack.NotNull;

import javax.persistence.*;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name="users", uniqueConstraints = {
        @UniqueConstraint(columnNames = "email")
})
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @NotNull
    @Size(max = 50)
    @Email
    @Column(unique = true)
    private String email;

    @Size(max = 50)
    private String password;

    private boolean enabled;

    private boolean blurrEnabled;

    @ManyToMany
    @JoinTable(name = "user_roles",
            joinColumns= @JoinColumn(name="user_id"),
            inverseJoinColumns = @JoinColumn(name="role_id"))
    private Set<Role> roles = new HashSet<>();

    @OneToMany
    private Set<Computer> computers = new HashSet<>();

    public User(){

    }

    public User(String email) {
        this.email = email;
        this.enabled = false;
    }

    public User(String email, String password) {
        this.email = email;
        this.password = password;
        this.enabled = true;
    }

    public User(Long id) {
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Set<Role> getRoles() {
        return roles;
    }

    public void setRoles(HashSet<Role> roles) {
        this.roles = roles;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public boolean isBlurrEnabled() {
        return blurrEnabled;
    }

    public void setBlurrEnabled(boolean blurrEnabled) {
        this.blurrEnabled = blurrEnabled;
    }
}
