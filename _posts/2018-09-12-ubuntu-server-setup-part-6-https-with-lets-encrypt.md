---
layout: post
title: Ubuntu Server Setup Part 6 - HTTPS With Let's Encrypt
tags:
  - ubuntu
  - server
  - https
  - let's encrypt
  - certbot
  - certificate
typora-root-url: ..
---

- [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016-03-29-ubuntu-server-setup-part-1-logging-in %})
- [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018-03-11-ubuntu-server-setup-part-2-securing-login %})
- [Part 3 - Installing a Firewall]({{ site.baseurl }}{% post_url 2018-07-31-ubuntu-server-setup-part-3-setup-firewall %})
- [Part 4 - Setup Nginx Web Server]({{ site.baseurl }}{% post_url 2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %})
- [Part 5 - Install Git, Ruby and Jekyll]({{ site.baseurl }}{% post_url 2018-08-27-ubuntu-server-setup-part-5-git-ruby-jekyll %})

`HTTPS` is a must have nowadays with sites served under plain `HTTP` being downgraded in search results by Google and marked as insecure by browsers. The process of obtaining an `SSL` certificate used to be cumbersome and expensive, but now thankfully because of Let's Encrypt it completely free and you can automate the process with just a few commands.

This part assumes that you already have an active `Nginx` server running (as described in Part 4) and so will go over how to use Let's Encrypt with Nginx. `Certbot` (the client software) has a number of plugins that make the process just as easy if you are running another web server such as `Apache`.

## Prepare the Nginx Server

Make sure have a server block where `server_name` is set to your domain name (in this case `example.com`).

This is so `Certbot` knows which config file to modify in order to enable `HTTPS` (it adds a line pointing to the generated SSL certificates).

```nginx
server {
  	listen 80;
  	listen [::]:80;
  
  	server_name example.com www.example.com;
  	root /var/www/example;
  
  	index index.html;
  	location / {
  		try_files $uri $uri/ =404;
  	}
  }
```

That's all the preparation needed on the Nginx side. `Certbot` will handle everything else for us.

## Install and Run Certbot

`Certbot` is the client software (written in Python), that is supported by Let's Encrypt themselves to automate the whole process. There are a wide range of [different alternatives](https://letsencrypt.org/docs/client-options/) in various languages if you have different needs.

You should install `Certbot` through the dedicated `ppa` to make sure you always get the latest updates. In this example we install the Nginx version (which includes the Nginx plugin):

```shell
sudo apt-get update
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install -y python-certbot-nginx
```

Once installed, you can run `Certbot`. Here the `--nginx` flag is used to enable the Nginx plugin. Without this, `Certbot` would just generate a certificate and your web server wouldn't know about it. The plugin is required to modify the Nginx configuration in order to see the certificate and enable `HTTPS`.

```shell
sudo certbot --nginx
```

It will ask for:

- an email address (you will be emailed if there are any issues or your certs are about to expire)
- agreeing to the Terms of Service
- which domains to use `HTTPS` for (it detects the list using `server_name` lines in your Nginx config)
- whether to redirect `HTTP` to `HTTPS` (recommended)

Once you have selected these options, `Certbot` will perform a 'challenge' to check that the server it is running on is in control of the domain name. As described in the [ACME protocol](https://github.com/ietf-wg-acme/acme/) which is what underlies Let's Encrypt, there are a number of different challenge types. In this case `tls-sni` was probably performed, although `DNS` might be used for wildcard certificates.

If the process completed without errors, a new certificate should have been generated and saved on the server. You can access this via `/var/letsencrypt/live/domain`.

The Nginx server block should have also been modified to include a number of extra `ssl` related fields. You will notice that these point to the generated certificate alongside the Let's Encrypt chain cert. If you checked the option to redirect all `HTTP` traffic to `HTTPS`, you should also see another server block generated which merely captures all `HTTP` traffic and performs a redirection to the main `HTTPS` enabled server block.

**You could stop here if all you want is HTTPS** as this already gives you an `A` rating and maintains itself.

Test your site with SSL Labs using `https://www.ssllabs.com/ssltest/analyze.html?d=www.YOUR-DOMAIN.com`

## Renewal

**There is nothing to do**, `Certbot` installed a cron task to automatically renew certificates about to expire.

You can [check renewal works](https://certbot.eff.org/docs/using.html#re-creating-and-updating-existing-certificates) using:

```shell
sudo certbot renew --dry-run
```

You can also [check what certificates exist](https://certbot.eff.org/docs/using.html#managing-certificates) using:

```shell
sudo certbot certificates
```

## A+ Test

If you did the SSL check in the previous section you might be wondering why you didn't get an A+ instead of just an A. It turns out that the default policy is to use some slightly outdated protocols and cipher types to maintain backwards compatibility with older devices. If you want to get the A+ rating, add the below config to your Nginx server block (the same one that got updated by `Certbot`). In particular we only use TLS 1.2 (not 1.0 or 1.1) and the available ciphers are restricted to only the latest and most secure. **Be aware though that this might mean you site is unusable on some older devices which do not support these modern ciphers**.

```nginx
ssl_trusted_certificate /etc/letsencrypt/live/YOUR-DOMAIN/chain.pem;

ssl_session_cache shared:le_nginx_SSL:1m;
ssl_session_timeout 1d;
ssl_session_tickets off;

ssl_protocols TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
ssl_ecdh_curve secp384r1;

ssl_stapling on;
ssl_stapling_verify on;

add_header Strict-Transport-Security "max-age=15768000; includeSubdomains; preload;";
add_header Content-Security-Policy "default-src 'none'; frame-ancestors 'none'; script-src 'self'; img-src 'self'; style-src 'self'; base-uri 'self'; form-action 'self';";
add_header Referrer-Policy "no-referrer, strict-origin-when-cross-origin";
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
```