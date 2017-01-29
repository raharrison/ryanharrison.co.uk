---
layout: post
title: 'Python - Iterate over a list with indexes'
tags:
  - python
  - list
  - tip
  - trick
---
In Python the typical way to iterate over a loop is to use the conventional `foreach` loop, as `lists` expose `iterators`:

{% highlight python %}
values = ["Foo", "Bar", "Baz", "Qux"]

for value in values:  
	print value

Output:  
Foo  
Bar  
Baz  
Qux  
{% endhighlight %}

In a lot of cases this is all that's needed, however in other circumstances we may need access to the index that each element is at inside the `list` - most of the time in order to perform some kind of check on the next or previous values in the `list`. The conventional `for` loop above of course simply gives us the values inside the `list`, not the indexes. We could set up a counter variable which increments each time around the loop, yet this seems clumsy. We are increasing the scope of a variable that should ideally be kept local to the loop.

Another popular solution is to use the `range` function, which returns an `iterator` of values from zero to the number we specify as a parameter. By creating a `list` of numbers from zero to the size of the `list`, we can then use each element as an index in order to extract each value:

{% highlight python %} 
for i in range(len(values)):  
	print "The value at index {0} = {1}".format(i, values[i])

Output:  
The value at index 0 = Foo  
The value at index 1 = Bar  
The value at index 2 = Baz  
The value at index 3 = Qux  
{% endhighlight %}

Although this gets us our desired output (in this simple example anyway), it again seems quite a clunky way to perform such as simple task in Python. We have to refer to each value as `values[i]`, or otherwise set up a new local variable. Luckily however, as ever, this is a much neater way of doing this in Python.

One of the built-in functions that Python provides is the `enumerate` function. This handy function gives us an `iterator` that returns a `tuple` containing a count (which by default starts from zero) and the values obtained from iterating over the sequence. By simply running through the tuples returned from the `iterator` provided by this function, we get access to both the indexes and the corresponding values:

{% highlight python %} 
for (index, value) in enumerate(values):  
	print "The value at index {0} = {1}".format(index, value)

Output:  
The value at index 0 = Foo  
The value at index 1 = Bar  
The value at index 2 = Baz  
The value at index 3 = Qux  
{% endhighlight %}

As you can see this is much neater and more efficient than the other solutions. There is no need for extra variables - everything is provided to us in the loop declaration.