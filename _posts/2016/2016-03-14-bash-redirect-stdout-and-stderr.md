---
layout: post
title: Bash - Redirecting stdout and stderr
tags:
  - bash
  - redirect
  - stdout
  - stderr
---

#### Redirect `stdout`/`stderr` to a truncated file:

{% highlight bash %}
# StdOut
cmd > out.txt # (stderr printed to console)
# StdErr
cmd 2> err.txt # (stdout printed to console)
{% endhighlight %}

#### Redirect `stdout`/`stderr` to a file (appending):

{% highlight bash %}
# StdOut
cmd >> out.txt # (stderr printed to console)
# StdErr
cmd 2>> err.txt # (stdout printed to console)
{% endhighlight %}

#### Redirect both `stdout` and `stderr` in same command to different files (truncating):

{% highlight bash %}
cmd > out.txt 2> err.txt
{% endhighlight %}

#### Redirect both `stdout` and `stderr` to same output (truncating):

{% highlight bash %}
cmd > out.txt 2>&1
{% endhighlight %}

"Redirection statements are evaluated, as always, from left to right. `>> file` - `STDOUT` to file (append mode) (short for `1>> file`) `2>&1` - `STDERR` to 'where stdout goes' Note that the interpretation 'redirect `STDERR` to `STDOUT`' is wrong"

[Source](http://stackoverflow.com/questions/876239/how-can-i-redirect-and-append-both-stdout-and-stderr-to-a-file-with-bash)