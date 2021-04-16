---
layout: post
title: Sublime Text 3 SFTP Plugin
tags:
  - sublime
  - sftp
  - plugin
  - sublime text
---

Amongst one of the best plugins available for Sublime Text 2 & 3 is the SFTP plugin from [wbond](https://wbond.net) (who is known for other great plugins including Alignment, SVN and Package Control itself). The SFTP plugin negates the need for using another dedicated SFTP client such as FileZilla when editing documents on a remote server. From the site, it's features include:

- Work off of a server - edit and manipulate files and folders
- Map a local folder to a remote folder
  - Publish files, folders, or just the changes since your last commit
  - Sync folders - up, down or both directions
  - Diff local vs. remote versions of a file
- Other operations and options to help you get stuff done
- Password and SSH key auth with SSH agent support
- Persistent connections for performance

To install, simply open up Package Control through `Ctrl+Shift+P`, Select `Install Package` and select `SFTP`. You then have to configure the plugin for use on your current project. This is done through the SFTP/FTP context menu on the right click context menu of your root directory. Once configured, a `sftp-config.json` file will be created. This is where you tell the plugin where to map your local directory to on the remote server. The main changes I make are:

- Make sure `type` is SFTP not FTP (we like security)
- I like to set `upload_on_save` to true so the most recent copy is pushed to the server whenever I save a file (great timesaver)
- Change `host` to point to your remote servers IP/domain
- Change `user` to whatever user you have SFTP (SSH) setup for on your server.
- Change `port` to whatever port you have SSH running on (you shouldn't really be running on the default 22)
- `remote_path` should point to the directory you want to push changes to on your remote server e.g. `/home/<user>/project`

Finally, you will want to make sure you are authenticating in some way. You *could* use a password, but you really should be using public key authentication. As such, change the `ssh_key_file` property to point to the absolute path to your key file. This caused me some confusion initially as I used the `id_rsa` OpenSSH key I use for SSH under Cygwin. For *nix systems this should work fine, however on Windows it turns out that Sublime uses PSFTP (PuTTY SFTP) instead, so it expects a PuTTY private key file (`.ppk` extension). If you get a lot of `Connection Refused` errors from Sublime and `No authentication found` errors in the SSH logs, this could be the reason. If all is setup correctly, you should be able to push files to the remote server.

The SFTP/FTP menu also provides some additional options such as Syncing your Remote/Local directories and Browsing your remote. Note that this is the 'Remote' workflow whereby you are editing a copy of the files on your local machine. There is also a 'Server' workflow which allows you to work directly off the server.

Just like Sublime Text itself, the plugin is not officially free. However, the trial never ends - just prompts you to purchase every so often. For more information on the plugin, visit the official page <https://wbond.net/sublime_packages/sftp>.
