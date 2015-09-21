---
layout: post
title: 'C# – Write code indirectly using reflection'
tags:
  - 'c#'
  - reflection
---
You can use the reflection features in C# to write your normal code in an indirect manner. No idea why you would want to do something like this, but it gives an idea of the control you get when using reflection.

In this example we have a small class wrapping two integers inside their own properties. First of all an object is created, the properties set, and the `.ToString()` method result passed into a `Console.WriteLine` using the conventional way. The exact same thing happens again but now indirectly through the use of reflection. As you can see it takes up nearly three times more code to to the exact same thing using reflection but you at least get the same result.

{% highlight csharp %}  
class Program  
{  
    static void Main()
    {  
        Console.WriteLine("Using normal method:\n");

        // Normal method of instantiation and calling methods  
        Foo obj = new Foo();  
        obj.First = 36;  
        obj.Second = 83;  
        Console.WriteLine(obj.ToString());

        Console.WriteLine("\nUsing reflection:\n");  
        Type fooType = typeof (Foo);

        // Get an instance of the class  
        Foo fooInstance = (Foo) Activator.CreateInstance(fooType);

        // Get and set values of the two int properties  
        PropertyInfo firstPropInfo = fooType.GetProperty("First", typeof(int));  
        PropertyInfo secondPropInfo = fooType.GetProperty("Second", typeof(int));

        firstPropInfo.SetValue(fooInstance, 36, null);  
        secondPropInfo.SetValue(fooInstance, 83, null);

        // Run the ToString method on the object  
        MethodInfo toStringInfo = fooType.GetMethod("ToString");  
        string toStringResult = (string) toStringInfo.Invoke(fooInstance, null);

        // Run Console.WriteLine using the ToString result  
        MethodInfo writeLineInfo = typeof (Console).GetMethod("WriteLine", new[] {typeof(string)});  
        writeLineInfo.Invoke(null, new[] {toStringResult });  
    }  
}

class Foo  
{  
    public int First { get; set; }  
    public int Second { get; set; }

    public override string ToString()  
    {  
        return "First = " + First + ", Second = " + Second;  
    }  
}  
{% endhighlight %}

**Output**:

{% highlight text %}  
Using normal method:

First = 36, Second = 83

Using reflection:

First = 36, Second = 83  
{% endhighlight %}

[Here is a Java version of the same example][1]

 [1]: {{ site.baseurl }}{% post_url 2013-09-05-java-write-code-indirectly-using-reflection %}