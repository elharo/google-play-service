package net.grainier.google_play_service.controller;

import com.google.common.collect.Sets;
import net.grainier.google_play_service.models.Event;
import net.grainier.google_play_service.models.TrendingProduct;
import net.grainier.google_play_service.util.JsonConverter;
import net.grainier.google_play_service.util.ResponseContainer;
import net.grainier.google_play_service.util.enums.ResponseStatusEnum;
import net.grainier.google_play_service.util.ResponseWrapper;
import org.codehaus.jackson.type.TypeReference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.*;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisDataException;

import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;

@Controller
@RequestMapping("/")
public class TrendingController {
    private static final Logger logger = LoggerFactory.getLogger(TrendingController.class);

    @Autowired
    private Jedis jedisClient;

    @Autowired
    private ApplicationContext appContext;

    @PostConstruct
    public void init() {
        // setOperations = template.opsForSet();
    }

    @RequestMapping(method = RequestMethod.GET)
    public String printWelcome(ModelMap model) {
        model.addAttribute("message", "Trending Service API");
        return "hello";
    }

    @RequestMapping(value = "/updateCategoriesDatabase", method = RequestMethod.POST, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer updateCategoriesDatabase(@RequestBody String bodyObj, HttpServletResponse response, HttpServletRequest request) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");

        if (bodyObj != null && !bodyObj.equals("")) {
                try {
                    productCategory = (ProductCategory) JsonConverter.convertToObject(bodyObj, new TypeReference<ProductCategory>() {
                    }); // make JSON
                } catch (IOException e) {
                    return new ResponseWrapper<String>().Wrap(null, "Update Categories Database", ResponseStatusEnum.INVALID_PARAMETERS, "Invalid Parameter format / type.");
                }
        } else {
            return new ResponseWrapper<String>().Wrap(null, "Update Categories Database", ResponseStatusEnum.INVALID_PARAMETERS, "Input parameters not found.");
        }

        if (productCategory.getCategory() != null && !productCategory.getCategory().equals("") && productCategory.getWebIds() != null && productCategory.getWebIds().length > 0) {
            // put new data to the redis database
            Jedis jedis = (Jedis) appContext.getBean("redisClient");
            String key;

            for (String webId : productCategory.getWebIds()) {
                key = String.format("CATEGORY:INFO:%s", webId);
                // persist in redis
                jedis.set(key, productCategory.getCategory());
            }

            return new ResponseWrapper<String>().Wrap(null, "Update Categories Database", ResponseStatusEnum.SUCCESS, "Database Updated.");
        } else {
            return new ResponseWrapper<String>().Wrap(null, "Update Categories Database", ResponseStatusEnum.FAILURE, "Input parameters not found.");
        }
    }

    @RequestMapping(value = "/getEventsAndCategories", method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer getEventsAndCategories(HttpServletResponse response) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");

        EventsAndCategories result = getAllEventsAndCategories();

        if (result != null) {
            return new ResponseWrapper<EventsAndCategories>().WrapSingle(result, "All Events And Categories", ResponseStatusEnum.SUCCESS, "");
        } else {
            return new ResponseWrapper<EventsAndCategories>().Wrap(null, "All Events And Categories", ResponseStatusEnum.NO_DATA, "RESULTS_NOT_FOUND");
        }
    }

