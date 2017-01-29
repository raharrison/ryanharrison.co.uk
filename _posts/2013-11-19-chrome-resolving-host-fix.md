---
layout: post
title: Chrome Resolving Host Fix
tags:
  - chrome
  - fix
---
So recently I came up against the 'Resolving Host' problem in Chrome that temporarily grinds the browser to a complete halt. There seems to be a lot of people who are having the same problems, yet no real solution that works for any substantial amount of time.

The current fixes take the form of unchecking the 'Predict network actions to improve page load performance' checkbox under the advanced settings section of Chrome. On a completely updated system, for me however, this didn't seem to work.

After a ton of searches and many trials I think I've found a solution that really works (well for me anyways):

Disable the 'Built-in Asynchronous DNS' functionality of Chrome by:

  1. Navigate to `chrome://flags`
  1. Find `Built-in Asynchronous DNS` (about halfway down the page)
  1. Disable it and then restart Chrome

I've been using this fix for over a month now and the problem seems to have disappeared completely.