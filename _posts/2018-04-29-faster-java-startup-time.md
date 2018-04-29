---
layout: post
title: Faster Java Startup Times
tags:
  - faster
  - java
  - startup
  - time
---

Although Java is considered to be very performant in general, the startup times aren't particularly great. All things taken into account, this isn't particularly surprising when you factor in everything that happens when you start a Java program - VM creation, class loading, JIT compilation etc.

For small projects or utility programs this isn't too much of a problem, but for larger projects with a very big classpath, this can become quite annoying during development. For Spring Boot apps in particular, even though the development process is very quick, startup times can become large when you start adding a lot of dependencies.

## VM Arguments

Here are a couple of VM args which you can add to speed up startup times. 

> **NOTE - This is for development only to improve app restarts etc. This is absolutely not recommended in production environments**

`-Xverify:none`

This option disables JVM bytecode verification during startup and is perhaps the most significant source of improvement. When enabled, the JVM will check your code for certain dangerous and disallowed behaviour. Obviously, by not performing such checks, the JVM startup time will be improved. Again, you should definitely [not do this in a production environment](https://blogs.oracle.com/buck/never-disable-bytecode-verification-in-a-production-system), even if you trust all the code you are running.

`-XX:TieredStopAtLevel=1`

This option tells the JVM to stop optimising your code after the first level. The JVM has three tiers of intermediate compilation. Here we are preventing any further incremental compilation after the first level, meaning that your system has slightly more resources to use elsewhere rather than optimising your code. Again, this could potentially decrease performance so isn't recommended in production. You can read more about compilation in HotSpot in this [presentation deck](https://www.ethz.ch/content/dam/ethz/special-interest/infk/inst-cs/lst-dam/documents/Education/Classes/Fall2015/210_Compiler_Design/Slides/hotspot.pdf).

I created a simple Spring Boot app with an in-memory H2 database and a couple REST endpoints to test the difference in startup times with and without these JVM args (not that this project includes a lot of extra dependencies such as actuator, JPA, caching to reflect a standard Spring App with a large classpath):

| Startup Mode                                                | Startup Time |
| ----------------------------------------------------------- | ------------ |
| Run inside IDE with no custom arguments                     | 9.8s         |
| Run inside IDE with `-Xverify:none -XX:TieredStopAtLevel=1` | **6.2s**     |
|                                                             | **+37%**     |

That's quite a massive 37% improvement in startup times just with some simple VM args!

## Spring Boot Specifics

Aside from these magic VM args, there are a few things to take into account when building standard Spring applications that really impact startup performance:

- Spring projects are generally a magnet for massive classpaths. Look at your dependency list in a Spring Boot project and there are probably hundreds of `.jar` files and thousands of classes to load. No wonder why disabling bytecode verification can improve times so dramatically. Try to limit the amount of libraries you are bringing in and think carefully about whether you need another dependency before you just adding it to your project. Try not to end up like a Node project where half the internet is in your `node_modules` directory.
- Component scanning can be slow. This is one killer feature of the Spring framework, but as I mentioned above, if your classpath is massive then it's going to take time to run through all those classes. Try to limit the packages that are scanned or maybe consider splitting your project up. You can also make use of the `@Lazy` annotation to prevent `@Bean`s from being immediately created/loaded.
- Doing database migrations at startup. No surprise that this is going to cause some slowdown. If you are using [Liquibase](https://www.liquibase.org/) for migrations, the [JHipster](https://github.com/jhipster/jhipster) project has a nice [AsyncSpringLiquibase](https://github.com/jhipster/jhipster/blob/master/jhipster-framework/src/main/java/io/github/jhipster/config/liquibase/AsyncSpringLiquibase.java) class that prevents blocking whilst migrations are taking place.
- Initialising caches. This may significantly improve performance when the app is live, but when you have a lot of [Ehcaches](http://www.ehcache.org/) it can take a whilst to init them all at startup. In your local environment consider turning some of them off, or doing this lazily.
