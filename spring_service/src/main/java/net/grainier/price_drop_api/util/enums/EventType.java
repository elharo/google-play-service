package net.grainier.price_drop_api.util.enums;

/**
 * Created by grainierp on 1/22/14.
 */

/**
 Most Viewed				{EVENT : CLICK}
 Most Rated 				{EVENT : RATE}
 Most Shared				{EVENT : SHARE}
 Most Added to list		{EVENT : ADD_TO_WISH_LIST}
 logic : simple logic of getting the count of event


 Most Sold	/	Just Sold			{EVENT : ADD_TO_BAG}
 Most Reviewed	/	Just Reviewed	{EVENT : REVIEW}
 Most Pinned		/	New Pin 		{EVENT : PIN}
 Best Seller    {EVENT : SOLD}
 logic : will uses the same logic as above, but if the event occured within last 5mins (or a given time), it will be marked with the lable "Just"
 */
public enum EventType {
    CLICK,
    ADD_TO_BAG,
    ADD_TO_WISH_LIST,
    RATE,
    SHARE,
    REVIEW,
    PIN,
    SOLD;

    public static boolean isTypeExists(String type) {
        for (EventType et : EventType.values()) {
            if (et.toString().equals(type))
                return true;
        }
        return false;
    }

    public static boolean isTypeExists(EventType type) {
        for (EventType et : EventType.values()) {
            if (et == type) return true;
        }
        return false;
    }

    public static EventType getEventTypeEnum(String type) {
        for (EventType et : EventType.values()) {
            if (et.toString().equals(type.toUpperCase()))
                return et;
        }
        return null;
    }
}