---
layout: post
title: Ubuntu Server Setup Part 9 - Setup a  Reverse Proxy with Nginx
tags:
    - ubuntu
    - server
    - nginx
    - server
    - reverse proxy
    - proxy
    - request
typora-root-url: ../..
---

-   [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016/2016-03-29-ubuntu-server-setup-part-1-logging-in %})
-   [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018/2018-03-11-ubuntu-server-setup-part-2-securing-login %})
-   [Part 3 - Installing a Firewall]({{ site.baseurl }}{% post_url 2018/2018-07-31-ubuntu-server-setup-part-3-setup-firewall %})
-   [Part 4 - Setup Nginx Web Server]({{ site.baseurl }}{% post_url 2018/2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %})
-   [Part 5 - Install Git, Ruby and Jekyll]({{ site.baseurl }}{% post_url 2018/2018-08-27-ubuntu-server-setup-part-5-git-ruby-jekyll %})
-   [Part 6 - HTTPS With Let's Encrypt]({{ site.baseurl }}{% post_url 2018/2018-09-12-ubuntu-server-setup-part-6-https-with-lets-encrypt %})
-   [Part 7 - Email Forwarding with Postfix]({{ site.baseurl }}{% post_url 2018/2018-10-10-ubuntu-server-setup-part-7-forward-email-postfix %})
-   [Part 8 - Sending Email Through Gmail]({{ site.baseurl }}{% post_url 2018/2018-10-30-ubuntu-server-setup-part-8-sending-email-through-gmail %})
-   [Part 10 - Install Docker and Docker Compose]({{ site.baseurl }}{% post_url 2022/2022-02-24-ubuntu-server-setup-part-10-install-docker %})

In the [previous part]({{ site.baseurl }}{% post_url 2018/2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %}) we covered how to set-up Nginx as a web server to serve static content. In this part, we will configure Nginx as a reverse proxy (one of the main other use cases) to be able to access other services running locally on your server without opening up a dedicated port.

## What is a Reverse Proxy?

A reverse proxy can be thought of as a simple 'passthrough', whereby specific requests made to your web server get routed to other applications running locally and their responses returned as though they were all handled by the one server. For example, you wanted to give public access to a Python server you have running on port 8080. Instead of directly opening up the port and thus increasing the overall attack surface, Nginx can be configured to proxy certain requests to that server instead. This also has the advantage of easily enabling HTTPS for all services without having to configure each application separately and you get all the other advantages of a high performance web server like load balancing etc.

Follow the steps in the [previous tutorial]({{ site.baseurl }}{% post_url 2018/2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %}) to setup Nginx and also optionally [enable HTTPS]({{ site.baseurl }}{% post_url 2018/2018-09-12-ubuntu-server-setup-part-6-https-with-lets-encrypt %}). The rest of this part assumes you have another server running on your machine listening on localhost under port `8080`.

## Configure NGINX

Open up the main configuration file for your site:

```shell
$ sudo nano /etc/nginx/sites-available/yourdomain.com
```

```nginx
server {
  listen 80;
  listen [::]:80;

  server_name yourdomain.com;

  location /otherapp {
      proxy_pass http://localhost:8080/;
  }
}
```

The `proxy_pass` directive is what makes this configuration a reverse proxy. It specifies that all requests which match the location block (in this case the root `/otherapp` path) should be forwarded to port `8080` on `localhost`, where our other app is running.

Test the new configuration to see if there are any errors

```shell
$ sudo nginx -t
```

If there are no errors present, reload the Nginx config

```shell
$ sudo nginx -s reload
```

In a browser, navigate to your main public domain and append `/otherapp` to the end e.g. http://yourdomain.com/otherapp. Because the URL matches the `location` element in the config above, Nginx will forward the request to our other server running on port `8080`.

## Additional Options

For basic applications, the main `proxy_pass` directive should work just fine. However, as you would expect, Nginx offers a number of other options to further configure the behaviour of the reverse proxy.

In the below configuration, proxy buffering is switched off - this means that the request body will be forwarded to the proxied server immediately as it is received, which can be useful for some real-time apps. A custom header `X-Original-IP` is also set on the forwarded request, containing the IP from the original request (which can then be picked up by the other server as needed).

```nginx
location /otherapp {
    proxy_pass http://localhost:8080/;
    proxy_buffering off;
    proxy_set_header X-Original-IP $remote_addr;
}
```
