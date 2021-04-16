---
layout: post
title: 30 Useful Java Libraries
tags:
  - java
  - library
  - useful
  - jvm
typora-root-url: ..
---

A collection of some interesting Java libraries and frameworks (not including the big ones everyone uses such as Spring or JUnit). Hopefully it contains some lesser known libraries which you might not have heard of before and may find useful.

| Name                                                         | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [ArchUnit](https://www.archunit.org/)                        | Write unit tests to enforce the architecture of your Java code. E.g. all your service classes follow established conventions for naming and package layout through to finding cyclic dependencies. |
| [AssertJ](https://assertj.github.io/doc/)                    | Forget `Hamcrest` or those provided by `JUnit`, `AssertJ` is the only library you will need for writing assertions. Provides countless rich integrations which are easily discoverable through auto-completion. |
| [Awaitility](https://github.com/awaitility/awaitility)       | Testing asynchronous systems can be challenging. `Awaitility` provides a simple DSL that allows you to define the expectations of async operations within tests - without having to deal with threads, timeouts and other concurrency issues. |
| [Caffeine](https://github.com/ben-manes/caffeine)            | A high performance, near optimal caching library with a modern lambda-based API. Can be easily integrated into `Spring` applications through its standard caching abstractions. |
| [Eclipse Collections](https://www.eclipse.org/collections/)  | Perhaps not needed in all cases, but can give much improved GC times and overall performance over the standard Java collections in some high throughput pipelines. Also includes immutable versions for better safety in parallel workloads. |
| [Failsafe](https://jodah.net/failsafe/)                      | A lightweight, zero-dependency library for handling all kinds of application failures. Provides a concise API that allows you to wrap executable logic within a number of resilience policies such as `Retry`, `Timeout`, `Fallback` and `CircuitBreaker`. |
| [FastExcel](https://github.com/dhatim/fastexcel)                 | `Apache POI` has numerous features for interacting with Excel files, but the API is cumbersome and resource consumption can be a problem for larger files. `FastExcel` provides a much simpler API to generate and read big Excel files quickly. |
| [Guava](https://github.com/google/guava)                 | Numerous core Java libraries from Google including additional collection types and utilities for concurrency, I/O, hashing, caching and strings. Perhaps becoming less necessary now, but still a great extension over the Java standard library. |
| [Handlebars](https://github.com/jknack/handlebars.java)      | Simple, logic-less templating engine when you want something a bit more lightweight than [Freemarker](https://freemarker.apache.org/) or [Thymeleaf](https://www.thymeleaf.org/). |
| [HikariCP](https://github.com/brettwooldridge/HikariCP)      | The best JDBC connection pool out there - fast, simple, reliable and with "zero-overhead". The default in newer `Spring Boot` based applications. |
| [Immutables](https://immutables.github.io/)                  | For those that prefer not to use `Lombok`, but still like all the benefits of immutable classes. `Immutables` is an annotation processor that generates simple, fast and consistent value objects (data classes) without all the traditional boilerplate. |
| [Faker](https://github.com/DiUS/java-faker)                  | Generate all kinds of fake data (names, addresses, emails and many more). Really useful when you need to create some throwaway data as part of tests or quick proof-of-concepts/demos. |
| [Jimfs](https://github.com/google/jimfs)                     | An in-memory file system for Java from Google. Great for unit testing when you don't want to/can't mock the underlying filesystem (usually due to static methods from `java.nio.Files` etc). |
| [Jib](https://github.com/GoogleContainerTools/jib)           | Build optimised `Docker` images from your Java applications directly from `Maven`/`Gradle`, without the need for CLI dependencies or `Dockerfiles`. `Jib` separates your app into multiple layers (splitting dependencies from classes) for much quicker rebuilds. |
| [jOOR](https://github.com/jOOQ/jOOR)                         | The `Java Reflection API` is powerful, but often cumbersome to use. `jOOR` provides a simple, fluent wrapper that gives much more intuitive access to the standard meta information and class structures. |
| [Lombok](https://projectlombok.org/)                         | A set of annotations that helps remove all the typical boilerplate and verbosity in Java applications. Easily auto-generate data classes with `constructors`, `getters/setters`, `toString`, `equals/hashcode`, `builders`, `loggers` and more. |
| [Micrometer](https://micrometer.io/)                         | A vendor-neutral application metrics facade (think `SLF4J`, but for metrics). Support for dimensional metrics and [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-features.html) offers a number of useful out-of-the-box integrations. |
| [Mug](https://github.com/google/mug)                         | A small set of utilities over Java 8 `Streams` and `Optionals`. Also includes a functional style `Maybe` implementation. |
| [Picocli](https://picocli.info/)                             | A user-friendly framework for building command-line based apps with the JVM. Supports autocompletion, colours, subcommands and is `GraalVM` compatible. |
| [Resilience4J](https://github.com/resilience4j/resilience4j) | A lightweight fault tolerance library for Java 8+ and a successor for [Netflix Hystrix](https://github.com/Netflix/Hystrix). Provides decorators for `Circuit Breakers`, `Rate Limiters`, `Retries` and `Bulkheads`. Can also be used as a circuit breaker implementation within [Spring Cloud Circuit Breaker](https://spring.io/projects/spring-cloud-circuitbreaker). |
| [Rest Assured](https://github.com/rest-assured/rest-assured) | A powerful DSL for writing tests over your RESTful API's.    |
| [Retrofit](https://github.com/square/retrofit)               | A lightweight and type-safe HTTP client for the JVM. A common go-to within Android applications to interact with external services. |
| [ShedLock](https://github.com/lukas-krecan/ShedLock)         | A distributed lock that makes sure your scheduled tasks are executed at most once at the same time. Uses an external store like a `Redis`, `JDBC` database or `Zookeeper` for coordination. |
| [StreamEx](https://github.com/amaembo/streamex)              | Many enhancements over the standard `Java Stream API` that make common tasks shorter and more convenient. Fully compatible with the built-in Java 8 `Stream` classes, but provides many additional useful methods. |
| [TestContainers](https://www.testcontainers.org/)            | Write proper integration tests that use `Docker` to spin-up throwaway instances of databases, queues, browsers and more. Integrates with `JUnit` and doesn't require any extra complex configuration. No longer feel the need to mock out external services! |
| [ThreeTen Extra](https://www.threeten.org/threeten-extra/)   | Additional date-time classes that complement those already in Java 8 (`MutableClock`, `LocalDateRange` etc). Curated by the primary author of the new `java.time` API. |
| [Vavr](https://www.vavr.io/)                                 | An essential for all the functional programmers out there. Provides all the essential data types and functional control structures alongside a number of extra modules for integrations with other libraries and frameworks. |
| [Verbal Expressions](https://github.com/VerbalExpressions/JavaVerbalExpressions) | A library that helps to construct difficult regular expressions with a fluent and human-readable API. |
| [WireMock](https://github.com/tomakehurst/wiremock)          | A library for stubbing and mocking HTTP services. Allows you to construct a standalone local web server that can be used within integration tests to verify expected behaviour against external API's. Also integrates with [Spring Cloud Contract](https://spring.io/projects/spring-cloud-contract). |
| [Yavi](https://github.com/making/yavi)                       | A lambda-based, type-safe validation library with no reflection, annotations or dependencies. For those who are not fans of using the [Bean Validation](https://beanvalidation.org/) frameworks. |
{: style="table-layout:auto"}

For even more Java libraries check out <https://github.com/akullpp/awesome-java>