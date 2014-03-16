package net.grainier.price_drop_api.models;

import net.grainier.price_drop_api.util.enums.EventType;

/**
 * Created by grainierp on 1/22/14.
 */
public class Event {
    private EventType type;
    private long timeStamp;
    private long count;

    public Event(EventType type) {
        this.type = type;
        this.timeStamp = 0L;
        this.count = 0L;
    }

    public Event() {
        // to get rid of JsonMappingException
    }

    public EventType getType() {
        return type;
    }

    public void setType(EventType type) {
        this.type = type;
    }

    public long getTimeStamp() {
        return timeStamp;
    }

    public void setTimeStamp(long timeStamp) {
        this.timeStamp = timeStamp;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    @Override
    public boolean equals(Object other){
        if (other == null) return false;
        if (other == this) return true;
        if (!(other instanceof Event))return false;
        Event event = (Event) other;
        return this.getType() == event.getType();
    }
}
