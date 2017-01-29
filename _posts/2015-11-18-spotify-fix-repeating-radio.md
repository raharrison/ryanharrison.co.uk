---
layout: post
title: Spotify - Fix Repeating Radio
tags:
  - spotify
  - radio
  - repeat
---

![Spotify Logo](/images/2015/spotify.png){: .center-image width="200"}

I tend to use the radio in Spotify quite a bit. It's never been the best of implementations out there, but recently it's been more annoying than usual in terms of repeating. The radio has always liked to repeat some songs over and over again, but it has now decided to repeat entire sequences of songs.

For example, if I start a new radio I will get a sequence of songs as usual. If however I listen to something else (perhaps a random song or playlist etc) and then go back to the same radio station, I will be greeted with the exact same sequence of songs as before. As you can imagine, this has gotten annoying really quickly. Initially you can keep skipping until you get to something new, but eventually that gets way too long-winded.

A quick search on the support forums show multiple users with the same kind of issues as me, but none are recent and there are no real solutions. Thankfully, after snooping through the AppData files for Spotify, I was able to come up with a solution:

  1. Navigate to the `Local AppData` folder for Spotify. This should be at `C:/Users/<user>/AppData/Local/Spotify`
  1. Locate to the `Local Storage` directory inside the `Browser` directory. At this point you should be in `AppData/Local/Spotify/Browser/Local Storage`
  1. There should be two files starting with `http_radio`. For me they are `http\_radio.app.spotify.com\_0.localstorage` and `http\_radio.app.spotify.com\_0.localstorage-journal`. Delete both of these files
  1. Restart Spotify and the radio's should be reset

This might just be an issue for me, or might be a bug that will be fixed at some point. If it's a design decision they need to rethink their priorities. At least I have this relatively easy fix however. I've put it all into a batch file and tend to run it just before I start Spotify.