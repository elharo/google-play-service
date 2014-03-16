package net.grainier.price_drop_api.util;

import net.grainier.price_drop_api.util.enums.ResponseStatusEnum;

import java.util.ArrayList;
import java.util.List;


public class ResponseWrapper<T> {

	public ResponseContainer<T> Wrap(List<T> ol,ResponseStatusEnum status,String message) {
	
		ResponseContainer<T> rc = new ResponseContainer<T>();
		
		try {
			rc.setResData(ol);
			rc.setResCode(status.toString());
			rc.setResMessage(message);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		return rc;
	}

    public ResponseContainer<T> WrapSingle(T obj,ResponseStatusEnum status,String message) {

        ResponseContainer<T> rc = new ResponseContainer<T>();

        try {
            rc.setResData(new ArrayList<T>());
            rc.getResData().add(obj);
            rc.setResCode(status.toString());
            rc.setResMessage(message);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return rc;
    }
	
}
