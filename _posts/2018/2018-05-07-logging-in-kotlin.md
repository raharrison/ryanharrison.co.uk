---
layout: post
title: Logging in Kotlin
tags:
  - kotlin
  - logging
---

If you're coming into Kotlin from Java-land, you're probably very familiar with the below statement which creates a static reference to a `SLF4J` logger for the current class:

```java
private static final logger = LoggerFactory.getLogger(Something.class);
```

Even though you can of course use `SLF4J` in Kotlin, you can't use the above statement to create one due to the way that Kotlin handles `static`. Here are a couple options and workarounds for logging in Kotlin:

### Instance Variable

```kotlin
class Something {
    val logger = LoggerFactory.getLogger(Something::class.java)
}
```

This will work, but doesn't look like idiomatic Kotlin to me. For starters, you are referencing both the `Logger` and `LoggerFactory` alongside the Java version of the target class. There is also the bigger problem of the fact that this will create a new logger for each instance of `Something`  - not very efficient at all in certain cases.

### Companion Object

To clean this up a bit we can make use of `companion objects` in Kotlin to get the same `static` behaviour:

```kotlin
class Something {
    companion object {
        val logger = LoggerFactory.getLogger(Something::class.java)
    }
}
```

This will get you most of the way there, but we can do better by extracting out a factory function to create the logger for us:

**Factory Function**

```kotlin
inline fun <reified T> loggerFor(): Logger = LoggerFactory.getLogger(T::class.java)
```

**Usage**

```kotlin
class Something {
    companion object {
        val logger = loggerFor<Something>()
    }
}
```

In my opinion this isn't that great either as I have to generate and use a companion object for every class that just needs logging. That's even more verbose than Java! There is also the issue that companion objects are actually really quite heavyweight constructs - nowhere near as clear-cut as a simple static variable in Java. [This great article](https://medium.com/@BladeCoder/exploring-kotlins-hidden-costs-part-1-fbb9935d9b62) explains how they are working behind the scenes.

### Extension Function

If you want, you can also get around having to pass in the class name as the generic parameter using an extension function:

```kotlin
inline fun <reified T> T.logger(): Logger { return LoggerFactory.getLogger(T::class.java) } 
```

**Usage**

```kotlin
class Something {
    companion object {
        val logger = logger()
    }
}
```

The bad news with this approach is that in your logs the source class will actually show up as the companion object, not the actual class itself. You can around this with some logic in the factory function:

**Removing Companion Object**

```kotlin
inline fun <reified T> T.logger(): Logger {
    if (T::class.isCompanion) {
        return LoggerFactory.getLogger(T::class.java.enclosingClass)
    }
    return LoggerFactory.getLogger(T::class.java)
}
```

### Top-Level Variable - My Favourite

My personal favourite is to define the logger as a private top level variable within the same file as the target class. You can make use of the above factory function to make it very simple without having to worry about companion objects at all:

```kotlin
private val logger = loggerFor<DatabaseFactory>()

class DatabaseFactory {
    // use in here
}
```

You're not making mess in the global scope because the logger is private to this file, and no companion object!

### Kotlin-Logging Library

If none of these approaches suit your needs, there is a [dedicated logging framework](https://github.com/MicroUtils/kotlin-logging) for Kotlin which handles this in a neat approach:

```kotlin
private val logger = KotlinLogging.logger {} 
class Something {
    // use in here
}
```

This library makes clever use of a lambda as a way to get a handle on the enclosing class name. It also does a similar thing as described above to remove the companion class when needed. Personally however, I see little benefits to introducing yet another logging library for these benefits (it also provides some Kotlin friendly features around lambdas and lazy logging). With this I would end up with `SLF4J`, `Logback`/`Log4J` and now `kotlin-logging`.

### Why no static keyword?

No idea. It's one of the very few annoyances that I have with Kotlin in that it's way too difficult to define `static` variables. Companion objects are there, but that's a lot of boilerplate and [overhead](https://medium.com/@BladeCoder/exploring-kotlins-hidden-costs-part-1-fbb9935d9b62) when you just want a simple static variable like a logger.

There is also the `@JVMStatic` issue, as variables inside companion objects aren't actually static by default as seen by the `JVM`. They just act that way due to their singleton nature.

I wish JetBrains would either add a proper static keyword or make it easier to define companion variables without a complete object. Something like:

```kotlin
companion val logger = loggerFor<Something>()
```

Which could automatically translate into a `companion object` with the variable inside. It's not perfect, but saves me some boilerplate.