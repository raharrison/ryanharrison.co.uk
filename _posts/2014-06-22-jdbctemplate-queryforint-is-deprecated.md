---
layout: post
title: JdbcTemplate queryForInt() is deprecated
tags:
  - deprecated
  - java
  - jdbc
  - library
  - spring
---
There is a lot of Spring documentation online which makes use of the `queryForInt()` and `queryForLong` methods of the very handy `JdbcTemplate` class. However, using newer versions of the Spring framework, these methods have now become deprecated (apparently this has happened from version 3.2.2).

These are the two methods affected:

{% highlight java %}
@Deprecated  
public long queryForLong(String sql, Object... args) throws DataAccessException
{% endhighlight %}

{% highlight java %}
@Deprecated  
public int queryForInt(String sql, Object... args) throws DataAccessException
{% endhighlight %}

I'm not sure why the designers have to decided to deprecate these two methods, but the solution (or perhaps the workaround is simple):

**Old:**

{% highlight java %}
int result = getJdbcTemplate().queryForInt(sql, new Object[] { param });
{% endhighlight %}

**New:**

{% highlight java %}
int result = getJdbcTemplate().queryForObject(sql,  
new Object[] { param }, Integer.class);
{% endhighlight %}

The workaround makes use of the `queryForObject` method and we pass in the `Integer` class in order to coerce the general object into the type we desire. Similarly, for `queryForLong`, you can replace `Integer.class` with `Long.class`.