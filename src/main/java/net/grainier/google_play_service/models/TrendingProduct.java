package net.grainier.google_play_service.models;

import net.grainier.google_play_service.util.enums.EventType;
import org.codehaus.jackson.annotate.JsonIgnore;

import java.util.ArrayList;

/**
 * Created by grainierp on 12/12/13.
 */
public class TrendingProduct {
    private String webId;
    private long rank;
    private long timeStamp;
    private String event;
    private String category;
    private ArrayList<Event> events;

    public TrendingProduct() {
        timeStamp = System.currentTimeMillis();
        events = new ArrayList<>();
        for (EventType et : EventType.values()) {
            events.add(new Event(et));
        }
    }

    @JsonIgnore
    public void setEvent(EventType event) {
        this.event = event.toString().toUpperCase();
        Event lastEvent = new Event(event);
        lastEvent.setTimeStamp(System.currentTimeMillis());

        if (isEventExistInEvents(lastEvent)) {
            this.events.remove(lastEvent);
            this.events.add(lastEvent);
        } else {
            this.events.add(lastEvent);
        }
    }

    public void updateEvent(Event updatedEvent) {
        if (isEventExistInEvents(updatedEvent)) {
            this.events.remove(updatedEvent);
            this.events.add(updatedEvent);
        } else {
            this.events.add(updatedEvent);
        }
    }

    public boolean isEventExistInEvents (Event event) {
        for (Event e : this.events) {
            if (e.equals(event)) return true;
        }
        return false;
    }

    public  Event getEvent (EventType type) {
        for (Event e : this.events) {
            if (e.getType() == type) return e;
        }
        return null;
    }

    public String getWebId() {
        return webId;
    }

    public void setWebId(String webId) {
        this.webId = webId;
    }

    public long getRank() {
        return rank;
    }

    public void setRank(long rank) {
        this.rank = rank;
    }

    public long getTimeStamp() {
        return timeStamp;
    }

    public void setTimeStamp(long timeStamp) {
        this.timeStamp = timeStamp;
    }

    public String getEvent() {
        return event;
    }

    public void setEvent(String event) {
        this.event = event;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public ArrayList<Event> getEvents() {
        return events;
    }

    public void setEvents(ArrayList<Event> events) {
        this.events = events;
    }

    @Override
    public String toString() {
        return String.format("TrendingProduct [webId=%s, rank=%d, timeStamp=%d, event=%s, category=%s]", webId, rank, timeStamp, event, category);
    }
}
