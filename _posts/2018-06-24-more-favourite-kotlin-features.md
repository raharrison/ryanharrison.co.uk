---
layout: post
title: More Favourite Kotlin Features
tags:
  - kotlin
  - features
  - favourite
---

This post is a continuation of a [previous post]({{ site.baseurl }}{% post_url 2018-05-15-favourite-kotlin-features %}) on some of my favourite language feature in Kotlin.

## Higher Order Functions and First Class Lambdas

Functions are considering first-class citizens in Kotlin. Java 8 introduced the much needed concept of lambdas and functional interfaces, which bring large improvements to the language, but Kotlin brings in some more great syntax which further improves the experience.

In Java, if you want to pass in a block of code, or return one, you have to start dealing with instances of `Function`, `Predicate` etc. This is fine, but not terribly readable when it's really just following the convention of first type params are arguments, last is the return type - e.g. `Function<String, String, String, Integer>`. In Kotlin, the concept of a lambda is much more deeply integrated into the language. If you wanted to pass in the equivalent of the above `Function` in Kotlin, you would specify the type of the argument as a lambda expression:

```kotlin
fun work(job: (String, String, String) -> Int) {
    // call job as you would think, not .call()
    job("a", "b", "c)
}
```

The same can be used if you want to return a function from a function:

```kotlin
fun getPrinter(): (String) -> Unit = { println(it) }
```

Note above that you don't even need to specify the return type, Kotlin will infer it by itself. It also makes use of `it` which is a special variable which refers to the first argument of the lambda.

The syntax gets even nicer when you start calling functions which take a lambda with one argument as its last parameter. Take the `.also` method which you can call on `Any` object:

```kotlin
val str = "something".also((s) -> {
    println(s)
})
// simplify using 'it' to refer to the parameter
val str = "something".also({
    println(it)
})
// simplify by removing parenthesis as last argument is a lambda
val str = "something".also {
    println(it)
}
```

Such syntax enables the use of some really nice builder API's. Take [kotlinx.html](https://github.com/Kotlin/kotlinx.html) with code taken from the [ktor-samples](https://github.com/ktorio/ktor-samples/tree/master/app/youkube):

```kotlin
h2 { +"Login" }
form(call.url(Login()) { parameters.clear() }, classes = "pure-form-stacked", method = FormMethod.post) {
    acceptCharset = "utf-8"
    label {
        +"Username: "
        textInput {
            name = Login::userName.name
            value = it.userName
        }
    }
    label {
        +"Password: "
        passwordInput {
            name = Login::password.name
        }
    }
    submitInput(classes = "pure-button pure-button-primary") {
        value = "Login"
    }
}
```

Or even simply working with lists. In Java, `streams` have helped significantly, but in Kotlin it's still much more expressive and neat (coupled with the addition of new helper extension methods in the standard library):

```kotlin
val numbers = arrayListOf(10, 5, -9, 9, 11, 5, -6)
numbers.filter { it >= 0}
numbers.forEach { println("${it * 2} ") }
numbers.map { it * 2 }.filter { it > 10 }.forEach { println(it) }
```

The same `::` method reference syntax as Java is available in Kotlin to refer to functions within the same/different scopes. Kotlin also introduces the concept of `inline` functions however (just like `also` as described above). This reduces any overhead that would otherwise be brought in when passing around method references, as the compiler merely copies and pastes it to the call site. Note that Kotlin also does have similar functional interface classes to Java - `KFunction<T>` etc.

The improvements made to lambdas in Kotlin make passing around and dealing with them in general much easier and more attractive to developers. You just have to take a look at any popular Kotlin library to see how widely the concept is utilised within the language. I think that much of the improved readability and expressiveness of Kotlin can be in some way attributed to this feature.

## Null Safety

Another one of the flagship features of Kotlin. The whole concept of nullability is handled very differently in Kotlin compared to say Java. In Java, any reference variable can be nullable. This allows for a lot of flexibility, but introduces a whole mess of dreaded `NullPointerException`. This may not seem like a huge issue, but when they make up the [highest proportion of Exceptions](https://blog.samebug.io/which-java-exceptions-are-the-most-frequent-f830b113c37f) generated from Java software (by quite some margin), then it's clear that a better solution is needed.

In Kotlin you have to be explicit. An equivalent variable of type `String` for example in Kotlin must be given a value at definition. Even if it's a `var` it cannot be given a `null` value. Of course, if you don't have the concept of `null`, then you can't get `NullPointerExceptions`!

```kotlin
val str:String = "name"
str = null // Compile-time error
str.length // will never generate a null pointer exception
```

However, having the concept of 'no value' is actually quite useful. In Kotlin you *can* assign `null` to a variable, but you have to explicitly define that capability in the variable definition, and more importantly you have to perform a null check every time you use the variable. In Java-land the equivalent would be using the `Optional<T>` class in the standard library.

```kotlin
val str:String? = "name"
str = null // now accepted
str.length // compile-time error as str might be null
str?.length // safe call operator for easy null check
```

You can define a nullable variable by appending a `?` to the end of the variable definition. Now it can accept `null` as a value, but any time you use that variable you will need to do a null check to prevent exceptions. Kotlin provides some handy concepts to make handling `null` easier:

```kotlin
str?.length // length if str is not null, otherwise null
val lengthOrZero = str?length ?: 0 // length if str is not null, otherwise zero (elvis operator)
str?.let {
    // use as it.length etc (inlined function with null check)
    // it is smart cast to String not String?
}
```

Another killer feature is that Kotlin also performs smart type casting to prevent casting to the non-nullable type:

```kotlin
if(str != null) {
    val length = str.length // str is now String not String?
}
```

## Default and Named Arguments

Gone are the days of needing to write boilerplate function overloads when you want to provide some default or optional values. Similar to how languages such as Python have done for years, Kotlin allows default values for function arguments and named arguments when calling functions:

```kotlin
fun foo(num: Int, str: String = "12") {
}
//All 3 are valid
foo(15, "Hey")
foo(str = "Name", num = 45) //Named argument
foo(45) //usage of default argument
```

In Java the equivalent of the above would be:

```java
void foo(int num, String str) {
}

void foo(int num) {
    foo(num, "12")
}
```

A nice feature to improve clarity and reduce boilerplate. In the example above, the Java version isn't so bad, but the problem grows exponentially as you add arguments.

This post has again got quite long, but there are even more items I can discuss in a part 3.