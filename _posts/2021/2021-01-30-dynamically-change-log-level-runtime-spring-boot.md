---
layout: post
title: How to Dynamically Change Log Levels at Runtime with Spring Boot
tags:
  - log
  - logger
  - logging
  - spring boot
  - actuator
  - runtime
  - debug
typora-root-url: ..
---

As we can all probably agree, logging is a vital part of any application. It provides visibility into what our component is doing at any point in time and is an invaluable tool when trying to debug issues. When faced with a problem in production, likely one of the first things that will be done is to check the logs for any errors and to hopefully locate the source of the issue. It's therefore vital that our logs are not only relevant and useful (perhaps a topic for another day), but are also visible and accessible when we need them the most. Hopefully we will be lucky and the logs will include all the necessary details to pinpoint the issue - or maybe they won't. This may be decided by the level at which the loggers are configured.

By default, most if not all of our loggers will probably be set to `INFO` level. This is fine when everything is working correctly - including only the key operations/tasks and not creating too much noise as to overload the logging tools - but perhaps not so great when you need to work an issue. Although the developers may have included some basic `INFO` level log output within the problematic area, this may not include enough data to properly trace through an erroneous transaction. The same developer may have also added some additional `DEBUG` log lines (hopefully, if not they should do) that give us some additional details into what was being done, but these may not be visible to us when the application is deployed within an environment. 

I bet most people reading this can remember that instance in which they were debugging an issue, were able to focus down on a particular segment of code, only to find that the log line that gave them that critical piece of information was set to `DEBUG` level and so was unavailable to them. We may have 6 different log levels available, but without finer control over their configuration at runtime, we may as well only have half that.

## Spring Boot Logging Properties

Log configuration within Spring Boot applications takes a number of different forms these days, but in this post we'll focus just on the main ones (excluding specific `logback.xml` modifications etc). A lot of the same configuration changes you would previously have made in those dedicated files can now also be set as simple application properties. For example, to change the global root log level to `DEBUG`, we can just add the following to `application.properties` (or `YAML` equivalent):

````properties
logging.level.root=DEBUG
````

This however has similar problems to the conventional `logback.xml` approach - to update these configuration settings you would have to rebuild and redeploy your entire application - not something that's plausible in production. The difference here is that these all just standard Spring Boot properties, so in much the same way as you would elsewhere, you can set them as environment variables or pass them in as JVM options:

```properties
-Dlogging.level.root=DEBUG
```

This gets us somewhat closer to where we want to be - we can now control the log level without redeploying - but it also introduces another problem. This enables `DEBUG` log output for the *entire* application. If you've ever done this before, even in a basic Spring application, you will know that the output is extremely noisy:

- At default `INFO` level a simple Spring Boot app generates 14 lines of log output at startup
- At `DEBUG` level the same application generates over 2440 log lines - just at startup!

```
DEBUG 6852 --- [           main] o.s.b.f.s.DefaultListableBeanFactory     : Creating shared instance of singleton bean 'org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration'
DEBUG 6852 --- [           main] o.s.b.f.s.DefaultListableBeanFactory     : Creating shared instance of singleton bean 'spring.servlet.multipart-org.springframework.boot.autoconfigure.web.servlet.MultipartProperties'
2021-01-30 17:36:25.708 DEBUG 6852 --- [           main] o.s.b.f.s.DefaultListableBeanFactory     : Autowiring by type from bean name 'org.springframework.boot.autoconfigure.web.servlet.MultipartAutoConfiguration' via constructor to bean named 'spring.servlet.multipart-org.springframework.boot.autoconfigure.web.servlet.MultipartProperties'
DEBUG 6852 --- [1)-192.168.1.22] sun.rmi.transport.tcp                    : RMI TCP Connection(1)-192.168.1.22: (port 65235) op = 80
DEBUG 6852 --- [1)-192.168.1.22] javax.management.remote.rmi              : [javax.management.remote.rmi.RMIConnectionImpl@3440316d: connectionId=rmi://192.168.1.22  1] closing.
DEBUG 6852 --- [1)-192.168.1.22] javax.management.remote.rmi              : [javax.management.remote.rmi.RMIConnectionImpl@3440316d: connectionId=rmi://192.168.1.22  1] closed.
DEBUG 6852 --- [           main] o.s.b.f.s.DefaultListableBeanFactory     : Autowiring by type from bean name 'errorPageCustomizer' via factory method to bean named 'dispatcherServletRegistration'
DEBUG 6852 --- [           main] o.apache.tomcat.util.IntrospectionUtils  : IntrospectionUtils: setProperty(class org.apache.coyote.http11.Http11NioProtocol port=8080)
```

