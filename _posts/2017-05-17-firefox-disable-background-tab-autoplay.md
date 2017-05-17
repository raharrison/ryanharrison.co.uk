---
layout: post
title: Firefox - Disable autoplay of videos in background tabs
tags:
  - firefox
  - video
  - autoplay
---

In Chrome, when you open a link in a new background tab (e.g middle click), any videos on that page (YouTube etc) will not start to play until you directly visit that tab (bringing it to the foreground). This is is something I make use of quite often, however this behaviour is not the default in Firefox. Thankfully though, due to the great configuration options in Firefox, this can easily be fixed:

  1. Type `about:config` in the search bar to open up all of the configuration options.
  1. Filter the results by entering `autoplay` into the search box.
  1. Toggle the preference `media.block-autoplay-until-in-foreground` to `true`.

![Firefox configuration options](/images/2017/firefox-disable-autoplay.png)

From then on, any videos will not begin until you bring that tab into the foreground. When media is being blocked from playing, a play icon will appear in the tab (similar to the mute button for audio). You can click on this to begin playing without bringing the tab to the foreground.

