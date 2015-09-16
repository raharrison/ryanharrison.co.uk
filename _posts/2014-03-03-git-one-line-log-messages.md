---
layout: post
title: 'Git &#8211; One Line Log Messages'
tags:
  - git
  - tip
---
A lot of the time when viewing the log in your Git repository you aren&#8217;t that interested in the author and date/time of each commit &#8211; the message and the hash are the most important parts. It would therefore be helpful to cut out everything from the log apart from the main details of each commit. Luckily, just like most things in Git, this is pretty straightforward to do:

`git log --pretty=oneline`

Which will output something like:

{% highlight text %}
a4cc7fe68b3a9f9fe4b1927aa687714ca05a5096 Third commit  
246387bc6f15b1ca4a384af362cdb0deb8364b0e Second commit  
1c827a75295fe5ad657fd3882cbb3a32c3ca1b2b Initial commit
{% endhighlight %}

This is all well and good, yet the hash is pretty long and distracted. Again however there is a way around that as well:

`git log --pretty=oneline --abbrev-commit`

Which outputs:

{% highlight text %}
a4cc7fe Third commit  
246387b Second commit  
1c827a7 Initial commit
{% endhighlight %}

This time we only get a fraction of the hash for each commit (which is all we really need) and the message &#8211; much better!