package cgi.blurr.loggingsserver.Security.jwt;

import cgi.blurr.loggingsserver.Model.User;
import cgi.blurr.loggingsserver.Security.Services.UserDetailsServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class JwtTokenFilter extends OncePerRequestFilter {

    @Autowired
    JwtUtils utils;

    @Autowired
    UserDetailsServiceImpl userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, FilterChain filterChain) throws ServletException, IOException {
        try {
            String token = parseToken(httpServletRequest);
            if(token != null && utils.validate(token)) {
                String email = utils.getEmailFromToken(token);

                UserDetails user = userDetailsService.loadUserByUsername(email);
                UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(httpServletRequest));

                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        }catch (Exception e) {
            System.out.println(e.getMessage());
        }

        filterChain.doFilter(httpServletRequest, httpServletResponse);
    }

    private String parseToken(HttpServletRequest request) {
        String auth = request.getHeader("Authorization");

        if(StringUtils.hasText(auth) && auth.startsWith("Bearer ")) {
            return auth.substring(7);
        }

        return null;
    }
}
