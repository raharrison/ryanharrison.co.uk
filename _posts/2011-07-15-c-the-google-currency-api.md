---
layout: post
title: C# - The Google Currency API
tags:
  - C#
  - google api
  - JSON
  - regular expressions
---

**NOTE: The Google Finance API has now been deprecated so this code will no longer work**

After I found myself using Google to translate currencies, I wondered whether it would be possible to utilise this functionality in a program. After a little research it turns out that Google offer a huge API that deals with currencies and finance. For the purpose of this post I will show you how to convert currencies, yet you can also use the API to find stock information and even market gains over a period.

Although here I will be using C#, it should be possible to use pretty much any language and get the same results.

This particular feature can be utilised through a simple URL containing the amount to convert from, the currency to convert from, and the currency to convert to. This translates into this URL -;

`http://www.google.com/ig/calculator?hl=en&q={AMOUNT}{FROM}=?{TO}`

For example -;

`http://www.google.com/ig/calculator?hl=en&q=1GBP=?USD`

(which converts 1 British Pound to US Dollars) returns the following -;

`{lhs: "1 British pound",rhs: "1.6121 U.S. dollars",error: "",icc: true}`

The URL responds with a JSON object where the actual result is mixed in with some other information from the request, which presents a minor problem when trying to convert currencies in our program. This will be dealt with a bit later on.

First of all in our program, we to get the output of the request. I used the WebClient class, which will download the response as a String for use in our program. In the following code, the URL is constructed with parameters passed in by the user, and the string is downloaded and stored in the &#8216;response&#8217; variable.

{% highlight csharp %}
using System;

public static class CurrencyConverter  
{  
	public static decimal Convert(decimal amount, string from, string to)  
	{  
		WebClient web = new WebClient();

		string url = string.Format("http://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}", amount, from.ToUpper(), to.ToUpper());

		string response = web.DownloadString(url);  
	}  
}  
{% endhighlight %}

This takes care of getting the response with the answer we want, yet we still need to somehow extract the correct data from the string. In this example I will use Regular Expressions however if your prefer not to use them, or your language does not natively support them, it would be perfectly viable to loop through the response one character at a time, and parse out the result.

The Regex pattern will look like this &#8211;

`rhs: \\\"(\\d\*.\\d\*)`

This pattern essentially searches for the &#8216;rhs&#8217; which appears just before the result value, and extracts any numbers afterwards until any non-numeric character is reached.

Using the Regex to extract the result, we end up with the following, final code &#8211;

{% highlight csharp %}
using System;  
using System.Text.RegularExpressions;

public static class CurrencyConverter  
{  
	public static decimal Convert(decimal amount, string from, string to)  
	{  
		WebClient web = new WebClient();

		string url = string.Format("http://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}", amount, from.ToUpper(), to.ToUpper());

		string response = web.DownloadString(url);

		Regex regex = new Regex("rhs: \\\"(\\d\*.\\d\*)");  
		Match match = regex.Match(response);

		return System.Convert.ToDecimal(match.Groups[1].Value);  
	}  
}  
{% endhighlight %}

The full source code can be found in [GitHub][2].

Thats about it for the Google Currency API for now, however I may post snippets on how to use some other features of the extensive API&#8217;s Google offer soon.

[More Information about the Google Finance API][1]

 [1]: http://code.google.com/apis/finance/docs/2.0/reference.html
 [2]: https://github.com/raharrison/GoogleAPI