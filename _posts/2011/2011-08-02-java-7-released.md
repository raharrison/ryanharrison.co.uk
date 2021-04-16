---
layout: post
title: Java 7 Released
tags:
  - java
  - sdk
---
A few days ago Oracle announced the availability of their new Java 7 SDK. Some of of the major changes include -;

  * New I/O APIs (Asynchronous I/O)
  * Strings in switch statements
  * Unicode 6.0
  * Elliptic-curve cryptography
  * Translucent and shaped windows
  * Heavyweight/lightweight component mixing
  * Swing Nimbus look-and-feel
  * Swing JLayer component
  * The integral types (byte, short, int and long) can also be expressed using the binary number system. To specify a binary literal, add the prefix `0b` or `0B` to the number.
  * Any number of underscore characters (`_`) can appear anywhere between digits in a numerical literal. This feature enables you, for example, to separate groups of digits in numeric literals, which can improve the readability of your code.
  * You can replace the type arguments required to invoke the constructor of a generic class with an empty set of type parameters (`<>`) as long as the compiler can infer the type arguments from the context. This pair of angle brackets is informally called the diamond.
  * A single catch block can handle more than one type of exception. This enables you to specify more specific exception types in the throws clause of a method declaration and reduces code repetition.
  * The try with-resources statement is a try statement that declares one or more resources. A resource is an object that must be closed after the program is finished with it. The try with-resources statement ensures that each resource is closed at the end of the statement.
  * Java API for XML Processing (JAXP) 1.4.5.

[JDK 7 Release Notes][1]

[Download Link][2]

[1]: http://www.oracle.com/technetwork/java/javase/jdk7-relnotes-418459.html
[2]: http://www.oracle.com/technetwork/java/javase/downloads/index.html