If you look at the some of the output above you will notice that most of it is just noise and won't help you resolve any real issues. In fact, it may hinder you when trying to search through all the volume just to find those few useful lines.

In reality setting the root log level to `DEBUG` is not something you really want to do unless you feel some need to closely inspect the Spring startup sequence. It belongs at the default `INFO` level where the frameworks and other libraries won't overwhelm you with data. What you actually probably wanted was to only set the new log level for certain targeted areas of your application - be it a set of packages or even a particular class in much the way you can in `logback.xml`. Spring Boot also allows you to use the same property syntax for this. For example, to enable `DEBUG` output only in our `service` packages or specifically within our `WidgetService` class, we can instead add the following to `application.properties`:

```properties
logging.level.com.example.demo.service=DEBUG
logging.level.com.example.demo.service.WidgetService=DEBUG
```

Checking the log output again, you should see most of the noise from before disappear - leaving only our targeted package at the lower log level. Much more useful! You might notice that this really just has the same effect as updating the `logback.xml` file directly, and you would be correct. The big difference here however is that when combined with the VM argument trick from before, you now have much fine-grained control over your loggers after your application is deployed.

```
INFO 8768  --- [nio-8080-exec-1] com.example.demo.service.WidgetService   : Finding widgets for bob
DEBUG 8768 --- [nio-8080-exec-1] com.example.demo.service.WidgetService   : Background working happening to find widgets..
DEBUG 8768 --- [nio-8080-exec-1] com.example.demo.service.WidgetService   : Found user bill, returning widget 2
```

This is another improvement, but still has one big problem - you need to restart your application for the changes to be applied. This might be ok for some cases, but for example if the underlying issue was due some particular bad state of a local cache, restarting would reset the component, hide the underlying cause and make it much harder to reproduce further. Depending on the issue it may be possible to get your application back into the same state again after rehydrating caches etc, but sometimes "turn it off and on again" just hides the larger underlying problem.

As a last improvement, it would be great if you could dynamically change the log levels for particular targeted areas at runtime - without having to rebuild, redeploy *or* restart.

## Spring Boot Actuator

[Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html), amongst other things, allows you to do just this through one of it's administration endpoints. To enable this functionality we first need to add the starter dependency to the `build.gradle` file:

```groovy
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

By default actuator doesn't expose any of it's admin endpoints, so we also need to explicitly enable the loggers feature(and others if you need to). Add the following into `application.properties`:

```properties
management.endpoints.web.exposure.include=loggers
```

If we now visit `http://localhost:8080/actuator` in the browser (or as `GET` request from elsewhere) you should see just the logger endpoints are now enabled:

```json
{
  "_links": {
    "self": {
      "href": "http://localhost:8080/actuator",
      "templated": false
    },
    "loggers": {
      "href": "http://localhost:8080/actuator/loggers",
      "templated": false
    },
    "loggers-name": {
      "href": "http://localhost:8080/actuator/loggers/{name}",
      "templated": true
    }
  }
}
```

Actuator hooks into the log system used within your app (be it `Logback` or` Log4j`) and allows you to interact with these endpoints as an API to query and modify the underlying log levels.

### Viewing Current Log Levels

First of all visit `http://localhost:8080/actuator/loggers` (via `GET` request) to see all the loggers configured within your application and their current levels (it will likely be quite a large list):

