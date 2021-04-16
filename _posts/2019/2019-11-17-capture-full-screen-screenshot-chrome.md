---
layout: post
title: How to capture full page screenshots in Chrome
tags:
  - chrome
  - full
  - screenshot
  - devtools
  - page
typora-root-url: ..
---

Capturing full page screenshots of a webpage within Chrome can be useful, but most solutions to this involve having to install obnoxious extensions. Turns out however that this can easily be done within the base Chrome install itself - no extensions or extra programs needed. There are two methods of doing so depending on whether or not you want a screenshot capturing exactly what you see on screen, or want to emulate the view from a different device/screen resolution.

## 1. Command Menu - Capture full screenshot

The first and easiest method will capture a PNG screenshot of the full page as you see it within your browser.

- Open up the Chrome Devtools by pressing `F12`, `CTRL + SHIFT + I` or `Right-Click anywhere -> Inspect`
- Open up the devtools command menu panel by pressing `CTRL + SHIFT + P` (this is a commonly missed feature similar to the VS Code Command Pallete that gives you quick access to pretty much all devtools features)
- Start typing `capture` in the menu - you will see options to capture a full size screenshot or even just a defined area of the page if needed.

![Chrome capture full size screenshot](/images/2019/chrome-capture-screenshot.png)



## 2. Device Mode

The second, slightly more involved option, lets you capture screenshots through the built in Chrome device mode which allows you to view webpages as though you were using other devices such as phones or tablets.

- Open up the Chrome Devtools by pressing `F12`, `CTRL + SHIFT + I` or `Right-Click anywhere -> Inspect`
- Enable the `Device Mode` by pressing the button directly to the left of the `Elements` tab or keyboard shortcut `CTRL + SHIFT + M`
- After selecting your preferred device options, resolution etc, press the hamburger menu on the top right of the page and select `Capture full size screenshot`.

![Chrome capture full size screenshot](/images/2019/chrome-device-mode-screenshot.png)