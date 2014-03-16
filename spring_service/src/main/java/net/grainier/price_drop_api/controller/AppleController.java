package net.grainier.price_drop_api.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import redis.clients.jedis.Jedis;

/**
 * Created by grainier on 3/16/14.
 */
@Controller
@RequestMapping("/")
public class AppleController {
    @Autowired
    private Jedis appleRedisClient;
    @Autowired
    private ApplicationContext appContext;
    private static final Logger logger = LoggerFactory.getLogger(AppleController.class);
}
