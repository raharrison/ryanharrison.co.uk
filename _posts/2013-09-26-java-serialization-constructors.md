---
layout: post
title: 'Java &#8211; Serialization Constructors'
tags:
  - java
  - serialization
  - tip
---
It is a common misconception that classes which implement the `Serializable` interface must also declare a constructor which takes no arguments.

When deserialization is taking place, the process does not actually use the object&#8217;s constructor itself. The object is instantiated without a constructor and is then initialised using the serialized instance data.

The only requirement on the constructor for a class that implements `Serializable` is that the first non-serializable superclass in its inheritance hierarchy must have a no-argument constructor. This is because when you serialize an object, the serialization process chains it&#8217;s way up the inheritance hierarchy of the class &#8211; saving the instance data of each Serializable type it finds along the way. When a class is found that does not implement `Serializable`, the serialization process halts.

Then when deserialization is taking place, the state of this first non-serializable superclass cannot be restored from the data stream, but is instead initialised by invoking that class&#8217; no-argument constructor. The rest of the instance data of all the `Serializable` subclasses can then be restored from the stream.

For example this class which does not provide a no-arguments constructor:

{% highlight java %}
public class Foo implements Serializable {  
	public Foo(Bar bar) {  
		...  
	}  
	...
	...  
}  
{% endhighlight %}

Although the class itself does not itself declare a no-arguments constructor, the class is still able to be serialized. This is because the first non-serializable superclass of this class, which in this case is `Object`, provides a no-arguments constructor which can be used to initialize the subclass during deserialization.

If however `Foo` extended from a `Baz` class which did not implement `Serializable` and did not declare a no-arguments constructor:

{% highlight java %}
public class Baz {  
	public Baz(Bar bar) {  
	   ...
	}  
	...
}
public class Foo implements Serializable {  
	...
	...
}  
{% endhighlight %}

In this case a `NotSerializableException` would be thrown during the deserialization process as the state of the `Baz` class cannot be restored through the use of a no-arguments constructor. Because the instance data of the superclass `Baz` could not be restored, the subclass also cannot be properly initialised &#8211; so the deserialization process cannot complete.