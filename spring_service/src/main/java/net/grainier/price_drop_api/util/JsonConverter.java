package net.grainier.price_drop_api.util;

import org.codehaus.jackson.JsonParseException;
import org.codehaus.jackson.map.DeserializationConfig;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.type.TypeFactory;
import org.codehaus.jackson.type.TypeReference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Collection;

public class JsonConverter {

	static ObjectMapper mapper = new ObjectMapper();
	final static Logger logger = LoggerFactory.getLogger(JsonConverter.class);

	public static String convertToJson(Object objectToConvert) throws Exception {
		try {
			return mapper.writeValueAsString(objectToConvert);
		} catch (Exception e) {
			logger.error("Error serializing object", e);
			throw e;
		}
	}

	public static Object convertToObject(String jsonString, TypeReference cls)
			throws JsonParseException, JsonMappingException, IOException {
        mapper.configure(DeserializationConfig.Feature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return mapper.readValue(jsonString, cls);
	}

	public static <T> Collection<T> readListValues(String jsonString, Class collectionClass,
			T elementClass) throws JsonParseException,
			JsonMappingException, IOException {
		return mapper.readValue(jsonString,
				TypeFactory.collectionType(collectionClass, elementClass.getClass()));
	}

}
