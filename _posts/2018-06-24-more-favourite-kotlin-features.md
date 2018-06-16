---
layout: post
title: More Favourite Kotlin Features
tags:
  - kotlin
  - features
  - favourite
---

This post is a continuation of a [previous post]({{ site.baseurl }}{% post_url 2018-05-13-favourite-kotlin-features %}) on some of my favourite language feature in Kotlin.

## Higher Order Functions and First Class Lambdas

- pass functions as blocks of code
- don't need parens if last param
- nice syntax no functional interface
- it for only param ref.

## Top Level Functions and Multi-Class Files

- You can have functions on the top level defined outside of any class
- A source file can have many top level definitions or classes defined
- No need for Utils classes - just have as top level instead in own file
- Gets around a lot of files with no contents in Java e.g interfaces and multiple implementations all short

## Null Safety

```
val str:String = "name"
str = null // As str is defined as null save it will show error
str.length
```



## Default and Named Arguments

```
fun argumentValid(num: Int, str: String = "12") {
}
//All 3 are valid
argumentValid(15, "Hey")
argumentValid(str = "Name", num = 45) //Named argument
argumentValid(45) //usage of default argument
```

## Coroutines

- suspend
- async
- channels
- dispatchers
- compiler generated state machines