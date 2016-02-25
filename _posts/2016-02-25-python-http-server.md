---
layout: post
title: Python - Simple HTTP Server
tags:
  - python
  - http
  - server
---

Python comes with a really handy built-in HTTP server that you can get up and running in a matter of seconds - and without having to mess around with something like Apache. This is great for serving simple web pages locally through HTTP to get around the limitations of the `file://` protocol within the browser.

The command to start the server unsurprisingly differs from Python 2 to Python 3, but either way it's really easy to remember. Simply open up a terminal, change directory to the folder containing the files you want to serve and either of the following to start the server depending on your Python version:

####Python 2:

    cd files/my-directory
    python -m SimpleHTTPServer

    Serving HTTP on 0.0.0.0 port 8000 ...

####Python 3:

    cd files/my-directory
    python -m http.server

    Serving HTTP on 0.0.0.0 port 8000 ...

Then navigate to `http://localhost:8000` in your browser to see your files (by default you get a directory listing if there is no `index.html` file).

You can also specify the port you want to use if 8000 doesn't work for you:

    python -m SimpleHTTPServer 8080
    python -m http.server 8080

    Serving HTTP on 0.0.0.0 port 8080 ...