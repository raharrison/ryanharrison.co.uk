---
layout: post
title: Maximum Sum Subsequence
tags:
  - algorithm
  - efficiency
  - java
  - maximum sum subsequence
  - order of growth
---
The maximum sum subsequence of an array is the consecutive group of numbers that have the largest sum.

For example with the array `{1, 11, -9, -20, 7, 10, -6, 3, 4, -2}`, the maximum sum subsequence is 18 using the elements `{7, 10, -6, 3, 4}` starting from index `4` and ending at index `8`.

Here are a few algorithms implemented in Java of increasing efficiency that can be used to solve this problem.

1\. **Brute Force &#8211;** take each element as a starting point and each element after as an ending point, sum the elements in between and keep track of the largest sum.

**Efficiency (Order of Growth) = O(n^3)**

{% highlight java %} 
// Calculate the maximum sum of a subsequence of an array  
// Returns an array containing the start index, end index and maximum sum  
// This algorithm has an order of O(n^3)  
public static int[] maximumSumSubsequence(int[] values) {  
	int max = 0;  
	int start = 0;  
	int finish = 0;

	for(int i = 0; i < values.length; i++) { 
		for(int j = i; j < values.length; j++) { 
			int sum = sumSequence(values, i, j); 
			if(sum > max) {  
				max = sum;
				start = i;  
				finish = j;  
			}  
		}  
	}

	return new int[] { start, finish, max };  
}

// Returns the sum of the elements of an array from start to finish inclusive  
private static int sumSequence(int[] values, int start, int finish) {  
	int sum = 0;  
	for(int i = start; i <= finish; i++) { 
		sum += values[i]; 
	} 
	return sum; 
}
{% endhighlight %} 

Although this works well, it scales extremely badly with the algorithm taking nearly half a second with only 2000 elements. As the size of the input doubles, the time taken will increase by a factor of 8 - not good. 

2\. **Remember the current sum.** Instead of computing the sum of elements i to j on each iteration of the innermost loop, we can instead remember the current sum of the elements. This increases the efficiency by a factor of O(n). 

**Efficiency (Order of Growth) = O(n^2)**

{% highlight java %}
// Calculate the maximum sum of a subsequence of an array 
// Returns an array containing the start index, end index and maximum sum 
// This algorithm has an order of O(n^2) 
public static int[] maximumSumSubsequence(int[] values) { 
	int max = 0; 
	int start = 0; 
	int finish = 0; 
	for(int i = 0; i < values.length; i++) { 
		// now we remember the current sum on each iteration of the inner loop 
		int sum = 0; 
		for(int j = i; j < values.length; j++) { 
			sum += values[j]; 
			if(sum > max) {  
				max = sum;  
				start = i;  
				finish = j;  
			}  
		}  
	}
	return new int[] { start, finish, max };  
}  
{% endhighlight %}

This optimisation, although small saves a lot of execution time. Now as the size of the input array doubles, the time taken will increase by a factor of 4. However we can still improve this and gain a linear relationship between size and execution time.

3\. **Single loop &#8211;** now we only traverse the array once. We keep track of the maximal sum subsequence so far and the maximal sum subsequence ending at the current position.

**Efficiency (Order of Growth) = O(n)**

{% highlight java %} 
// Calculate the maximum sum of a subsequence of an array  
// Returns an array containing the start index, end index and maximum sum  
// This algorithm has an order of O(n)  
public static int[] maximumSumSubsequence(int[] values) {  
	int max = 0;  
	int start = 0;  
	int finish = 0;

	int endStart = 0;  
	int endMax = 0;

	for(int i = 0; i < values.length; i++) { 
		endMax += values[i]; 
		if(endMax > max) {  
			max = endMax;  
			start = endStart;  
			finish = i;  
		}

		if(endMax < 0) { 
			endMax = 0; 
			endStart = i + 1;
		} 
	} 
	return new int[] { start, finish, max };
}
{% endhighlight %}

Now we have the best case scenario for this problem. We cannot get any better as in the worst case scenario each element of the array has to be looked at at least once. With the now linear order of growth as the size of the input doubles, the time taken also doubles.