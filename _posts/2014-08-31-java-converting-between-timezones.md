---
layout: post
title: 'Java &#8211; Converting Between Timezones'
tags:
  - date
  - java
  - timezone
  - tip
  - trick
---
In Java it&#8217;s not too easy to convert `Date` objects between timezones as they always like to store the time in UTC (even though they will happily print BST when converted to a String form). Normal timezone conversion in Java is done through the `Calendar` class which is, as all Java developers know, really heavy and a nightmare to use. Even using a `Calendar` though, getting a `Date` object out if it in a different timezone doesn&#8217;t seem to happen at all. But it can be useful to have a `Date` object represent a time in a different timezone, so here is a little helper method that gets around it. Included is also another handy helper method that creates a `Date` object at a certain time (something that you often want to do but don&#8217;t want to see or use a `Calendar` directly):

{% highlight java %}
import java.util.Calendar;  
import java.util.Date;  
import java.util.TimeZone;

public class TimeZoneConversions {  
	public static void main(String[] args) {  
		Date date = dateOf(14, 30, 0, 20, 8, 2014);  
		TimeZone local = TimeZone.getTimeZone("Europe/London");  
		TimeZone dest = TimeZone.getTimeZone("America/New_York");

		System.out.println(date);  
		System.out.println(translateTime(date, local, dest));
	}

	public static Date dateOf(int hour, int minute, int second,  
		int dayOfMonth, int month, int year) {  
		Date date = new Date();  
		Calendar c = Calendar.getInstance();  
		c.setTime(date);

		c.set(Calendar.YEAR, year);  
		c.set(Calendar.MONTH, month - 1);  
		c.set(Calendar.DAY_OF_MONTH, dayOfMonth);  
		c.set(Calendar.HOUR_OF_DAY, hour);  
		c.set(Calendar.MINUTE, minute);  
		c.set(Calendar.SECOND, second);  
		c.set(Calendar.MILLISECOND, 0);  
		return c.getTime();  
	}

	public static Date translateTime(Date date, TimeZone src, TimeZone dest) {  
		long time = date.getTime();  
		int offset = (dest.getOffset(time) - src.getOffset(time));  
		return new Date(time - offset);  
	}  
}  
{% endhighlight %}