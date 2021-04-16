---
layout: post
title: WSL 'Bash Here' Context Menu Item
tags:
  - wsl
  - bash
  - context menu
  - explorer
---

Similarly to how you can hold `shift` whilst you right click on a directory within Windows explorer to open a new command prompt at that directory, it is also possible to do the same with the new WSL Bash. This can make it much easier to work with files within explorer from within the WSL as opposed to lengthy `cd` commands to the relevant `mnt`.

![WSL Explorer Context Menu](/images/2017/wsl-context-menu.png)

To add the new context menu item for Bash within explorer, you need to create a new key within the registry and a few new values underneath it:

  1. Open the registry editor by searching for `regedit` or going through `Win+R`. You will need admin privileges to open the editor.
  1. (Optional) Backup your registry via File->Export.
  1. Navigate to the key `HKEY_CLASSES_ROOT\Directory\Background\shell`.
  1. Create a new key called `WSL` under shell and and another key underneath `WSL` called `command`. This should reflect the structure in the `cmd key` within shell. The newly created structure should be `HKEY_CLASSES_ROOT\Directory\Background\shell\WSL\command`.
  1. Change the `Default` value under the `WSL` key to the value you want to see in the context menu e.g. 'Bash Prompt Here'.
  1. (Optional) Create a new String value called `Icon` under the `WSL` key with a value of `%USERPROFILE%\\AppData\\Local\\lxss\\bash.ico`. This will make the bash icon appear in the context menu as seen in the screenshot above.
  1. Change the `Default` value under the `command` key to `cmd.exe /c pushd "%V" && bash.exe`.
  1. Exit the editor and test by right clicking the white space within any directory in Windows Explorer.

  You should something corresponding to the screenshot. Selecting the new menu item will open up a new WSL Bash prompt starting at the current directory.

  Here is the contents of a `.reg` file you can also use instead of the above. Simply copy the contents into a file with the `.reg` extension and then double click on it to merge it into your registry.

{% highlight text %}
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\Background\shell\WSL]
@="Bash Prompt Here"
"Icon"="%USERPROFILE%\\AppData\\Local\\lxss\\bash.ico"

[HKEY_CLASSES_ROOT\Directory\Background\shell\WSL\command]
@="cmd.exe /c pushd \"%V\" && bash.exe"
{% endhighlight %}




