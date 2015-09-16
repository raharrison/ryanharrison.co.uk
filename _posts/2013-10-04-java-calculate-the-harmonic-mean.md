---
layout: post
title: Java - Calculate the Harmonic Mean
tags:
  - java
  - mean
  - snippet
  - statistics
---
Here is a small snippet to calculate the [harmonic mean][1] of a data set.

The harmonic mean is defined as:

![][2]

<br />
{% highlight java %}
public static double harmonicMean(double[] data)  
{  
	double sum = 0.0;

	for (int i = 0; i < data.length; i++) { 
		sum += 1.0 / data[i]; 
	} 
	return data.length / sum; 
}
{% endhighlight %}

 [1]: http://en.wikipedia.org/wiki/Harmonic_mean
 [2]: http://upload.wikimedia.org/math/8/d/5/8d5a941622352760cadde9f52209b89d.png