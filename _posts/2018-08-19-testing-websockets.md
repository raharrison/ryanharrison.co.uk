---
layout: post
title: Testing WebSockets
tags:
  - websocket
  - test
  - wscat
typora-root-url: ..
---

Like any other web service, websockets also need to be tried out and tested. The only problem is they aren't quite as easy to deal with as your standard REST endpoints etc as you can't just point to the URL and inspect whatever output is sent back. Websockets are persistent, so instead you need some way of hanging on to the connection in order to see output as it might arrive in various intervals, as well as send adhoc messages down the wire.

[PostMan](https://www.getpostman.com/) is generally my go-to choice of testing any web related service and for pretty much any other web service it works great. Unfortunately though, PostMan doesn't have the capability of handling websockets (yet I hope), meaning that other tools must be used if you want a quick and dirty way of displaying/sending messages.

## In the Browser

The simplest way to see what's happening is to use the browser itself - just as it would probably be used on the site itself later on. Using the built in developer tools, you can open up an adhoc `WebSocket` connection and interact with it as required.

**Open Console**

Open up the `Developer Tools` (`F12`) and go to the `Console` tab (FireFox works similarly). Here you can enter `WebSocket` related commands as necessary without having a to run a dedicated site/server.

**Note:** If you are not running a secured WebSocket (i.e not with the `wss:` protocol), you will have to visit an `HTTP` site before you open the console. This is because the browser will not allow unsecured websocket connections to be opened on what should otherwise be a secured `HTTPS` page.

The below example runs through the code needed to open a `WebSocket` connection, send content to the server and log the output as it is received:

**Open Connection**

```javascript
ws = new WebSocket("ws://localhost:8080/ws"); // create new connection
```

**List to events**

```javascript
// When the connection is open
ws.onopen = function () {
  connection.send('Ping');
};

// Log errors
ws.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
ws.onmessage = function (e) {
  console.log('From Server: ' + e.data);
};
```

**Send Messages**

```javascript
// Sending a String
ws.send('your message');
```

**Close Connection**

```javascript
ws.close() // not necessarily required
```

## WsCat

The web browser approach works well enough, but it is a bit cumbersome to have to paste in the code each time. There are however many tools which abstract this away into helpful command line interfaces. [Wscat](https://github.com/websockets/wscat) is one such terminal based tool which makes testing websockets just about as easy as it gets.

There isn't much to `wscat`, just point it to your server URL and it will log out any messages received or send any as you type them. It's based on Node (see below for similar alternatives in other environments) so just install through `npm` and run directly within the console.

<https://github.com/websockets/wscat>

```shell
npm install -g wscat
```

```shell
$ wscat -c ws://localhost:8080/ws
connected (press CTRL+C to quit)
> pong
< ping
> ping
< pong
```

## Other Tools

Here are some other related tools (most just like `wscat`). [This GitHub repo guide](https://github.com/facundofarias/awesome-websockets) also has plenty of other websocket related tools you might want to check out.

<https://github.com/thehowl/claws>

- Go based
- Json formatting and pipes

<https://github.com/esphen/wsta>
- Rust based
- most advanced
- very pipe friendly
- configuration profiles

<https://github.com/progrium/wssh>
- Python based
- equivalent of `wscat` if `Node` is not your thing