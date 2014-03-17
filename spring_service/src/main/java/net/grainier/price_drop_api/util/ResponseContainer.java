package net.grainier.price_drop_api.util;

/**
 * Generic response container for KDE responses
 */
public class ResponseContainer {
    private String resCode; //Response code
    private String resMessage; //Textual message for the response code
    private Object resData; //Data to be returned

    public String getResCode() {
        return resCode;
    }

    public void setResCode(String resCode) {
        this.resCode = resCode;
    }

    public String getResMessage() {
        return resMessage;
    }

    public void setResMessage(String resMessage) {
        this.resMessage = resMessage;
    }

    public Object getResData() {
        return resData;
    }

    public void setResData(Object resData) {
        this.resData = resData;
    }
}