    @RequestMapping(value = "/getEventCounts", method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer getEventCounts(@RequestParam(value = "webId", defaultValue = "") String webId, HttpServletResponse response) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");

        TrendingProduct Product = null;
        Jedis jedis = (Jedis) appContext.getBean("redisClient");
        String key = String.format("OBJECT:PRODUCT:%s", webId);

        try {
            String existingProductJsonInRedis = jedis.get(key);
            if (!"".equals(existingProductJsonInRedis) && existingProductJsonInRedis != null) try {
                Product = (TrendingProduct) JsonConverter.convertToObject(existingProductJsonInRedis, new TypeReference<TrendingProduct>() {
                });
            } catch (IOException e) {
                logger.error(e.toString());
                throw e;
            }
        } catch (Exception ex) {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "EVENT COUNTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }

        if (Product != null) {
            // EventCounts counts = new EventCounts();
            // counts.setClickCount(Product.getClickCount());
            // counts.setAddToBagCount(Product.getAddToBagCount());
            // counts.setAddToWishListCount(Product.getAddToWishListCount());
            return new ResponseWrapper<Event>().Wrap(Product.getEvents()/*counts*/, "EVENT COUNTS", ResponseStatusEnum.SUCCESS, "");
        } else {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "EVENT COUNTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }
    }


    @RequestMapping(value = "/getTrendsForChannel", method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer getTrendsForChannel(@RequestParam(value = "channel", defaultValue = "") String channel, HttpServletResponse response) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");
        ArrayList<TrendingProduct> trendingProducts;
        String event;
        String category;

        Jedis jedisEventClient = (Jedis) appContext.getBean("redisClient");
        Jedis jedisCategoryClient = (Jedis) appContext.getBean("redisClient");

        try {
            event = channel.split(":")[0];  // extract keys
            category = channel.split(":")[1];
        } catch (Exception e) {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }

        if (!"all".equals(event) && !"all".equals(category)) {
            // intersection
            event = String.format("SET:EVENT:%s", event);
            category = String.format("SET:CATEGORY:%s", category);
            HashSet<String> result = new HashSet<>(jedisClient.sinter(new String[]{event, category}));
            trendingProducts = getProductsForRedisKeys(result);
        } else if ("all".equals(event) && !"all".equals(category)) {
            // specified category set
            category = String.format("SET:CATEGORY:%s", category);
            HashSet<String> result = new HashSet<>(jedisClient.smembers(category));
            trendingProducts = getProductsForRedisKeys(result);
        } else if (!"all".equals(event) && "all".equals(category)) {
            // specified event set
            event = String.format("SET:EVENT:%s", event);
            HashSet<String> result = new HashSet<>(jedisClient.smembers(event));
            trendingProducts = getProductsForRedisKeys(result);
        } else if ("all".equals(event) && "all".equals(category)) {
            // union of all sets
            ArrayList<String> eventsArrayList = new ArrayList<>(jedisEventClient.keys("SET:EVENT:*"));
            ArrayList<String> categoriesArrayList = new ArrayList<>(jedisCategoryClient.keys("SET:CATEGORY:*"));
            eventsArrayList.addAll(categoriesArrayList); // add together

            // redis.clients.jedis.exceptions.JedisDataException: ERR wrong number of arguments for 'sunion' command
            HashSet<String> result = new HashSet<>(jedisClient.sunion(eventsArrayList.toArray(new String[eventsArrayList.size()])));
            trendingProducts = getProductsForRedisKeys(result);
        } else {
            // error with params
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }

        if (trendingProducts != null && trendingProducts.size() > 0) {
            return new ResponseWrapper<TrendingProduct>().Wrap(trendingProducts, "TRENDING PRODUCTS", ResponseStatusEnum.SUCCESS, "");
        } else {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "RESULTS_NOT_FOUND");
        }
    }

    @RequestMapping(value = "/getFilteredTrends", method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer getFilteredTrends(HttpServletResponse response, HttpServletRequest request) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");
        ArrayList<TrendingProduct> trendingProducts = null;

        Map requestParameterMap = request.getParameterMap();
        String[] categories = (String[]) requestParameterMap.get("categories[]");
        String[] events = (String[]) requestParameterMap.get("events[]");

        Jedis jedisEventClient = (Jedis) appContext.getBean("redisClient");
        Jedis jedisCategoryClient = (Jedis) appContext.getBean("redisClient");

        if (events != null && categories != null) {
            // make redis keys from request params
            for (int i = 0; i < events.length; i++) events[i] = String.format("SET:EVENT:%s", events[i]);
            for (int j = 0; j < categories.length; j++) categories[j] = String.format("SET:CATEGORY:%s", categories[j]);
            // String[] keys = (String[]) ArrayUtils.addAll(events, categories);

            try {
                HashSet<String> eventsSet = new HashSet<>(jedisEventClient.sunion(events));
                HashSet<String> categoriesSet = new HashSet<>(jedisCategoryClient.sunion(categories));
                HashSet<String> intersection = new HashSet<>(Sets.intersection(eventsSet, categoriesSet));

                trendingProducts = getProductsForRedisKeys(intersection);
            } catch (JedisDataException e) {
                logger.error(e.toString());
                return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "RESULTS_NOT_FOUND");
            }
        } else {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }


        if (trendingProducts != null && trendingProducts.size() > 0) {
            return new ResponseWrapper<TrendingProduct>().Wrap(trendingProducts, "TRENDING PRODUCTS", ResponseStatusEnum.SUCCESS, "");
        } else {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "TRENDING PRODUCTS", ResponseStatusEnum.NO_DATA, "RESULTS_NOT_FOUND");
        }
    }

    private EventsAndCategories getAllEventsAndCategories() {
        Jedis jedisEventClient = (Jedis) appContext.getBean("redisClient");
        Jedis jedisCategoryClient = (Jedis) appContext.getBean("redisClient");

        // get keys for categories and events
        ArrayList<String> eventsArrayList = new ArrayList<>(jedisEventClient.keys("SET:EVENT:*"));
        ArrayList<String> categoriesArrayList = new ArrayList<>(jedisCategoryClient.keys("SET:CATEGORY:*"));

        ArrayList<String> events = new ArrayList<>();
        ArrayList<String> categories = new ArrayList<>();

        for (String event : eventsArrayList)
            try {
                events.add(event.split(":")[2]);    // this is the category name
            } catch (Exception ignored) {
            }

        for (String category : categoriesArrayList)
            try {
                categories.add(category.split(":")[2]);    // this is the category name
            } catch (Exception ignored) {
            }

        EventsAndCategories eventsAndCategories = new EventsAndCategories();
        eventsAndCategories.setEvents(events);
        eventsAndCategories.setCategories(categories);
        return eventsAndCategories;
    }

    private ArrayList<TrendingProduct> getProductsForRedisKeys(HashSet<String> keys) {
        Jedis jedisProductsClient = (Jedis) appContext.getBean("redisClient");
        ArrayList<TrendingProduct> trendingProducts = new ArrayList<>();
        for (String key : keys) {
            String resultJson = jedisProductsClient.get(key);
            try {
                TrendingProduct product = (TrendingProduct) JsonConverter.convertToObject(resultJson, new TypeReference<TrendingProduct>() {
                });
                trendingProducts.add(product);
            } catch (IOException e) {
                logger.error(e.toString());
            }
        }
        return trendingProducts;
    }
}