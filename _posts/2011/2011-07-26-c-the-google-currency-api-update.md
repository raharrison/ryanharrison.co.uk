---
layout: post
title: C# The Google Currency API Update
tags:
    - C#
    - google api
    - JSON
    - regular expressions
---

**NOTE: The Google Finance API has now been deprecated so this code will no longer work**

After testing out the code from the [recent post on the Google Currency API][1], it became apparent that the code had one very significant bug that caused an exception to be thrown when the user enters a value that returns a result over the one million mark. For example -;

[http://www.google.com/ig/calculator?hl=en&q=1000000gbp=?usd][2]

which gives back this JSON object -;

`{lhs: "1 000 000 British pounds",rhs: "1.6399 million U.S. dollars",error: "",icc: true}`

As you can see, instead of returning just a decimal number, it gives a number followed by a String, which caused the previous program to crash.

In this case to fix the bug, the Regex needs to be modified so that it returns not only the number, but also the new String in the same match. With this information, the number can then be multiplied to give the final result as a single decimal.

The Regex now becomes -;
`rhs: \\\"((\\d|\\s|\\.)*)(\\s[^\\s]+)`

(the cluster of backslashes are to escape the possible escape sequences of '/d' and '/s' for example)

The new Regular Expression makes use of 'Groups' to store the two pieces of data in the same match -; the first groups contains the number, and the third contains the String due to the way this pattern is designed (it's probably possible to modify this, yet it doesn't create too much of a problem and so isn't worth the effort).

We can now produce a match from the response using the same code as before -;

{% highlight csharp %}
WebClient client = new WebClient();

string url = string.Format("http://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}", amount, from.ToUpper(), to.ToUpper());

string response = client.DownloadString(url);

Regex pattern = new Regex("rhs: \\\"((\\d|\\s|\\.)\*)(\\s[^\\s]+)");  
Match match = pattern.Match(response);  
{% endhighlight %}

Once we have access to the match, we can extract the data into our own variables -;

{% highlight csharp %}
string number = match.Groups[1].Value;  
number = number.Replace(((char)160).ToString(), "");

decimal num = System.Convert.ToDecimal(number);  
string units = match.Groups[3].Value.Replace(" ","");  
{% endhighlight %}

Here, the number is stored as a String from the first group and the 'spaces' are removed (for some reason in the returned String, 'spaces' have a Unicode value of 160, which is called the 'Non-breaking space'). Next, the number is converted into a decimal and the units are extracted from the match and stored in the 'units' variable.

As the only possible values of the 'units' variable are 'millions', 'billions' and 'trillions', we can simply test the variable against each and multiply the number correspondingly to get the overall result. Finally, we just need to round the number to two decimal places to signify a currency, and return the value. Here is the full updated code which hopefully is bug free. The full source code can be found in [GitHub][3].

{% highlight csharp %}
using System;  
using System.Text.RegularExpressions;

public static class Currency  
{  
 public static decimal Convert(decimal amount, string from, string to)  
 {  
 WebClient client = new WebClient();

    	string url = string.Format("http://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}", amount, from.ToUpper(), to.ToUpper());

    	string response = client.DownloadString(url);

    	Regex pattern = new Regex("rhs: \\\"((\\d|\\s|\\.)*)(\\s[^\\s]+)");
    	Match match = pattern.Match(response);

    	string number = match.Groups[1].Value;
    	number = number.Replace(((char)160).ToString(), "");

    	decimal num = System.Convert.ToDecimal(number);
    	string units = match.Groups[3].Value.Replace(" ","");

    	if(units.Equals("million"))
    	{
    		num *= 1000000;
    	}
    	else if (units.Equals("billion"))
    	{
    		num *= 1000000000;
    	}
    	else if (units.Equals("trillion"))
    	{
    		num *= 1000000000000;
    	}

    	return Math.Round(num, 2);
    }

}  
{% endhighlight %}

[1]: {{ site.baseurl }}{% post_url 2011/2011-07-15-c-the-google-currency-api %}
[2]: http://www.google.com/ig/calculator?hl=en&q=1000000gbp=?usd
[3]: https://github.com/raharrison/GoogleAPI
