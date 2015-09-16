---
layout: post
title: 'Java &#8211; Calculate the Geometric Mean'
tags:
  - java
  - mean
  - snippet
  - statistics
---
Here is a small snippet to calculate the [geometric mean][1] of a data set.

The geometric mean is defined as:

![][2]

<br />
{% highlight java %} 
public static double geometricMean(double[] data)  
{
	double sum = data[0];

	for (int i = 1; i < data.length; i++) {
		sum *= data[i]; 
	}
	return Math.pow(sum, 1.0 / data.length); 
}
{% endhighlight %}

 [1]: http://en.wikipedia.org/wiki/Geometric_mean
 [2]: http://upload.wikimedia.org/math/0/2/c/02cc5b37c813d7b94697e89f8e7086d6.png