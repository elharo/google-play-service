package net.grainier.price_drop_api.controller;

import com.google.common.collect.Sets;
import net.grainier.price_drop_api.models.Event;
import net.grainier.price_drop_api.models.TrendingProduct;
import net.grainier.price_drop_api.util.JsonConverter;
import net.grainier.price_drop_api.util.ResponseContainer;
import net.grainier.price_drop_api.util.ResponseWrapper;
import net.grainier.price_drop_api.util.enums.ResponseStatusEnum;
import org.codehaus.jackson.type.TypeReference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import redis.clients.jedis.Jedis;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;

@Controller
@RequestMapping("/")
public class GoogleController {
    @Autowired
    private Jedis googleRedisClient;
    @Autowired
    private ApplicationContext appContext;
    private static final Logger logger = LoggerFactory.getLogger(GoogleController.class);

    @RequestMapping(method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public String printWelcome(HttpServletResponse response) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");

        model.addAttribute("message", "Trending Service API");
        return "hello";
    }

    @RequestMapping(value = "/getTrendsForChannel", method = RequestMethod.GET, produces = {"application/json"})
    @ResponseBody
    public ResponseContainer getTrendsForChannel(@RequestParam(value = "channel", defaultValue = "") String channel, HttpServletResponse response, HttpServletRequest request) {
        response.addHeader("Access-Control-Allow-Origin", "*");
        response.addHeader("accept", "application/json");
        ArrayList<TrendingProduct> trendingProducts = null;

        HashSet<String> eventsSet = new HashSet<>(jedisEventClient.sunion(events));
        HashSet<String> categoriesSet = new HashSet<>(jedisCategoryClient.sunion(categories));
        HashSet<String> intersection = new HashSet<>(Sets.intersection(eventsSet, categoriesSet));


        Jedis jedisEventClient = (Jedis) appContext.getBean("redisClient");
        Jedis jedisCategoryClient = (Jedis) appContext.getBean("redisClient");

        Map requestParameterMap = request.getParameterMap();
        String[] categories = (String[]) requestParameterMap.get("categories[]");
        String[] events = (String[]) requestParameterMap.get("events[]");

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


        HashSet<String> result = new HashSet<>(jedisClient.sinter(new String[]{event, category}));
        ArrayList<String> eventsArrayList = new ArrayList<>(jedisEventClient.keys("SET:EVENT:*"));
        ArrayList<String> categoriesArrayList = new ArrayList<>(jedisCategoryClient.keys("SET:CATEGORY:*"));
        eventsArrayList.addAll(categoriesArrayList); // add together

        if (trendingProducts != null) {
            return new ResponseWrapper<Event>().Wrap(Product.getEvents()/*counts*/, "EVENT COUNTS", ResponseStatusEnum.SUCCESS, "");
        } else {
            return new ResponseWrapper<TrendingProduct>().Wrap(null, "EVENT COUNTS", ResponseStatusEnum.NO_DATA, "INVALID_ARGUMENTS");
        }
    }

    private void getAllEventsAndCategories() {
        Jedis jedisEventClient = (Jedis) appContext.getBean("redisClient");
        Jedis jedisCategoryClient = (Jedis) appContext.getBean("redisClient");

        // get keys for categories and events
        ArrayList<String> eventsArrayList = new ArrayList<>(jedisEventClient.keys("SET:EVENT:*"));
        ArrayList<String> categoriesArrayList = new ArrayList<>(jedisCategoryClient.keys("SET:CATEGORY:*"));

        ArrayList<String> events = new ArrayList<>();
        ArrayList<String> categories = new ArrayList<>();
    }
}