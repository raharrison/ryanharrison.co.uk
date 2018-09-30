---
layout: post
title: Java 11 HTTP Client API
tags:
  - java
  - jdk
  - http
  - client
typora-root-url: ..
---

One of the more noteworthy features of the new [Java/JDK 11](http://jdk.java.net/11/) release is the new `HttpClient` API which has been in incubator status since JDK 9. Previously, the process of sending and retrieving data over `HTTP` has been very cumbersome in Java. Either you went through the hassle of using `HttpURLConnection`, or you bring in a library to abstract over it such as the `HttpClient` from [Apache](http://hc.apache.org/index.html). Notably, both solutions would also block threads whilst doing so.

As these days dealing with `HTTP` connections is so common, the JDK finally has a modern API which can deal with these scenarios - including support for `HTTP 2` (server push etc) and `WebSockets`.

## Create a Client

The first step to make use of the new API is to create an instance of the `HttpClient` class. The library itself makes heavy use of the builder pattern to specify configuration options, as is the case in most new Java libraries.

You can configure things like `HTTP` version support (the default is set to `HTTP 2`), whether or not to follow redirects, authentication and a proxy for all requests that pass through the client.

```java
HttpClient client = HttpClient.newBuilder()
      .version(Version.HTTP_2)
      .followRedirects(Redirect.SAME_PROTOCOL)
      .authenticator(Authenticator.getDefault())
      .build();
```

The `HttpClient` instance is the main entry point to send and receive requests (both synchronously or asynchronously). Once created you can reuse them, but they are also immutable.

## Create Requests

An `HTTP` request is represented by instances of `HttpRequest` which holds the URL, request method, headers, timeout and payload (if applicable). By default `GET` is used if no other is specified.

```java
HttpRequest request = HttpRequest.newBuilder()
               .uri(URI.create("https://something.com"))
               .build(); // GET request
```

The following snippet creates a `POST` request with a custom timeout. A `BodyPublisher` must be used to attach a payload to a request - in this case taking a `JSON` String and converting it into bytes.

```java
HttpRequest request = HttpRequest.newBuilder()
      .uri(URI.create("https://something.com/api"))
      .timeout(Duration.ofMinutes(1))
      .header("Content-Type", "application/json")
      .POST(BodyPublishers.ofString(json)
      .build()
```

## Send Requests

Once an `HttpRequest` is created, you can send it via the `HttpClient` previously constructed. Both synchronous and asynchronous operations are supported:

### Sync

The `HttpClient.send` method will perform the `HTTP` request synchronously - meaning that the current thread will be blocked until a response is obtained. The `HttpResponse` class encapsulates the response itself including status code, body and headers.

```java
HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
System.out.println(response.statusCode());
System.out.println(response.body());
```
When receiving responses, a `BodyHandler` is provided to instruct the client on how to process the response body.  The `BodyHandlers` class includes default handlers for the most common scenarios. `ofString` will return the body as an UTF-8 encoded String, `ofFile` accepts a `Path` to write the response to a file and `ofByteArray` will give you the raw bytes.

### Async

One of the best features of the API is the ability to perform completely asynchronous requests - meaning that no thread is blocked during the process. Under the hoods, the implementation uses NIO and non-blocking channels to ensure no blocking IO operations are performed.

The `HttpClient.sendAsync` method takes the same parameters as the synchronous version, but returns a `CompletableFuture<HttpResponse<T>>` instead of just the raw `HttpResponse<T>`. Just as with any other `CompletableFuture`, you can chain together callbacks to be executed when the response is available. In this case, the body of the response is extracted and printed out. [More details here](https://www.callicoder.com/java-8-completablefuture-tutorial/) on how to work with `CompletableFuture`.

```java
CompletableFuture<HttpResponse<String>> future = client.sendAsync(request, 
        BodyHandlers.ofString());

future.thenApply(HttpResponse::body) // retrieve body of response
      .thenAccept(System.out::println); // use body as String
```

Each `HttpClient` has a single implementation-specific thread that polls all of its connections. Received data is then passed off to the executor for processing. You can override the `Executor` on the `HttpClient`, by default it is a cached thread pool executor.

## Kotlin

As the new API sits like any other in the default JDK, you can easily make use of it in your Kotlin projects as well! You can paste in the above examples into IntelliJ to perform the automagical Java-Kotlin conversion, or the below example covers the basics:

```kotlin
val client = HttpClient.newBuilder().build();

val request = HttpRequest.newBuilder()
               .uri(URI.create("https://something.com"))
               .build();

val response = client.send(request, BodyHandlers.ofString());
println(response.statusCode())
println(response.body())
```

### Coroutines (Async)

Things get much more interesting when taking into account the new asynchronous capabilities and [Kotlin coroutines](https://github.com/Kotlin/kotlinx.coroutines/blob/master/coroutines-guide.md). It would be great if we could launch a coroutine which sends the request and suspends until the response is available:

```kotlin
suspend fun getData(): String {
    // above code to construct client + request
    val response = client.sendAsync(request, BodyHandlers.ofString());
    return response.await().body() // suspend and return String not a Future
}

// in some other coroutine (suspend block)
val someData = getData()
process(someData) // just as if you wrote it synchronously
```

No need to deal with chaining together callbacks onto `CompletableFuture`, you get the same procedural code flow even though the implementation suspends and is completely non-blocking.

The magic comes from the `CompletionStage.await()` extension function provided by the coroutines [JDK integration library](https://github.com/Kotlin/kotlinx.coroutines/blob/master/integration/kotlinx-coroutines-jdk8/README.md):

```kotlin
return suspendCancellableCoroutine { cont: CancellableContinuation<T> ->
    val consumer = ContinuationConsumer(cont)
    whenComplete(consumer) // attach continuation to CompletionStage
}
```

[Docs for the function](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-jdk8/kotlinx.coroutines.experimental.future/java.util.concurrent.-completion-stage/await.html).

## More Information

<https://download.java.net/java/early_access/jdk11/docs/api/java.net.http/java/net/http/package-summary.html>

<http://openjdk.java.net/groups/net/httpclient/intro.html>

<https://www.youtube.com/watch?list=PLX8CzqL3ArzXyA_lJzaNmrFqpLOL4aCEz&v=sZSdWq490Vw>
