---
layout: post
title: 'C# – String concatenation instead of StringBuilders'
tags:
  - 'c#'
  - efficiency
  - string
  - tip
---
In C# when you concatenate two strings together you are implicitly creating a lot of strings in memory – more than you would have thought. For example consider the code:

{% highlight csharp %}  
List<string> values = new List<string>() {"foo ", "bar ","baz"};
string output = string.Empty;
foreach (var value in values)
{ 
    output += value; 
} 
{% endhighlight %}

Behind the scenes new strings are created for each portion of the resulting string in completely different memory locations through inefficient copy operations. So in total in this one line we have created: `1. "foo" 2. "bar" 3 "baz" 4 "foo bar" 5. "foo bar baz"` In just one seemingly simple concatenation loop 5 strings have been created which of course is wildly inefficient. The problem gets a lot worse when you end up concatenating hundreds of strings together in a loop like this. The solution is to use `StringBuilders`. The above code is converted into: 

{% highlight csharp %} 
List<string> values = new List<string>() {"foo ", "bar ","baz"};
StringBuilder builder = new StringBuilder();
foreach (var value in values)
{
    builder.Append(value);
} 
{% endhighlight %} 

Using this method is a lot more efficient thanks to the fact that `StringBuilders` keep the same position in memory for their strings and do not perform inefficient copy operations each time a new string is appended (for example number 4 from above would not be created in a completely separate memory location). This makes `StringBuilders` very useful when concatenating many strings at once. But that doesn't mean go replace all of your string concatenation code with StringBuilders right away. There are some situations where explicitly using a StringBuilder can make the situation worse. For example: 

{% highlight csharp %}
string result = "foo " + "bar " + "baz";
{% endhighlight %} 

You might think that this suffers with the same inefficiencies as in the first example but in fact it doesn't at all. The difference is that compile-time concatenations (which is what's happening here) are automatically translated by the compiler into the appropriate calls to `String.Concat()` (which is the fastest way). Adding a `StringBuilder` would essentially be ruining the optimisations made by the compiler. The use of `StringBuilder` should be reserved to building complex strings at runtime – not replacing compile time concatenations.