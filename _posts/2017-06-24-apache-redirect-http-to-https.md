---
layout: post
title: Apache - Redirect HTTP to HTTPS
tags:
  - apache
  - redirect
  - http
  - https
---

With all the focus these days on cybersecurity and the push towards a more secure web, it's more important than ever to ensure as many users as possible are using the HTTPS version of your site instead of the default HTTP version. Google search results will now rank secure versions better than their variations and some browsers are actively warning users if they are not browsing through HTTPS and there is a password input field on the page for example.

As such, having all of your standard HTTP traffic automatically redirect to their HTTPS equivalent can not only help reassure your visitors, but also potentially increase traffic as a whole. There really aren't any excuses for not using HTTPS now when [Let's Encrypt](https://letsencrypt.org/) is available.

Configuring redirects within your web server of choice is quite trivial. In this post I will focus on Apache, however I am sure the config is equally as straightforward if you are an Nginx user.

The first step is of course to make sure that you have a HTTPS version of your site available to the public. There are a thousand guides online about how to to this so I won't cover it again here, but in short get a certificiate for your domain from Let's Encrypt via certbot, create a new `VirtualHost` within Apache listening on port `443` and enable `SSLEngine` - pointing to your certificate. At this point your should have two versions of your site available - one through HTTP and one through HTTPS. At the end of this all of the HTTP traffic will be redirected the HTTPS virtual host.

Navigate to your main Apache config file which contains your HTTP virtual host definition. This is normally in `/etc/apache2/sites-available` and might be called something like `000-default.conf` if you haven't renamed it. If the first line of the file is `<VirtualHost *:80>` you are in the right place.

Open this file with your favourite text editor (you will need root privileges) and add the following, replacing "your-domain-name" with, of course, your domain name:

    # Redirect to HTTPS
    Redirect permanent / https://your-domain-name.com/

And that's it. Run the command `sudo service apache2 restart` to pick up the changes and then test it out. Navigating to any of your pages through HTTP should be automatically redirected to HTTPS resulting in that nice green padlock in your browser.





