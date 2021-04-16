---
layout: post
title: WSL - Creating a shortcut to Windows Documents
tags:
  - wsl
  - shortcut
  - linux
  - symlink
  - windows
---

Due to the fact that you should never [change Linux files using Windows apps and tools](https://blogs.msdn.microsoft.com/commandline/2016/11/17/do-not-change-linux-files-using-windows-apps-and-tools/) when running the WSL, I find myself during the vast majority of work in my Windows documents area and then accessing them directly via Bash.

Your Windows drives are accessible via `/mnt` using the same drive letters as found in Windows explorer - e.g to access your Windows Documents area via Bash you can `cd` to:

`/mnt/c/Users/<username>/Documents`

This works just fine, but it's a bit long winded when most of your frequently accessed files are located there (plus it looks ugly having such a long path in your prompt all the time). Thankfully, the process gets much simpler through the use of symlinks. Using the following command you can create a symlink pointing directly to your Windows Documents folder:

`ln -s /mnt/c/Users/<username>/Documents ~/docs`

You can then just do a quick `cd ~/docs` and end up right in your Windows home directory. The great part is that your prompt will also just show `~/docs` instead of the full path via `/mnt`. I have a number of these symlinks set up, pointing to various places in my Windows drive, and they make the whole experience when using Bash much more fluid.

