---
layout: post
title: Cygwin Change Home Directory
tags:
  - cygwin
  - home
  - directory
  - nsswitch.conf
---

In a new installation of Cygwin, your home directory will be in `C:/cygwin/home/<user>/`, and can be accessed by the usual `~` shortcut. Although this works just fine, it's often useful to use the utilities provided by Cygwin in your local Windows user area `C:/Users/<user>`. Manually navigating to your Windows home directory can be a tedious process as you also have to go through `cygdrive`. By default, to access your Windows area in Cygwin you would navigate to `/cygdrive/c/Users/<user>`. Alternatively, you can just change your Cygwin home directory to be the same as Windows for easy access to all your files.

There are numerous posts on the Internet about how to accomplish this but the accepted methods always seems to change alongside Cygwin versions. Common solutions tend to involve the `mkpasswd` command, various environment variables, shortcuts and even registry edits. Thankfully, it seems that in the newer versions of Cygwin, there is a much easier way which requires one simple edit to a configuration file.

Navigate to the `/etc/nsswitch.conf` file in your installation folder (this should be something like `C:/cygwin/etc/nsswitch.conf`). Open it up in your favourite text editor and make the following change to the `db_home` property. This change simply points your Cygwin home to your Windows home using the `%H` variable. After the change, the file should look like this:

    # /etc/nsswitch.conf
    #
    # Defaults:
    # passwd:   files db
    # group:    files db
    # db_enum:  cache builtin
    db_home: /%H
    # db_shell: /bin/bash
    # db_gecos: <empty>

And that's it. Fire up a new Cygwin terminal and you should see that the default directory is now your Windows home directory. As expected, `~` also now points to your Windows home area. 


