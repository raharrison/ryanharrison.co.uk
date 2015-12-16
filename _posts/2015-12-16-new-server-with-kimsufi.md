---
layout: post
title: New Dedicated Server with Kimsufi
tags:
  - server
  - dedicated
  - kimsufi
---

In a [previous post][1] I talked about how I needed to move away from shared hosting to a server where I could get root access. Initially I looked at getting a VPS with Hostgator, but the prices seemed too steep for me with the specs they were offering. I then started to shop around, trying to find a VPS with a reasonable price to performance ratio. There are a ton of providers out there, some of course better than others. My first port of call was DigitalOcean who are a very popular provider of servers. For around £10 per month you can get 1GB of RAM and 1 processing core. They are very good if you want to spin up a server for a few hours, but as I intended on having mine up 24/7, I again thought I could do better price wise.

I then visited OVH who are known to provide extremely cheap VPS's. At the time of writing, for around the same price you can get 2 vCores, 8GB of RAM and 40GB of SSD disk space. They certainly do live up to their reputation. They are known to not provide the best support on the market, but for that price I think that's quite reasonable. Besides, I don't really want to rely on support to fix my software issues - it's definitely good experience to figure out Unix issues yourself (and I definitely have had to).

I was just about to order myself a VPS with OVH when I got linked to one of their partners - [Kimsufi][2]. They are a separate company yet their servers are  located in OVH's datacentres so you still get access to their extensive infrastructure. Kimsufi don't really market their servers towards commercial needs, their website targets training, hosting and sandboxing - perfect! Kimsufi offer a set of 7 dedicated server models for crazy prices considering their specs (yes, that's right they are dedicated not VPS's). For around £12 you can get yourself a Core i5 and 16GB's of RAM or for just £25 per month you can get yourself dual Xeon processors and 24GB's of RAM - crazy right? The low price does of course come with it's drawbacks. Kimsufi will tell you themselves that they offer barebones support. If you have a software problem, then expect to have to fix it yourself. Of course they will still fix your server's hardware if it fails at any point. I settled on the KS-3 model which gives you your very own dedicated server with:

 - Intel Core i5-3570s @ 3.10GHz (4 cores)
 - 16GB RAM
 - 2TB Disk Space
 - 100 Mbps network link (unmetered)
 - 1 dedicated IPv4 and Ipv6 address

It was a little more than I wanted to pay, but who doesn't want their own dedicated quad core server? With these specs I was also able to set up a lot more software than I initially intended and I never have to worry about the performance implications. Although I wanted to get hold of a Kimsufi server, it wasn't that easy however, if you look at their [website][2] you will most likely see that all of the models are currently being replenished. They do become available every so often, but they sell out again almost immediately. Handily, there are a couple of websites which will alert you when a particular model becomes available so you can pounce as fast as possible:

 - <http://www.availability.ovh/>
 - <http://kimi.nwwebsites.co.uk/>

Whenever you get an alert email make sure you take action straight away. It takes some effort to get hold of one these servers. Also expect the ordering process to fail right at the end when they sell out whilst you are ordering (they don't reserve you one during checkout). It took a while, but eventually I got hold of a KS-3 and I've been very happy with it so far (~6 months). In the end my processor was even better than the one they advertise and otherwise you get exactly what you pay for. The control panel is simple but functional (I've never really needed use it apart from when installing an initial Linux distribution) and the network speeds are great. I've had a lot of fun and learnt a load setting up and configuring a Linux server (I will post more about this in the future). If you are looking to do the same and want to get your hands on a dedicated server, then I would definitely recommend you check out [Kimsufi][2].

  [1]: {% post_url 2015-11-14-hostgator-experiences %}
  [2]: https://www.kimsufi.com/uk/

