---
layout: post
title: Kotlin - Things to Improve
tags:
  - kotlin
  - improve
typora-root-url: ..
---

This list isn't very long and doesn't exactly include any game breaking lack of functionality. A good testament to how Kotlin is a solid language these days.

## Try/Multi Catch

A somewhat simple language feature that according to the designers is [still on the cards](https://discuss.kotlinlang.org/t/does-kotlin-have-multi-catch/486/20). Not too much of a problem to live without, but Java has had it for years and it should be a staple of any modern language:

```java
try {
    ...
} catch(SomeException | OtherException e) {
    ...
}
```

The Kotlin version relies on the `when` construct, which has many more levels of nesting and is generally just more ugly to read and write:

```kotlin
try {
    ...
} catch (e: Exception) {
    when(e) {
         is SomeException, is OtherException -> {...}
         else -> throw e
    }
}
```

## Ternary Operator and Collection Literals

These are both [hotly contested](https://discuss.kotlinlang.org/t/ternary-operator/2116), but I personally believe they should be part of Kotlin. All the arguments against the ternary operator seem to revolve around being 'too easy to abuse'. Yeah right. Kotlin has so many other language features which can be abused already (operator overloading anyone? extension functions anyone?), I just don't see why it's such a big deal.

Like it or not, Kotlin is competing against a myriad of other C based languages - all of which have the ternary operator already. Pretty much every developer knows it these days, it should be made available.

Because `if` in Kotlin is an expression, it is termed as the 'acceptable alternative':

```kotlin
val something = if(a < 4) "it's valid" else "not valid"
```

v.s. the syntax everyone and their mum is familiar with:

```java
val something = a < 4 ? "it's valid" : "not valid"
```

Not many characters saved, true. However, when the times comes that I need one (yes because it has it's place), I get angry at having to write the `if` statement - which is just more clunky to write.

Similarly, another highly wanted feature is collection literal syntax. I realise that this might get a bit complicated due to the whole mutable/immutable lists thing in Kotlin, but there are [enough people](https://blog.jetbrains.com/kotlin/2017/06/kotlin-future-features-survey-results/) who want it for a reason. Kotlin is trying to attract developers from the Python/Javascript/Swift worlds, this kind of thing is what will annoy those trying to make the transition.

People are getting on their high horses and spouting the important of 'language principles' and not cluttering the language. Your language principles can be as solid as you want, but if nobody uses it, then what's the point? Developers obviously expect these things - there is [data backing it up](https://blog.jetbrains.com/kotlin/2017/06/kotlin-future-features-survey-results/). Is how I create my lists or perform inline conditionals that much of a big deal to not have both ways of doing it?

## Static

I think the whole `static` and `companion` deal is a bit of a mess in Kotlin. When writing Kotlin on the JVM, the concept of `static` is still very much a thing, and in certain places still a necessity. Want to create a `JUnit` method marked as `BeforeAll`/`BeforeClass`? Yeah, it's just straight up annoying in Kotlin.

To create a simple `static` method in Kotlin, you have to go through the hassle of creating a `companion object`, plus specially annotate the function to tell the compiler to actually make it static. In this case, Java is actually less verbose than Kotlin (and by no small margin) and for what gain? They can do better here to appease those on the JVM.

```kotlin
companion object {
    @JvmStatic
    fun actuallyStatic() = println("That was a chore")
}
```

Now, I don't need static very often, really only for loggers/testing most of the time etc, but it's such a pain to do the above that I prefer the other (less efficient) routes of logger per instance of or a top level variable. It seems like a bit of a tacked on feature to solve this kind of problems and ties into some of the efficiency problems discussed below. Static variables/methods are about as fast as it gets, turns out [companion objects are the complete opposite](https://medium.com/@BladeCoder/exploring-kotlins-hidden-costs-part-1-fbb9935d9b62).

## Efficiency

I don't actually have any real data to back this up, but I think it's common knowledge that the Kotlin compiler isn't the fastest thing ever. To be honest I'm not too surprised, the amount of work it has to do is impressive. Nonetheless, when working on a Kotlin project and going back to Java, the compilation differences are noticeable to say the least. The Kotlin team have, and continue to do a lot of work to improve it though, so I hope it continues to get faster in the future.

Aside from the compiler, I feel the need to rant about generally inefficiencies though. Maybe this is just a reason to moan about we seem to have accepted that it's a good idea to use lambdas and streams literally everywhere. What happened to the good old `for-loop`? Things like streams aren't free. Depending on what you're doing there can be significant allocation going on and other overhead. Kotlin `inline` functions do a good job at resolving this, but they aren't usable everywhere.

There is a [great series here](https://medium.com/@BladeCoder/exploring-kotlins-hidden-costs-part-1-fbb9935d9b62) which covers some of the hidden costs in using some of Kotlin fancy language features. As discussed above, when you define a simple companion object, the compiler generates a bunch of boilerplate and indirection. I just wanted a simple static variable/function, why do I have to have all this extra stuff (yes, really, multiple new classes get generated for this).

There is a widespread movement towards immutability, which don't get me wrong, has many benefits. But it also encourages so much inefficiency. Want to increment that one integer inside this object? Let's copy the whole thing. Hardware continues to improve, yet developers and language designers seem to find a way to add another layer of abstraction to render it moot.

## Too many imports

I've been doing a fair amount of work with [Ktor](https://ktor.io/) and [Exposed](https://github.com/JetBrains/Exposed) recently, and can't help but think that extension functions are getting massively abused at this point (already). Don't get me wrong, they are great and the syntax they allow for is a big selling point, but when you start using some of these libraries, you realise that everything and their dog is a top level extension function. Literally everything.

Take the following snippet which defines a simple Ktor web service for example. The actual logic portion is nice and neat, but at the top we have 22 (!) imports.

```kotlin
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import io.ktor.application.call
import io.ktor.http.HttpStatusCode
import io.ktor.http.cio.websocket.Frame
import io.ktor.request.receive
import io.ktor.request.authorization
import io.ktor.request.receiveMultipart
import io.ktor.response.respond
import io.ktor.response.etag
import io.ktor.response.header
import io.ktor.response.respondFile
import io.ktor.response.respondText
import io.ktor.routing.Route
import io.ktor.routing.delete
import io.ktor.routing.param
import io.ktor.routing.get
import io.ktor.routing.post
import io.ktor.routing.put
import io.ktor.routing.route
import io.ktor.websocket.webSocket
// before any of our actual app imports

...
// implementation at https://github.com/raharrison/kotlin-ktor-exposed-starter/blob/master/src/main/kotlin/web/WidgetResource.kt
```

Kotlin has import * syntax, which the library makers tell everyone to use, but didn't we previously agree that this was a bad idea? Something about having to 'explicitly define your dependencies' or something? But hey, as long as we get our nice builder syntactic sugar, lets just make IntelliJ fold it up and forget it ever happened.
