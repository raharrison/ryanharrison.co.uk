---
layout: post
title: Ubuntu Server Setup Part 4 - Setup Nginx Web Server
tags:
    - ubuntu
    - server
    - nginx
typora-root-url: ../..
---

-   [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016/2016-03-29-ubuntu-server-setup-part-1-logging-in %})
-   [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018/2018-03-11-ubuntu-server-setup-part-2-securing-login %})
-   [Part 3 - Installing a Firewall]({{ site.baseurl }}{% post_url 2018/2018-07-31-ubuntu-server-setup-part-3-setup-firewall %})
-   [Part 5 - Install Git, Ruby and Jekyll]({{ site.baseurl }}{% post_url 2018/2018-08-27-ubuntu-server-setup-part-5-git-ruby-jekyll %})
-   [Part 6 - HTTPS With Let's Encrypt]({{ site.baseurl }}{% post_url 2018/2018-09-12-ubuntu-server-setup-part-6-https-with-lets-encrypt %})
-   [Part 7 - Email Forwarding with Postfix]({{ site.baseurl }}{% post_url 2018/2018-10-10-ubuntu-server-setup-part-7-forward-email-postfix %})
-   [Part 8 - Sending Email Through Gmail]({{ site.baseurl }}{% post_url 2018/2018-10-30-ubuntu-server-setup-part-8-sending-email-through-gmail %})
-   [Part 9 - Setup a Reverse Proxy with Nginx]({{ site.baseurl }}{% post_url 2019/2019-06-16-ubuntu-server-setup-part-9-reverse-proxy-nginx %})
-   [Part 10 - Install Docker and Docker Compose]({{ site.baseurl }}{% post_url 2022/2022-02-24-ubuntu-server-setup-part-10-install-docker %})

Serving web pages is one of the most common and useful use cases of a cloud server. [Nginx](https://www.nginx.com/) is popular and handles some of the largest sites on the web. It's configuration is simplistic but very powerful and Nginx can often use less resources than an equivalent Apache server.

## Install Nginx

Nginx is available in the default Ubuntu repositories, so installation is simple through `apt`:

```shell
$ sudo apt update
$ sudo apt install nginx
```

That's all you need to do for the base install of Nginx. By default, the service is started and Nginx includes a simple default landing page (located in `/var/www/html`) which you should now be able to access via the web.

## Access through the Web

First, make sure that Nginx is running on your system. If using a modern Ubuntu server installation, you can do this via `systemd`:

```shell
$ sudo systemctl status nginx
```

```
● nginx.service - A high performance web server and a reverse proxy server
   Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
...
```

If Nginx is not already running, use the following to start the service:

```shell
$ sudo systemctl start nginx

# other useful commands
$ sudo systemctl stop nginx
$ sudo systemctl restart nginx
$ sudo systemctl reload nginx # reload config without dropping connections
$ sudo systemctl disable nginx # don't start nginx on boot
$ sudo systemctl enable nginx # do start nginx on boot
```

Also check that your firewall (if any) is setup to allow connections on port 80 (for `HTTP`). Refer to the [previous part in this series]({{ site.baseurl }}{% post_url 2018/2018-07-31-ubuntu-server-setup-part-3-setup-firewall %}) for instructions using `ufw`.

Now you can check that everything is working correctly by accessing your web server through the internet. If you don't already know the external IP for you server, run the following command:

```shell
$ dig +short myip.opendns.com @resolver1.opendns.com
```

When you have your server's IP address, enter it into your browser's address bar. You should see the default Nginx landing page.

```
http://your_server_ip
```

## Customise Nginx Config

All of the Nginx configuration files are stored within `/etc/nginx/` and it is laid out similarly to an Apache installation.

To create a new configuration - `server block` in Nginx, `virtual host` in Apache - first create a file within `/etc/nginx/sites-available`. It is good convention to use the domain name as the filename:

```shell
$ sudo nano /etc/nginx/sites-available/yourdomain.com
```

Within this file, create a new server block structure:

```nginx
server {
        listen 80;
        listen [::]:80;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name yourdomain.com www.yourdomain.com;

        location / {
                try_files $uri $uri/ =404;
        }
}
```

This server block will listen to requests on port 80 (`HTTP` requests) and will serve resources from the default `/var/www/html` directory. This can be changed as necessary - ideally a dedicated root directory per server block. The `server_name` is set to the domain name(s) you wish to serve. This is useful if you want to add `HTTPS` via [Let's Encrypt](https://letsencrypt.org/) later on.

Next, this server needs to be enabled by creating a symlink within the `/etc/nginx/sites-enabled` directory:

```shell
$ sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
```

You may also wish to delete the default configuration file unless you want to fall back to the defaults:

```shell
$ sudo rm /etc/nginx/sites-enabled/default
```

As we have added additional server names (our domains), it is good to correct the hash bucket size for server names to avoid potential conflicts later on:

```shell
$ sudo nano /etc/nginx/nginx.conf
```

Find the `server_names_hash_bucket_size` directive and remove the `#` symbol to uncomment the line:

```nginx
...
http {
    ...
    server_names_hash_bucket_size 64;
    ...
}
...
```

Finally, it's time to restart Nginx in order to reload our config. But first, you can see if there are any syntax errors in your files:

```shell
$ sudo nginx -t
```

If there aren't any problems, restart Nginx to enable the changes:

```shell
$ sudo systemctl restart nginx
```

Nginx will now serve requests for `yourdomain.com` (assuming you have set up an `A` DNS record pointing to your server). Navigate to `http://yourdomain.com` and you should see the same landing page as before. Any new files added to `/var/www/html` will also be served by Nginx under your domain.

## Enable HTTPS

If you already have `SSL` certificates for your domain names, you can easily setup Nginx to handle `HTTPS` requests. Makes sure that your firewall is setup to allow connections on port 443 first:

```nginx
server {
        listen 443 ssl;
        listen [::]:443 ssl;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name yourdomain.com www.yourdomain.com;

        location / {
                try_files $uri $uri/ =404;
        }

        ssl_certificate /etc/ssl/certs/example-cert.pem;
        ssl_certificate_key /etc/ssl/private/example.key;

        ssl_session_cache shared:le_nginx_SSL:1m;
        ssl_session_timeout 1440m;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_ciphers "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS";
}
```

The above uses the same configuration as Let's Encrypt to set strong ciphers and disable old versions of SSL. This should get you an A in [SSLTest](https://www.ssllabs.com/ssltest/). I will also add a post on setting up [Let's Encrypt](https://letsencrypt.org/) with Nginx to automate the process of using free SSL certificates for your site.

## Custom Error Pages

By default, Nginx will display it's own error pages in the event of a `404/50x` error etc. If you have your own versions, you can use the `error_pages` directive to specify a new path. Open up your server block config and add the following:

```nginx
server {
    ...
    error_page 404 /custom_404.html;
    error_page 500 502 503 504 /custom_50x.html;
    ...
}
```

If required, you can also specify a completely new location (not in the main `root` directory of the server block) for your error pages by providing a `location` block which resolves the specified error page path:

```nginx
server {
    ...
    error_page 404 /custom_404.html;
    location = /custom_404.html {
        root /var/html/custom;
        internal;
    }
    ...
}
```

## Log File Locations

-   `/var/log/nginx/access.log`: Every request to your web server is recorded in this log file unless Nginx is configured to do otherwise.
-   `/var/log/nginx/error.log`: Any Nginx errors will be recorded in this log file.
