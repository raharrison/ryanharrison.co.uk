---
layout: post
title: How to use Google DNS Servers
tags:
  - dns
  - google
  - server
---

If you are frequently running into the `Resolving Host` status message in Chrome and/or are generally having slow page loads, it could be because your DNS lookups are taking longer than they should. Unsurprisingly, the DNS servers provided by your ISP can be pretty bad, but you are free to use other open alternatives (the two most common being Google and OpenDNS) which could give you faster responses.

Follow these steps to use the open Google DNS servers within Windows 10 (there are plenty of alternative guides online for other OS's):

`Start -> Settings -> Network & Internet`

Click on `Change adapter options`

Select which network adapter you are using (WiFi/Ethernet depending on your setup). Right click and choose `Properties`.

In the list of configuration options select `Internet Protocol Version 4 (TCP/IPv4)`. Then click `Properties`.

![Adapter Properties](/images/2017/dns-network-properties.png)

In the bottom section, select `Use the following DNS server addresses`. Fill the boxes with the following depending on which provider you wish to use:

[Google DNS](https://developers.google.com/speed/public-dns/)

Preferred: 8.8.8.8<br>
Alternate: 8.8.4.4

[OpenDNS](https://www.opendns.com/)

Preferred: 208.67.222.222<br>
Alternate: 208.67.220.220

For Google DNS, it should look like the following:

![Configure DNS Servers](/images/2017/dns-configure-properties.png)

Hit OK and you should be good to go. There are also equivalent IP addresses for IPv6 if you need them. Hopefully your DNS lookups will not be a little more performant. You might have the potential downside of Google knowing even more about your browsing habits, but if you use Chrome then they probably know all that already - so you might as well enjoy a faster experience!