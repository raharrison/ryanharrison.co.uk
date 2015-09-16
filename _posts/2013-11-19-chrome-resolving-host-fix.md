---
layout: post
title: Chrome Resolving Host Fix
tags:
  - chrome
  - fix
---
So recently I came up against the &#8216;Resolving Host&#8217; problem in Chrome that temporarily grinds the browser to a complete halt. There seems to be a lot of people who are having the same problems, yet no real solution that works for any substantial amount of time.

The current fixes take the form of unchecking the &#8216;Predict network actions to improve page load performance&#8217; checkbox under the advanced settings section of Chrome. On a completely updated system, for me however, this didn&#8217;t seem to work.

After a ton of searches and many trials I think I&#8217;ve found a solution that really works (well for me anyways):

Disable the &#8216;Built-in Asynchronous DNS&#8217; functionality of Chrome by:

  1. Navigate to `chrome://flags`
  1. Find `Built-in Asynchronous DNS` (about halfway down the page)
  1. Disable it and then restart Chrome

I&#8217;ve been using this fix for over a month now and the problem seems to have disappeared completely.