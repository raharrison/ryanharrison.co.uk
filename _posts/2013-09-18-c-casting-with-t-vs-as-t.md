---
layout: post
title: 'C# &#8211; Casting with (T) vs. as (T)'
tags:
  - 'c#'
  - casting
---
In C# there are two methods for casting:

  1. `(T)` works with both value and reference types. It casts the object to `T`, and throws an `InvalidCastException` if the cast isn&#8217;t valid.  
    e.g &#8211; `Foo obj = (Foo) bar;`
  2. `as (T)` works only with reference types. It returns the object casted to `T` if it succeeds, and `null` if the cast isn&#8217;t valid.  
  e.g &#8211; 
  {% highlight csharp %}
Foo obj = bar as Foo;  
if(obj == null)
{  
  // the cast did not succeed so proceed accordingly  
}  
{% endhighlight %}

The question therefore is which one should be used where?

Using `(T)` means that you fully expect the cast to succeed. If it doesn&#8217;t succeed then there is an error in the code that needs looking at.

Using `as (T)` on the other hand means that you do not fully expect the cast to succeed in every case. It is considered normal behaviour if the cast did not succeed and this would be taken care of through a null check afterwards.

The only mistake is when you use `as (T)` but do not follow it up with a null check. The developer fully expects the cast to succeed so doesn&#8217;t write the null check. However later down the line when something goes wrong, no exception is thrown on the invalid cast, no null check is performed, and you have yourself a bug that is hard to track down. It is best to always use the regular cast `(T)` unless you intend to check yourself for the invalid cast via `as (T)` and a null check afterwards.