package net.grainier.google_play_service.util;

import java.util.List;

public class ResponseContainer<T> {
    private String resCode;
    private String resMessage;
    private List<T> resData;

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

    public List<T> getResData() {
        return resData;
    }

    public void setResData(List<T> resData) {
        this.resData = resData;
    }
}
