---
layout: post
title: 'Java - Common Pitfall when using Scanner'
tags:
  - java
  - scanner
  - tip
  - trick
---
It's very common for beginners in Java to use the many helpful methods of `Scanner` to obtain input from the user. They normally have some sort of task which involves asking the user for some `String` input, some numerical input and finally more `String` input - be this to do some processing with or just output back to the user in the simplest case. Most people will be happy using the `nextLine()` and `nextInt()` methods of `Scanner` to do so, however will then get confused when they don't get the behaviour they expect. This is a great example of why you should know the specific behaviour of the library methods you call and not just assume that they will conform exactly to your needs by default.

As an example, say we get the task to ask the user for their name, storing it in a `String` variable, their age, storing it in an `int` variable, and finally their address, again storing it in a `String` variable. We may come up with this code to start off with:

{% highlight java %}  
import java.util.Scanner;

public class Sample {  
    public static void main(String[] args) {  
        Scanner scanner = new Scanner(System.in);  
        System.out.println("Enter name:");  
        String name = scanner.nextLine();

        System.out.println("Enter age:");  
        int age = scanner.nextInt();

        System.out.println("Enter address:");  
        String address = scanner.nextLine();

        System.out.println("—————");  
        System.out.println("Your name = " + name);  
        System.out.println("Your age = " + age);  
        System.out.println("Your address = " + address);  
    }  
}
{% endhighlight %}

Seems OK at a first glance, we prompt the user for input, use `Scanner` to retrieve it from the console and finally output what they entered. When we run this code however, it doesn't function as expected:

{% highlight text %}  
C:\Users\Ryan\Java>java Sample  
Enter name  
Ryan  
Enter age  
20  
Enter address  
—————  
Your name = Ryan  
Your age = 20  
Your address =  
{% endhighlight %}

We get the name and age input successfully, but what happened to the address? We get prompted for the address yet have no opportunity to enter anything - resulting in a blank `String` for this field.

Although it may not seem like it, `Scanner` is actually behaving here exactly how it was designed to do so. The `Scanner` class is a multi-purpose tool, capable of not only parsing character input from the console, but also from other files and streams. In order to do so, it provides two methods: `next()` and `nextLine()`. The `next()` method takes a token from the current input stream up to the next delimiter (which by default is whitespace although this can be changed). It then returns this parsed token, but importantly leaves the delimiter in the stream. The `nextLine()` method on the other hand accepts a whole line up to and including the newline character. This time however, the delimiter gets consumed as well. Most of the other parsing methods in `Scanner` base themselves around these two base models.

Examples of those other parsing methods include convenient methods to accept input and convert it into another type (a call to `nextInt()` for example). Scanner does this by calling the `next()` method and then attempting to parse the output into the resulting type. This seems quite reasonable, but recall that we have called the `next()` method here and not `nextLine()`. This is where the problems occurs in our example above. The `next()` method leaves the delimiter in the stream, which means that when the user types a number, say "20" for their age and hits return, the `Scanner` gets a stream consisting of "20\n". When the `nextInt()` call happens, the "20" is removed, and becomes a 20, and now the stream is "\n". Now we call `nextLine()` again to retrieve the address. The `Scanner` does what it's meant to and takes the the "\n", discards the newline character ("\n") and returns the remaining String - which in this case is "". Thus we get the undesired behaviour.

The solution? Simply call `nextLine()` after we call `nextInt()` to consume the remaining newline character so that we get the chance to enter the address. Ideally however, you shouldn't litter your input code with a load of new `nextLine()` calls to get the desired behaviour. Therefore, its probably best to implement your own utility class to take input in the manner you expect - leaving the `Scanner` in the correct state for further use afterwards.

This leaves the question as to why they decided to implement it in this way. As I said before `Scanner` is a very multi-purpose tool that should be able to accept a wide variety of input formats - not just one token on each line. A major use case of `Scanner` is to for example parse all the ints on one line, separated by whitespace, in order to populate some kind of `Collection`. If the `nextLine()` methods was used in `nextInt()` rather than `next()` we wouldn't be able to do this and `Scanner` would be restrained in its use. This of course wouldn't be a useful design decision and so we have to do this small bit of extra work to make it conform to our requirements.