package net.grainier.price_drop_api.util.enums;

/**
 * Response status for Price Drop Rest APIs
 */
public enum ResponseStatusEnum {
    SUCCESS(200), //API executed successfully with data to return
    NO_CONTENT(204), //API executed successfully with no data to return
    FAILURE(500), //API failed to execute
    INVALID_USER(403),
    INVALID_PARAMETERS(400);// Forbidden. Invalid User

    private int value;

    private ResponseStatusEnum(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }
}
