---
layout: post
title: Favourite Kotlin Features
tags:
  - kotlin
  - features
  - favourite
---

Kotlin has many great language features which, in my view, put it way ahead of Java in terms of expressiveness and overall productivity. Here are a few of the notable examples:

## Full Java Interop

This is probably the key factor to widespread adoption of Kotlin - and something that most new languages struggle with when trying to gain usage. One of the major design decisions of Kotlin is that it has full compatibility with Java. This isn't like languages such as `Scala` or `Groovy`, which although compile down to the same bytecode and run on the `JVM`, cannot interact with Java code or make use of libraries written in Java.

When you start a Kotlin project, IntelliJ also probably created a similar Java source folder in the root of your project. This signifies a key point in that you can have both Kotlin and Java code right in the same project, talking to each other and compiling at the same time. No fancy tooling needed, it just works as you would expect. Kotlin supports or has variants for every Java language feature meaning there is full interop between the two.

For example take the following Java class:

```java
public class Foo {
    public void sayInJava(String something) {
        System.out.println("Said in Java: " + something);
    }
}
```

Maybe this is in a library `.jar` file somewhere and just referenced in your project. In Kotlin you can call the Java code just like you would your Kotlin code:

```kotlin
fun say() {
    val foo = Foo()
    foo.sayInJava("from Kotlin")
}
```

This is cool and all, but the great thing about this is that from day one Kotlin has fantastic 3rd party library support. Everyone knows that there is pretty much a library for everything in Java-land - well you get to use each and every one of those in your Kotlin code for free. This massively lowers the barrier to entry for Kotlin compared to so many other languages when you have extremely stable libraries at your disposal:

- Apache commons and all the rest of them
- Guava, collections etc
- Kafka, ElasticSearch, Hadoop etc
- Spring Framework (which now has first class Kotlin support)
- Hibernate, JooQ
- Logback, Log4j, AssertJ, Hamcrest
- The list goes on, and this doesn't even include Kotlin specific libraries!

This feature also means that you don't have to go head first into Kotlin for new or existing projects. There are a lot of developers on larger systems who have begun migrating over data classes and tests to Kotlin, leaving the core business logic in Java. That's perfectly feasible and probably recommended to keep it slow and appease those who are less than emphatic about using a new language.

## Data Classes

Probably one of the headline features in Kotlin - and it really does save you so much boilerplate. In Java, writing basic `POJO` classes is easy, but requires tons of boilerplate, even if the IDE can generate it for you. It litters up your codebase and makes your classes unnecessarily long and unreadable. For example a basic data class in Java could look like:

```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() {
        return name;
    }
     
    // other getters and setters
   
    // equals and hashcode generated
    
    // generated toString()
    
    // clone/copy method
}
```

That's a massive amount of code just to define a simple `Person` with a couple attributes. In Kotlin however, we can do it in one line:

```kotlin
data class Person(val name: String, val age: Int)
```

This one line is equivalent to all that code above. The `data` keyword will instruct the compiler to generate the following for all attributes:

- constructor to set all attributes (in this case they are `val` so are immutable)
- getters (optional setters if `var`) for all attributes - implemented as Kotlin `properties`
- `equals` and `hashcode` methods
- `toString` method
- `copy()` method similar to cloning in Java

## Extension Functions

This is another key feature of Kotlin that puts it above a lot of the competition. Similarly to `C#` (just with additional benefits) you can add your own methods and properties to classes without modifying their actual definition. The most common case is where you don't have access to the source of the target class (e.g `String` or `Int`), but want to keep the nicer syntax of operating directly on the object. For example, take the method `countMatches` of Apache Commons Lang:

**Java**

```java
int count = StringUtils.countMatches("some string", "s");
```

**Kotlin**

In Kotlin we can define an extension function which simply delegates down:

```kotlin
fun String.countMatches(s: String) = StringUtils.countMatches(this, s)
// then
val count = "some string".countMatches("s")
```

A simple example, but this concept gets used everywhere within the Kotlin standard library e.g:

```kotlin
public fun CharSequence.lineSequence(): Sequence<String> = splitToSequence("\r\n", "\n", "\r")

public fun CharSequence.lastIndexOfAny(strings: Collection<String>, startIndex: Int, ignoreCase: Boolean): Int = findAnyOf(strings, startIndex, ignoreCase, last = true)?.first ?: -1
```

Extension functions in Kotlin are really nothing more than compiler magic. If you look at the bytecode level, they are nothing more than `static` functions which take `this` as a first param (really just like every other method). The Kotlin compiler just allows us to use this nicer syntax in order to call such functions. Or the really handy one to convert a Java `Stream` to a list without going through the verbosity of `.collect(Collectors.toList())`:

```kotlin
public fun <T> Stream<T>.toList(): List<T> = collect(Collectors.toList<T>())
```

If that's not a reason to like extension functions, I don't know what is.

This is similar behaviour to how extension functions work in C#, but in Kotlin there is another way they can be used - as parameters to functions. Take the commonly used `apply` function as defined below. This can operate on any `T` (any object) and takes in one function as a parameter. This is no normal function though - it's an extension function of `T` (the class it operates on).

```kotlin
fun <T> T.apply(block: T.() -> Unit): T {
    block()
    return this
}
```

This has a very cool advantage in that the scope of the function is local to the class - e.g you have access to all the members:

```kotlin
val person = Person().apply {
    firstName = "Bill"
    secondName = "Smith"
    age = calculateAge()
}
```

A somewhat simple example, but it provides a really nice syntax for the `builder` pattern as described in [this article](https://kotlinlang.org/docs/reference/type-safe-builders.html). And it gets used all over the place in newer Kotlin libraries. Take a route definition in [Ktor](http://ktor.io/) for example (take a look at [this post]({{ site.baseurl }}{% post_url 2018-04-14-kotlin-ktor-exposed-starter  %}) on how to get started with `Ktor`):

```kotlin
route("/widget") {
	get("/") {
    	call.respond(widgetService.getAllWidgets())
	}
}
```

The `route` function itself is an extension function of the `Route` class and so we have access to other builders on top of the `Route` - in this case `get` which adds an interceptor. `get` itself takes in an extension function as a lambda which is how it is able to get a handle on the `call` variable amongst others.

## String Templating

A simple one, but very useful. Gone are the days of concatenating a bunch of small strings and variables together using `+` in Java, instead we can just use a template:

**Java**

```java
System.out.println("A = " + a + ", B = " + b + "C = " + c)
```

**Kotlin**

```kotlin
println("A = $a, B = $b, C = $c")
```

You can also directly call methods on the referenced variables:

```kotlin
println("Result is ${res.getResult()}")
```

**And More**

This post as gotten quite long so there are still plenty of other points I want to mention in a part 2.