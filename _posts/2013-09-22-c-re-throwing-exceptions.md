---
layout: post
title: 'C# – Re-throwing Exceptions'
tags:
  - 'c#'
  - exception
  - throw
  - tip
---
In C# it is common that exceptions are re-thrown after some logging has taken place, or perhaps even to alter the exception information to be more user friendly. However there are two different ways of re-throwing exceptions in C# and care needs to be taken when doing so, as one method will loose the stack trace – making things a lot harder to debug.

Consider the following code:

{% highlight csharp %}  
using System;

namespace ScratchPad  
{  
    internal class Throwing  
    {  
        // Some method which can throw an exception  
        static void DoSomething()  
        {  
            throw new Exception("Something bad happened");  
        }

        // Another method which tries calling the other method, catching an exceptions it may throw  
        static void Run()  
        {  
            try  
            {  
                Console.WriteLine("Trying to run DoSomething()");  
                DoSomething();  
            }  
            catch (Exception e)  
            {  
                // We caught the exception. Typically some logging is taken place here  
                Console.WriteLine("We caught an exception in DoSomething(). Message = " + e.Message);  
                Console.WriteLine("Re throwing the exception after logging");

                // We then re-throw the exception  
                throw e;  
            }  
        }

        static void Main()  
        {  
            try  
            {  
                // Run the method  
                Run();  
            }  
            catch (Exception e)  
            {  
                // We catch the exception here and examine its stack trace  
                Console.WriteLine("We caught the exception. Stack trace is");  
                Console.WriteLine();  
                Console.WriteLine(e.StackTrace);  
            }

            Console.ReadLine();  
        }  
    }  
}  
{% endhighlight %}

This is pretty self-explanatory. We have a method that runs another method and catches any exceptions it may throw (in this case one will be thrown every time). In the catch block we examine the exception, perhaps do some logging and re-throw the exception for the caller to handle. Finally in Main the re-thrown exception is caught again and the stack trace is examined.

At first look there is nothing wrong with this code, it’s all pretty commonplace, nothing much to see here. However this is the output that we get:

{% highlight text %}  
Trying to run DoSomething()  
We caught an exception in DoSomething(). Message =: Something bad happened  
Re throwing the exception after logging  
We caught the exception. Stack trace is

at ScratchPad.Throwing.Run() in C:\Code\ScratchPad\ScratchPad\Program.cs:line 28  
at ScratchPad.Throwing.Main() in C:\Code\ScratchPad\ScratchPad\Program.cs:line 37  
{% endhighlight %}

You may or may not have noticed that this is not the full stack trace. We can see that the exception came from `Run()`, however we can’t tell that in actual fact the exception originated from `DoSomething()` at all. This may or may not cause problems when debugging as now instead of going straight to the route cause, you first have to go through `Run()`.

We lose the top of the stack trace because we used

{% highlight csharp %}  
throw e;  
{% endhighlight %}

Which essentially resets the stack trace to now start in that method. This makes sense as this is really the same as doing something like:

{% highlight csharp %}  
throw new Exception(e.Message);  
{% endhighlight %}

But what if we wanted to see the whole stack trace? Well instead of using `throw e;` we just use:

{% highlight csharp %}  
throw;  
{% endhighlight %}

With the updated catch block:

{% highlight csharp %}  
catch (Exception e)  
{  
    // We caught the exception. Typically some logging is taken place here  
    Console.WriteLine("We caught an exception in DoSomething(). Message = " + e.Message);  
    Console.WriteLine("Re throwing the exception after logging");

    // We then re-throw the exception  
    throw;  
}  
{% endhighlight %}

We get the output:

{% highlight text %}  
Trying to run DoSomething()  
We caught an exception in DoSomething(). Message = Something bad happened  
Re throwing the exception after logging  
We caught the exception. Stack trace is

at ScratchPad.Throwing.DoSomething() in C:\Code\ScratchPad\ScratchPad\Program.cs:line 10  
at ScratchPad.Throwing.Run() in C:\Code\ScratchPad\ScratchPad\Program.cs:line 28  
at ScratchPad.Throwing.Main() in C:\Code\ScratchPad\ScratchPad\Program.cs:line 37  
{% endhighlight %}

We now have the full story in the stack trace. We can see that the exception originated from the `DoSomething()` method and passed through the `Run()` method into `Main()` – much more helpful when debugging.

I don’t see any situation when using `throw e;` would be of any use at all. If you wanted to hide the stack trace then you would typically be throwing a completely new exception anyway – with a new message and perhaps other information to pass to the caller. If you didn’t want to hide the stack trace then throw; is the statement to use. Resharper even sees `throw e;` as a problem and tries to replace it with the simple throw;.

Even so I bet this mistake has been made a lot of times by a lot of people. So remember if you are wanting to re-throw an exception, never use throw e; as it will loose your stack trace. Instead always use `throw;`.