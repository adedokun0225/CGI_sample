package cgi.blurr.loggingsserver.Repository;

import cgi.blurr.loggingsserver.Model.LogEntry;
import cgi.blurr.loggingsserver.Model.User;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;

@Repository
public interface LogEntryRepository extends CrudRepository<LogEntry, Long> {
    @Query("SELECT l FROM LogEntry l, Computer c " +
            "WHERE l.computer=c AND l.logDate BETWEEN :start AND :end AND c.user=:user " +
            "ORDER BY l.logDate ASC")
    List<LogEntry> findByLogDateBetween(@Param("start") Date startLogDate, @Param("end") Date endLogDate, @Param("user") User user);
}
