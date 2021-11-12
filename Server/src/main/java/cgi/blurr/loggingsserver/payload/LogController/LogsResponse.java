package cgi.blurr.loggingsserver.payload.LogController;


import cgi.blurr.loggingsserver.Lib.LogCodes;
import cgi.blurr.loggingsserver.Model.LogEntry;

import java.util.ArrayList;
import java.util.List;


public class LogsResponse {

    List<Interval> intervals = new ArrayList<>();

    List<Event> events = new ArrayList<>();

    public LogsResponse(){
    }

    public void add(LogEntry logEntry){
        if(logEntry.getType() == LogCodes.LOG_BLURR_ACTIVE || logEntry.getType() == LogCodes.LOG_BLURR_INACTIVE) {
            addInterval(logEntry);
        }else if (logEntry.getType() != LogCodes.LOG_ERROR){
            addEvent(logEntry);
        }
    }


    private void addInterval(LogEntry logEntry){
        if(!intervals.isEmpty()
                && intervals.get(intervals.size()-1).isBlurrOn() == (logEntry.getType() == LogCodes.LOG_BLURR_ACTIVE)
                && logEntry.getLogDate().getTime() - intervals.get(intervals.size()-1).getToMilis() < 600000){
            intervals.get(intervals.size() - 1).setToMilis(logEntry.getLogDate().getTime());
        }else{
            intervals.add(new Interval(logEntry.getLogDate().getTime(), logEntry.getType() == LogCodes.LOG_BLURR_ACTIVE));
        }
    }

    private void addEvent(LogEntry logEntry){
        events.add(new Event(logEntry.getType(),logEntry.getLogDate().getTime(), logEntry.getComment()));
    }

    public List<Event> getEvents() {
        return events;
    }

    public void setEvents(List<Event> events) {
        this.events = events;
    }

    public List<Interval> getIntervals() {
        return intervals;
    }

    public void setIntervals(List<Interval> intervals) {
        this.intervals = intervals;
    }

    class Interval{
        private long fromMilis;
        private long toMilis;
        private boolean blurrOn;

        public Interval(long initDate, boolean blurrOn){
            this.fromMilis = initDate;
            this.toMilis = initDate;
            this.blurrOn = blurrOn;
        }

        public long getFromMilis() {
            return fromMilis;
        }

        public long getToMilis() {
            return toMilis;
        }

        public boolean isBlurrOn() {
            return blurrOn;
        }

        public void setBlurrOn(boolean blurrOn) {
            this.blurrOn = blurrOn;
        }

        public void setFromMilis(long fromMilis) {
            this.fromMilis = fromMilis;
        }

        public void setToMilis(long toMilis) {
            this.toMilis = toMilis;
        }
    }

    class Event{
        private short type;
        private long dateMilis;
        private String comment;

        public Event(short type, long dateMilis, String comment){
            this.type = type;
            this.dateMilis = dateMilis;
            this.comment = comment;
        }

        public String getComment() {
            return comment;
        }

        public long getDateMilis() {
            return dateMilis;
        }

        public short getType() {
            return type;
        }

        public void setComment(String comment) {
            this.comment = comment;
        }

        public void setType(short type) {
            this.type = type;
        }

        public void setDateMilis(long dateMilis) {
            this.dateMilis = dateMilis;
        }
    }
}
