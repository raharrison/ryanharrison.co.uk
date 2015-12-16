---
layout: post
title: Speed Test in the Terminal
tags:
  - speedtest
  - terminal
  - cli
---

Finding your current download and upload speeds as long been the job of <http://www.speedtest.net>. This is fine for machines whereby you have access to a Javascript enabled browser, but particularly for servers, you have to find an alternative that you can use through the terminal.

Handily, there is an [open source project on GitHub ](https://github.com/sivel/speedtest-cli) that provides a command line interface for testing internet bandwidth using speedtest.net. The only prerequisite is that you have Python installed (any version between 2.5 and 3.4 will do).

The project provides many different methods of installation such as `pip` or `easy_install`. You can also clone the Git repository onto your machine somewhere. These will all work fine, however as the script is just one file, you can simply use `curl/wget` to download and run it directly. Using `wget`, the commands to download the script and make it executable are:

    $ wget -O speedtest-cli https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest_cli.py
    $ chmod +x speedtest-cli

Then, just run the script using `python speedtest-cli`. Just like speedtest.net, the script will choose the closest server to your machine and begin a download/upload test. The results are then output into your terminal window:

    user@machine:~/speedtest_cli$ python speedtest-cli
    Retrieving speedtest.net configuration...
    Retrieving speedtest.net server list...
    Selecting best server based on latency...
    Hosted by Heberg.fr (Roubaix) [0.72 km]: 4.621 ms
    Testing download speed........................................
    Download: 93.98 Mbit/s
    Testing upload speed..................................................
    Upload: 91.33 Mbit/s

There are also some additional switches that let your define which server you wish to use for the test. First, you need to find the corresponding id using `python speedtest_cli --list`. This will output a long list (probably best to redirect this into a file) of servers and id's. Make a note of the id you want to use and then run the command again, this time supplying said server e.g. `python speedtest_cli --server <ID>`.

For more information, visit their GitHub page at <https://github.com/sivel/speedtest-cli>.
