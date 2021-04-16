---
layout: post
title: How to Create a .gitignore File in Windows Explorer
tags:
  - git
  - tip
  - trick
  - windows
---
When working with Git repositories in Windows, it’s not rare to have to create `.gitignore` or even a `.gitattributes` file for your repo. Unfortunately, in Windows Explorer, creating files with a dot prefix isn’t so easy. If you try to rename a file to `.gitignore` for example in Windows Explorer, you will be met with this error message:

![gitignore error](/images/2014/gitignore_error.png){: .center-image width="300"}

To get around this problem, you normally have to open up a command prompt window in your repo and manually rename an existing file using:

`ren gitignore.txt .gitignore`

There is however a much easier way. Instead of naming your newly created file `.gitignore`, add an extra period onto the end making `.gitignore.` and your file will be created without the errors:

![gitignore create](/images/2014/gitignore_create.png){: .center-image width="93"}

As an aside those on Unix machines (or with Git Bash installed on Windows) can simply use this command and forget about the above:

`touch .gitignore`