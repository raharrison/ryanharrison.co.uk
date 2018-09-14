---
layout: post
title: Ubuntu Server Setup Part 3 - Installing a Firewall
tags:
  - ubuntu
  - server
  - firewall
typora-root-url: ..
---

- [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016-03-29-ubuntu-server-setup-part-1-logging-in %})
- [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018-03-11-ubuntu-server-setup-part-2-securing-login %})
- [Part 4 - Setup Nginx Web Server]({{ site.baseurl }}{% post_url 2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %})
- [Part 5 - Install Git, Ruby and Jekyll]({{ site.baseurl }}{% post_url 2018-08-27-ubuntu-server-setup-part-5-git-ruby-jekyll %})
- [Part 6 - HTTPS With Let's Encrypt]({{ site.baseurl }}{% post_url 2018-09-12-ubuntu-server-setup-part-6-https-with-lets-encrypt %})

By default, your server may not come with a firewall enabled - meaning that external users will have direct access to any applications listening on any open port. This is of course a massive security risk and you should generally seek to minimise the surface area exposed to the public internet. This can be done using some kind of firewall - which will deny any traffic to ports that you haven't explicitly allowed.

I personally only allow a few ports through the firewall and make use of reverse proxies through [Nginx](https://www.nginx.com/) to route traffic to internal apps. That way you can have many applications running on your server, but all traffic is run through port `443` (with `HTTPS` for free) first.

## UFW Installation

The simplest firewall is `ufw` ([Uncomplicated Firewall](https://help.ubuntu.com/community/UFW)) and may already come pre-installed on your server. If it doesn't you can get it by running:

```shell
$ sudo apt install ufw
```

Once installed, check that the `ufw` service is running:

```bash
$ sudo service ufw status
```

## Configure Firewall Rules

The first thing you want to do is ensure that the port `ssh` is running under is allowed through the firewall (by default `22`). If you don't, then you won't be able to log in to your server anymore!

```shell
$ sudo ufw allow 22
or
$ sudo ufw allow ssh 
```

Then start the firewall by running:

```shell
$ sudo ufw enable

Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

If you have a web server running, you will notice that any `http` or `https` requests no longer work. That's because we need to allow port `80` and `443` through the firewall:

```shell
$ sudo ufw allow http
$ sudo ufw allow https
```

Your web server will now be properly accessible again. You can list the currently enabled rules in `ufw` by running:

```shell
$ sudo ufw status

Status: active

To                         Action      From
--                         ------      ----
22                         ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22 (v6)                    ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
```

`ufw` also comes with some default app profiles:

```shell
$ sudo ufw app list

Available applications:
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
  OpenSSH
  Postfix
  Postfix SMTPS
  Postfix Submission
```

You can then pass in the app name to the `allow/deny` commands:

```shell
$ sudo ufw allow OpenSSH
```

Refer to my post on [Common Port Mappings]({{ site.baseurl }}{% post_url 2016-01-26-common-port-mappings %}) to find out which ports you might need to allow through your firewall.

## List and remove rules

To delete a rule, you first need to get the index:

```shell
$ sudo ufw status numbered

[ 1] 22                         ALLOW IN    Anywhere
[ 2] 80/tcp                     ALLOW IN    Anywhere
[ 3] 443/tcp                    ALLOW IN    Anywhere
...
```

If you wanted to delete the `443 (https)` rule, pass the index `3` into the `delete` command:

```shell
$ sudo ufw delete 3

Deleting:
 allow 443/tcp
Rule deleted
```

Finally you can disable the firewall by running:

```shell
$ sudo ufw disable
```

## Allow or Deny Specific IP's

You can also `allow` or `deny` access from specific ip addresses. For example, to allow connections from only `151.80.44.180`:

```shell
$ sudo ufw allow from 151.80.44.180
```

Or to only allow access to only port `22` from that specific ip:

```shell
$ sudo ufw allow from 151.80.44.180 to any port 22
```

Similarly, if you want to `deny` all connections from a specific ip use:

```shell
$ sudo ufw deny from 151.80.44.180
```
