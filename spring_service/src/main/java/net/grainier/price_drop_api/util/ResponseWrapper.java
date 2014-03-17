package net.grainier.price_drop_api.util;


import net.grainier.price_drop_api.util.enums.ResponseStatusEnum;

/**
 * Wrapper used to wrap the response
 */
public class ResponseWrapper {
    //Method to wrap the data object to the common KDE response format
    public ResponseContainer Wrap(Object resData, ResponseStatusEnum status) {
        ResponseContainer rc = new ResponseContainer();

        try {
            rc.setResCode(String.valueOf(status.getValue()));
            rc.setResMessage(String.valueOf(status));
            rc.setResData(resData);
        }
        catch (Exception e) {
            e.printStackTrace();
        }

        return rc;
    }
}
