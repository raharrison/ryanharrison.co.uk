---
layout: post
title: Even More Favourite Kotlin Features
tags:
    - kotlin
    - features
    - favourite
---

This post is a continuation of a [previous post]({{ site.baseurl }}{% post_url 2018/2018-06-24-more-favourite-kotlin-features %}) on some of my favourite language feature in Kotlin.

## Coroutines

Not technically a language feature, as most of it is implemented as a [library](https://github.com/Kotlin/kotlinx.coroutines) (which is cool in itself when you see the syntax), but still very useful. Dealing with `Threads` in Java has long been a bit of a pain point. The situation has got significantly better with the introduction of API's such as `ExecutorService` and now `CompletableFuture`, but the syntax isn't all that readable and you end up with `RxJava` like messes of chained method calls and lambdas everywhere.

Coroutines can be thought of as very lightweight threads - you can spawn thousands of coroutines without crashing your program because, unlike threads, they don't consume any OS level resources. In Kotlin, coroutines revolve around the concept of functions which can `suspend`. That is, at some point they can be suspended and the thread that was running it can go off and run something else. Later on, the coroutine can resume (maybe on a different thread) with new values and as if nothing ever happened. Under the hoods, similarly to C# `async/await`, the compiler generates a simple state machine which handles the suspension and resumption of these functions.

The great benefit of this is that your asynchronous code looks just like you would write it synchronously - no dealing with the threading model directly or chaining callbacks together. It also makes error handling much easier to deal with.

```kotlin
suspend fun someWork(): String {
    // call a web service, do some calculation etc
}

suspend fun worker() {
    val first = async { someWork() }
    val second = async { someOtherWork() }
    println("The answer is ${first.await() + second.await()}") // suspension point
}
```

In the example above, `worker()` will launch two coroutines to perform the two `async` blocks. By default, the coroutine `dispatcher` uses the shared `ForkJoinPool` which is where we get the real parallelisation from. In the `println` statement, the results are 'awaited'. At this point, if the result is not immediately available, execution suspends and the thread is free to do something else. When the `async` block returns, `worker()` is resumed and the `println` can continue (maybe suspending again on the second `await()`).

You can also do simpler things like just launching a background coroutine to do some work if you are not interested in the result:

```kotlin
launch {
    // do some work
    delay(100) // not Thread.sleep()
    // coroutines use a special version which is non-blocking
}
```

The key factor is that you want to avoid blocking threads. In Java multithreading scenarios, this is much more common - maybe you block waiting for a queue to fill or until a web request is finished. With Kotlin coroutines you don't have to block the entire thread - you suspend the coroutine instead and the thread is free to continue doing other work. This is especially handy in web frameworks such as [Ktor](https://github.com/ktorio/ktor) which is built around coroutines.

This is just scraping the surface of what the coroutines library has to offer -

-   channels (think pub/sub)

-   support for custom dispatchers and contexts (restrain execution to your thread pool etc)

-   full support for cancellation and error handing

-   actors, producers and select expressions

The [introductory guide](https://github.com/Kotlin/kotlinx.coroutines/blob/master/coroutines-guide.md) is a great read if you want to learn more. In effect, they are similar to Go-routines and a lot more powerful than C# `async/await`. If you read the guide you can see the multitude of use cases which can be easily parallelised or made non-blocking.

## Top Level Functions and Multi-Class Files

When you've got so many language constructs to remove boilerplate code and verbosity, it doesn't make sense to force developers into having only one class per file. Thankfully, unlike Java, no such restriction is forced in Kotlin - you can have as many public classes, functions, definitions in one file as you want. When you have a lot of `data classes` or `sealed classes`, it makes life a lot simpler to bundle up similar classes into one file. When you go back to Java, it's one thing that starts to get on your nerves that you may have never thought about before:

```kotlin
// All in one file
data class Foo(val bar: String)
data class Baz(val foo: Int)

class Printer {
    fun print(s: String) = println("Printer is printing $s")
}

sealed class Operation {
    class Add(val value: Int) : Operation()
    class Substract(val value: Int) : Operation()
}
```

You may have noticed that I said 'top-level functions' before. Yes, that's right, in Kotlin a function doesn't have to belong to a class - you can have it sitting with other related functions in their own file, or anywhere you want.

There is no need to have `Utils` classes anymore. You can (and should) name you source files as such, but the utilities themselves can sit in them without a class definition. And they can be used without referring to such a class:

```kotlin
// StringUtils.kt
fun replaceCommas(s: String) = s.replace(",", ".")
// and more helpers

// Work.kt
import StringUtils.replaceCommas
fun work() {
    println(replaceCommas("Some text, goes here"))
}
```

Even though Kotlin _does_ have a language feature that could support a similar utils pattern you would see in Java - the `object` keyword - top-level helper functions are much neater.

It might not seem like much, but it really can dramatically reduce the overall number of source files you have to deal with. A common case is where you define a short interface and a couple of implementations. In Java they would have to be split into 3 separate `.java` files, regardless of the fact that it might all be 50 lines long. In Kotlin, you can put everything into one file.

## Destructuring Declarations

Not quite Python-like multi-value returns from functions, but still some nice syntax to retrieve variables from data classes returned from your functions.

```kotlin
data class Student(val name: String, val age: Int)
fun getStudent(): Student {
    return Student("John", 22)
}
val (name, age) = getStudent()
println(name)
println(age)
```

## Singleton (Object)

Another Kotlin feature which I like is the simplicity of defining a “singleton”. Consider the following example of how a singleton could be created in Java and then in Kotlin.

```java
public class SingletonInJava {

    private static SingletonInJava INSTANCE;

    public static synchronized SingletonInJava getInstance() {
        if (INSTANCE == null) {
            INSTANCE = new SingletonInJava();
        }
        return INSTANCE;
    }
}
```

```kotlin
object SingletonInKotlin {
}

// And we can call
SingletonInKotlin.doSomething()
```

Kotlin has a feature to define a singleton in a very clever way. You can use the keyword `object`, which allows you to define an object which exists only as a single instance across your app. No need to worry about initialising your instance of thread safety, everything is handling by the compiler.