```json
{
  "levels": [
    "OFF", "ERROR", "WARN", "INFO", "DEBUG", "TRACE"
  ],
  "loggers": {
    "ROOT": {
      "configuredLevel": "INFO",
      "effectiveLevel": "INFO"
    },
    "com.example.demo.DemoApplication": {
      "configuredLevel": null,
      "effectiveLevel": "INFO"
    },
    "com.example.demo.service": {
      "configuredLevel": null,
      "effectiveLevel": "INFO"
    },
    "com.example.demo.service.WidgetService": {
      "configuredLevel": null,
      "effectiveLevel": "INFO"
    }
  }
}
```

In the above extract of the output we can see all the available levels, the current level for each area of our application and finally whether or not a custom level has been applied. These are all `null` for now since we are yet to override anything. This is not too helpful, but does help in identifying the logger names that we can later customize.

If you want to explicitly target a specific logger, you can add the name to the path (as described in the first actuator output). For example `http://localhost:8080/actuator/loggers/com.example.demo.service` will return:

```json
{
  "configuredLevel": null,
  "effectiveLevel": "INFO"
}
```

### Modifying Log Levels

In the above examples we have been using simple `GET` requests to query the current log configuration. The `/actuator/loggers/{name}` endpoint however also lets you send a `POST` request that allows you to update the configured level for a particular logger. For example, to change our service loggers to `DEBUG` level, send a `POST` request to `http://localhost:8080/actuator/loggers/com.example.demo.service` with the JSON body:

```json
{
    "configuredLevel": "DEBUG"
}
```

The corresponding `cURL` command would be (note the `Content-Type` header needs to be set as the payload is a JSON object):

```
curl -i -X POST -H 'Content-Type: application/json' -d '{"configuredLevel": "DEBUG"}'
  http://localhost:8080/actuator/loggers/com.example.demo.service
  HTTP/1.1 204
```

If successful, the API will return a `204 No Content` response. Checking the application logs again after some additional calls were made to the service class, you should see the same `DEBUG` log output as before, whilst all other output remains at the default `INFO` level:

```
INFO 10848  --- [nio-8080-exec-2] com.example.demo.service.WidgetService   : Finding widgets for bob
DEBUG 10848 --- [nio-8080-exec-2] com.example.demo.service.WidgetService   : Background working happening to find widgets..
DEBUG 10848 --- [nio-8080-exec-2] com.example.demo.service.WidgetService   : Found user bill, returning widget 2
```

To confirm the update, we can also try querying actuator again with the same logger name to view the updated configuration - `GET http://localhost:8080/actuator/loggers/com.example.demo.service`:

```json
{
    "configuredLevel": "DEBUG",
    "effectiveLevel": "DEBUG"
}
```

Pretty cool! This gives you a lot of flexibility at runtime to better utilize your logs at different levels to debug and resolve issues. If you so wanted to, you can also target the the `ROOT` logger at `http://localhost:8080/actuator/loggers/ROOT`, but of course be aware of the potential noise.

## Takeaways (TL;DR)

- Logs are a vital tool when debugging issues, but only if you can see the right lines when you need them. These might not be at  `INFO` level.
- Developers should be using the various log levels `TRACE`, `DEBUG`, `INFO`, `ERROR` accordingly to add additional data points to your log output. In general volume should increase as the level decreases, but more detailed data points will be included.
- The root logger should be kept at `INFO` level. Turning on `DEBUG` logs for our entire application will generate too much noise and will overwhelm both us and our log tooling.
- Use Spring Boot properties to set specific log levels for particular packages/classes. Pass these in as runtime JVM options for greater flexibility. Note that you will have to restart the app for them to take effect.
- Spring Boot Actuator gives the most fine-grained control - allowing you both query and update log levels at runtime through it's admin endpoints.

**Useful links:**

- <https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#boot-features-logging>
- <https://docs.spring.io/spring-boot/docs/current/actuator-api/htmlsingle/#loggers>

