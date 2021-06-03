---
layout: post
title: Using Ktor with Jackson Serialization
tags:
    - kotlin
    - ktor
    - jackson
    - json
    - mapper
typora-root-url: ../..
---

Although the preferred JSON serialization library used in a lot of the `Ktor` examples is [GSON](https://github.com/google/gson), which makes sense due to it's simplicity and ease of use, in real-world use [Jackson](https://github.com/FasterXML/jackson) is probably the preferred option. It's faster (especially when combined with the `AfterBurner` module) and generally more flexible. `Ktor` comes with a built-in feature that makes use Jackson for JSON conversion very simple.

## Add Jackson dependency

In your `build.gradle` file add a dependency to the Ktor Jackson artifact:

```kotlin
dependencies {
    compile "io.ktor:ktor-jackson:$ktor_version"
}
```

This will add the `Ktor` `JacksonConverter` class which can then be used within the standard `ContentNegotiation` feature.

It also includes an implicit dependency on the [Jackson Kotlin Module](https://github.com/FasterXML/jackson-module-kotlin) which must be installed in order for Jackson to handle `data classes` (which do not have an empty default constructor as Jackson expects).

## Install as a Converter

Then tell Ktor to use Jackson for serialization/deserialization for JSON content:

```kotlin
install(ContentNegotiation) {
    jackson {
        // extension method of ObjectMapper to allow config etc
        enable(SerializationFeature.INDENT_OUTPUT)
    }
}
```

which is the same as doing:

```kotlin
install(ContentNegotiation) {
    register(ContentType.Application.Json, JacksonConverter())
}
```

With the converter installed, any request to your Ktor server will be served with a JSON response as long as the `Content-Type` header accepts it.

## Reuse an Existing Mapper

The above configuration is quick and easy, however `ObjectMapper` instances are heavy objects and their configuration is generally shared across various areas of your app. Therefore, instead of creating a new `ObjectMapper` within the Ktor feature itself, initialise one for your application and point Ktor to it. You can then reuse the same mapper when needed without re-initialising it every time:

```kotlin
object JsonMapper {
    // automatically installs the Kotlin module
    val defaultMapper: ObjectMapper = jacksonObjectMapper()

    init {
        defaultMapper.configure(SerializationFeature.INDENT_OUTPUT, true)
        defaultMapper.registerModule(JavaTimeModule())
    }
}
```

then use the alternate syntax to install the converter, passing in our pre-made `ObjectMapper` instance:

```kotlin
install(ContentNegotiation) {
    register(ContentType.Application.Json, JacksonConverter(defaultMapper))
}
```

You are then free to reuse the same `JsonMapper.defaultMapper` object across the rest of your app.
