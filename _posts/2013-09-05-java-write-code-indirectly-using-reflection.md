---
layout: post
title: 'Java – Write code indirectly using reflection'
tags:
  - java
  - reflection
---
In a [recent post][1] I showed how it is possible to write all your [C# code indirectly through reflection][1]. Here is the same example in Java. The process itself is very much the same – retrieve meta information about the classes/methods we are interested in and then invoke them passing in the object it would normally be called from. The classes themselves are all very similar through C# to Java. `Type` becomes `Class`, `MethodInfo` becomes `Method` etc.

A more interesting difference is how the Java version uses variable length parameters in the `.invoke` calls on `Method` objects as a way of passing parameters to the particular method. In the C# version you have to explicitly pass a `Type` or object array. I think the Java version is slightly more user friendly in that quite small regard even though the actual parameter itself is an array in both circumstances.

Its also interesting to see just how many exceptions the Java version can throw in the process. Because they are all checked you are forced to deal with them whereas C# does not have this feature. Its probably likely then that you would have to catch a more generic exception in the C# version.

Here is the code for the Java version. The result is the same as the C# version.

{% highlight java %}  
import java.lang.reflect.InvocationTargetException;  
import java.lang.reflect.Method;

public class Reflector {

    public static void main(String[] args) throws InstantiationException, IllegalAccessException, SecurityException,  
        NoSuchMethodException, IllegalArgumentException, InvocationTargetException {

        // Normal method  
        System.out.println("Normal method:\n");  
        Foo foo = new Foo();  
        foo.setFirst(36);  
        foo.setSecond(83);  
        System.out.println(foo.toString());

        System.out.println("\nUsing reflection:\n");  
        Class<?> fooClass = Foo.class;

        Foo fooInstance = (Foo) fooClass.newInstance();  
        Method setFirstMethod = fooClass.getMethod("setFirst", int.class);  
        Method setSecondMethod = fooClass.getMethod("setSecond", int.class);  
        setFirstMethod.invoke(fooInstance, 36);  
        setSecondMethod.invoke(fooInstance, 83);

        Method toString = fooClass.getMethod("toString", null);  
        String result = (String) toString.invoke(fooInstance, null);

        Method println = System.out.getClass().getMethod("println", String.class);  
        println.invoke(System.out, result);
    }
}

class Foo {

    private int first;  
    private int second;

    public void setFirst(int newFirst) {  
        this.first = newFirst;  
    }

    public void setSecond(int newSecond) {  
        this.second = newSecond;  
    }

    @Override  
    public String toString() {  
        return "First = " + first + ", Second = " + second;  
    }  
}  
{% endhighlight %}

Output:

{% highlight text %}  
Normal method:

First = 36, Second = 83

Using reflection:

First = 36, Second = 83  
{% endhighlight %}

[Here is the C# version.][1]

 [1]: {{ site.baseurl }}{% post_url 2013-08-29-c-write-code-indirectly-using-reflection %}