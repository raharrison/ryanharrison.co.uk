---
layout: post
title: 'Java – A better Hello World program?'
tags:
  - java
---
For years now this has been the Java version of the famous 'Hello World' program that is often the very first program that new developers write:

{% highlight java %}  
public class HelloWorld {  
    public static void main(String[] args) {  
        System.out.println("Hello World!");  
    }  
}  
{% endhighlight %}

But is this a really the kind of code beginners should be seeing when they begin the Java adventures – putting all the logic in the main method and making no use of object oriented practices? Surely it would be better to drive in the fundamental OOP principles from the very start? You see all too much people using loads of static methods and calling them all in their main method which by now spans a good few hundred lines of code. Maybe they get this idea from this 'Hello World' program?

If we are really following object oriented programming practices (which Java tries so hard to enforce), the 'Hello World' program should really look more like this:

{% highlight java %}  
public class HelloWorld {  
    public static void main(String[] args) {  
        new HelloWorld().printHelloWorld();  
    }

    public void printHelloWorld() {  
        System.out.println("Hello World!");  
    }  
}  
{% endhighlight %}

Now we are suddenly using classes and methods! Ok it's a little more complicated for complete beginners to learn, but at least it gives the teachers more to talk about rather than trying to avoid the inevitable questions about the `static` keyword and that `String[]`.

Traditionally the 'Hello World' program is normally the shortest amount of code possible to generate the necessary output. That's fair enough and the first example does this fine, but for teaching practices the second program is so much better. Classes/methods are amongst the hardest concepts to teach new programmers so why not begin that journey from the very beginning? A lot of new Java developers try to force procedural code into a purely object oriented language. Most of the time it doesn't end well at all. Maybe this could be avoided by skipping the whole concept entirely (the static keyword is the main culprit). Everything should be inside methods of a class – of which objects should be created and those methods called with them. Hopefully the main method would then never grow into a hundred line mess of logic.

Just a suggestion to any Java teachers out there. Although a little harder to teach, in my experiences I reckon this could be a pretty helpful change in the long run.