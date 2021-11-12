package cgi.blurr.loggingsserver;

import cgi.blurr.loggingsserver.Model.Role;
import cgi.blurr.loggingsserver.Model.RoleEnum;
import cgi.blurr.loggingsserver.Model.User;
import cgi.blurr.loggingsserver.Repository.RoleRepository;
import cgi.blurr.loggingsserver.Repository.UserRepository;
import cgi.blurr.loggingsserver.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.password.PasswordEncoder;

@SpringBootApplication
public class LoggingsserverApplication {

	@Autowired
	private PasswordEncoder encoder;

	public static void main(String[] args) {
		SpringApplication.run(LoggingsserverApplication.class, args);
	}

	@Bean
	public CommandLineRunner loadData(UserService userService, RoleRepository roleRepository) {
		return (args) -> {
			for(RoleEnum role : RoleEnum.values()) {
				roleRepository.save(roleRepository.findByName(role).orElse(new Role(role)));
			}

			try {
				userService.addUser("patryk.morawski@cgi.com", "UTAQ*dAT3&3f9&Acw@Ry", RoleEnum.ROLE_ADMIN, RoleEnum.ROLE_USER);
			}catch (Exception e) {
				System.out.println(e.getMessage());
			}

		};
	}

}
