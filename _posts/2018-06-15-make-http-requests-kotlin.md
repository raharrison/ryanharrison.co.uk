---
layout: post
title: Make HTTP Requests in Kotlin
tags:
  - kotlin
  - http
  - request
  - ktor
  - fuel
---

These days making `HTTP` requests in any language is a staple of many common workflows and features. This post will go through a few of the methods in which you can make such requests in Kotlin using some of the great open source libraries available.

## [Fuel](https://github.com/kittinunf/Fuel)

Probably the most commonly used library for this requirement, [Fuel](https://github.com/kittinunf/Fuel) is fully featured and stable for any such use case. The default settings used are also good so it requires very little/if any configuration to get up and running.

The base of the library sits on extension functions of `String` - which in this case represent `URL`. This makes the interface very fluent any easy to read.

Fuel also makes use of the [Result](https://github.com/kittinunf/Result) library - written by the same creator - to bundle up error conditions and responses. This does mean another dependency to add, but it makes error handling a bit easier. The recommended method is done through a `when` expression:

```kotlin
"http://httpbin.org/get".httpGet().responseString { request, response, result ->
  when (result) {
    is Result.Failure -> {
      val ex = result.getException()
    }
    is Result.Success -> {
      val data = result.get()
    }
  }
}
```

The underlying requests are performed on a dedicated thread pool making the library capable of both blocking and asynchronous requests.

You can also perform synchronous requests if you want:

```kotlin
val (request, response, result) = "http://httpbin.org/get".httpGet().responseString() // result is Result<String, FuelError>
```

Take a look at the docs to find examples of how to use authentication, `POST` etc requests, parameters support, and timeouts etc. The API is configured in a fluent manner:

```kotlin
"http://httpbin.org/get".httpGet().timeout(timeout).timeoutRead(timeoutRead).responseString { request, response, result -> }
```

## [Ktor Client](https://ktor.io/clients/http-client.html)

Another approach is to make use of the newer [Ktor](https://github.com/ktorio/ktor) library. Although the main focus has been on the server-side area, it also includes another package to perform non-blocking requests in a similar fashion. As `Ktor` is based around Kotlin coroutines, this perhaps makes most sense if you are more familiar/are already using them in your project.

`Ktor` includes multiple methods of requests. The main being `Apache`, but `CIO` (Coroutine IO) and `Jetty` handlers are also available. Configuration is done through a fluent, builder-like API very similar to that used in the `Ktor` server packages.

```kotlin
val client = HttpClient(Apache) {
    install(JsonFeature) {
        serializer = GsonSerializer()
    }
}
val htmlContent = client.get<String>("https://en.wikipedia.org/wiki/Main_Page")
```

Note that in this case, `get` is a `suspending` function so you would have to call it within a coroutine. Using `runBlocking` or `async` are the most suitable candidates and means that, unlike `Fuel`, you have complete control over which thread pool is used for the requests.

```kotlin
suspend fun parallelRequests() {
    val client = HttpClient(Apache)
    
    // Start two requests asynchronously.
    val req1 = async { client.call("https://127.0.0.1:8080/a").response.readBytes() }
    val req2 = async { client.call("https://127.0.0.1:8080/b").response.readBytes() }
    
    // Get the request contents without blocking threads, but suspending the function until both
    // requests are done.
    val bytes1 = req1.await() // Suspension point.
    val bytes2 = req2.await() // Suspension point.
}
```

The `Apache` engine is based on Apache `HTTPComponents` and supports the widest variety of config options. It is also the only engine to support redirects and HTTP/2. It will bring in apache as a dependency though. The `CIO` engine is more basic but has no extra dependencies.

Much like you would expect from any HTTP library, you can configure cookies, authentication, timeouts etc as needed.

## Native URL

If you don't want to use a dedicated library, don't want to do any custom configuration, then Kotlin includes a nice extension method on the `URL` class to perform `GET` requests via opening a `stream`.

```kotlin
val response = try {
        URL("http://google.co.uk")
                .openStream()
                .bufferedReader()
                .use { it.readText() }
```

Other notable mentions include:

[khttp library](http://khttp.readthedocs.io/en/latest/)

[natively using HttpURLConnection](https://stackoverflow.com/questions/46177133/http-request-in-kotlin) as you would in Java