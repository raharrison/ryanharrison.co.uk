---
layout: post
title: Open Cygwin Here Shortcut
tags:
  - cygwin
  - shortcut
  - explorer
---

After frequently using the 'Open command window here shortcut' in Windows Explorer to open up a command prompt window in the current directory, I found it cumbersome not to have the option to open a Cygwin (or Bash) prompt as well, especially considering how I now find myself using Cygwin more and more often.

There are registry edits that you can do to get similar functionality, but it's much easier to just use one of the packages bundled with Cygwin. Open up the Cygwin installer and select the `chere` package under `Shells`. It's a very small package and so should install relatively quickly.

After that it's just one command to add the new entry to the right-click context menu in Windows Explorer. Open up a new Cygwin terminal as administrator (this is important!) and run:

`chere -i -t mintty`

This will add a new entry to open up a mintty (bash) shell at the current directory. There are also options to specifiy the shell to open (`-s zsh` etc) and the text in the shortcut (`-e "Custom text"` etc). If completed successfully, you should see a new 'Bash Prompt Here' context menu entry:

![Bash Prompt Here Entry]({{ site.url }}/images/2015/bash_prompt_here.png){: .center-image}

