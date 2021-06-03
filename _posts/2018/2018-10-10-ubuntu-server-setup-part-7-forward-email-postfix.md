---
layout: post
title: Ubuntu Server Setup Part 7 - Email Forwarding with Postfix
tags:
    - ubuntu
    - server
    - email
    - mail
    - postfix
    - domain
    - forward
typora-root-url: ../..
---

-   [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016/2016-03-29-ubuntu-server-setup-part-1-logging-in %})
-   [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018/2018-03-11-ubuntu-server-setup-part-2-securing-login %})
-   [Part 3 - Installing a Firewall]({{ site.baseurl }}{% post_url 2018/2018-07-31-ubuntu-server-setup-part-3-setup-firewall %})
-   [Part 4 - Setup Nginx Web Server]({{ site.baseurl }}{% post_url 2018/2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %})
-   [Part 5 - Install Git, Ruby and Jekyll]({{ site.baseurl }}{% post_url 2018/2018-08-27-ubuntu-server-setup-part-5-git-ruby-jekyll %})
-   [Part 6 - HTTPS With Let's Encrypt]({{ site.baseurl }}{% post_url 2018/2018-09-12-ubuntu-server-setup-part-6-https-with-lets-encrypt %})
-   [Part 8 - Sending Email Through Gmail]({{ site.baseurl }}{% post_url 2018/2018-10-30-ubuntu-server-setup-part-8-sending-email-through-gmail %})
-   [Part 9 - Setup a Reverse Proxy with Nginx]({{ site.baseurl }}{% post_url 2019/2019-06-16-ubuntu-server-setup-part-9-reverse-proxy-nginx %})

One of the best things about owning your own domain name is being able to use it as a custom email address. Many companies provide this service for a monthly fee, but if you have your own personal server/VPS already anyway, then you might as well take advantage of it.

Many custom email solutions are very heavyweight and include setting up [Postfix](http://www.postfix.org/), [Dovecot](https://www.dovecot.org/) (`IMAP` and `POP3` server) and some client like [Roundcube](https://roundcube.net/). You also have to worry about spam so will also need something like [spamassassin](https://spamassassin.apache.org/). Not to mention all the security and redundancy issues involved in storing and maintaining your own (sensitive) data. If you want an all-in-one bundle of all the above, check out [Mail-in-a-Box](https://mailinabox.email/).

That's all well and good for some use cases, but wouldn't it be nicer if you could use your existing Gmail account to handle email traffic for your custom domain? Integration with all your devices, access to your other email accounts, built in spam detection and you will be managing much less infrastructure.

This part covers the first part of getting to that solution - forwarding all email that comes to your domain onto your existing Gmail account. The second part will then cover the other half of the story which is how to send email as your custom domain from within Gmail.

In short, at the end of this part all email to `me@yourdomain.com` will be forwarded on to `you@gmail.com` automatically. It is assumed that you have control over a domain name, can change DNS properties, and have an existing Gmail account.

## DNS Setup

The first step is to configure a couple of DNS records to ensure that email traffic gets routed to your server correctly (`MX` record). The others are to help out in the battle against Gmail thinking that all your mail is spam and for them to correctly validate your server as being in control over your domains mailbox. In whatever DNS control panel your have, create the following:

-   An `A` record pointing `yourdomain.com` to your servers IP address
-   An `MX` record pointing `yourdomain.com` to the IP of your server (or `@` to point to your `A` record)
-   A `PTR` (reverse DNS) record pointing your servers IP to `yourdomain.com`. This allows Gmail to verify the legitimacy of our server via its IP when Gmail receives a forwarded e-mail from it.
-   An `SPF` record with the contents `v=spf1 mx a ip4:<yourip>/32 include:_spf.google.com ~all` (replacing with your own IP address)

The SPF record tells Gmail that only the servers specified are allowed to send e-mails purporting to be from `yourdomain.com` All other servers attempting to do the same will be rejected - which helps a lot with spam.

## Install and Configure Postfix

Now to get to the core part - installing Postfix and configuring it to forward all email to your Gmail account.

```shell
$ sudo apt-get install postfix
```

During the installation process, you will be be prompted a couple times. Choose the `Internet Site` option and provide your domain name into the inputs.

### /etc/postfix/main.cf

Once Postfix is installed, open up it's main configuration file:

```shell
$ sudo nano /etc/postfix/main.cf
```

The file will already contain a bunch of configuration options. In the second part I will provide the full configuration, but in this part just paste in the below. This basically just tells Postfix what our domain name is and sets some network properties.

The most important part is the bottom two lines which sets up alias mappings. This will tell Postfix that for all traffic to `yourdomain.com` perform a lookup into `/etc/postfix/virtual` to find out where to forward it on to.

```
myhostname = yourdomain.com
mydomain = yourdomain.com
myorigin = /etc/mailname
mydestination = yourdomain.com, localhost.localdomain, localhost
relayhost =
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = all
inet_protocols = ipv4

virtual_alias_domains = yourdomain.com
virtual_alias_maps = hash:/etc/postfix/virtual
```

### /etc/postfix/virtual

Now to edit the virtual mappings file to tell Postfix to forward our mail onto your Gmail account:

```shell
$ sudo nano /etc/postfix/virtual
```

Within that file, you can provide your domain name, followed by a whitespace and a comma separated list of domains to forward it to. In this case we are forwarding everything which comes to `me@yourdomain.com` onto your Gmail account. You can just provide `yourdomain.com` as the first parameter to forward all email regardless of address.

```
# Forwarding mapping, one from-to address pair per line. The format is:
#     <forward-from-addr> <whitespace> <forward-to-addr>
me@yourdomain.com you@gmail.com
```

### Update lookup table

Postfix doesn't directly read the virtual file, but instead generates a lookup table from it. Run the following to refresh the lookup table:

```shell
$ sudo postmap /etc/postfix/virtual
```

### Reload Postfix

```shell
$ sudo service postfix start # if not already running

$ sudo service postfix reload # reload our config files

$ sudo service postfix restart # or perform a restart
```

## Configure Firewall

`SMTP` traffic (which Postfix is handling and forwarding) runs on port 25, so makes sure to allow it through your firewall. Refer to [Part 3]({{ site.baseurl }}{% post_url 2018/2018-07-31-ubuntu-server-setup-part-3-setup-firewall %}) for info on how to set one up.

```shell
$ ufw allow 25/tcp
```

## Testing

After any new DNS records have propagated, you can test by sending an email to `me@yourdomain`. It should be forwarded onto `me@gmail.com` pretty quickly (make sure to also check your spam folder).

If you tried to the above and never received the email in your Gmail inbox, try checking the Postfix logs at `/var/log/mail.log` for errors.

That's it for this part, in the next part we will cover how to send email from Gmail, relaying through our server to appear as though it was sent by our custom domain.
