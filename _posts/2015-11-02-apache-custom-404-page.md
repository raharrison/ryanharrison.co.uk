---
layout: post
title: Apache - Create a Custom 404 Page
tags:
  - apache
  - server
---

By default, Apache will provide you with a simple 'Not Found' page in the event of a 404 error. Although this does the job, it's often better to provide users with a more relevant 404 page - perhaps including a link back to your homepage.

In the Apache web server, it is very quick to modify the page served when various errors occur. First, you need to create your new `404.html` page and place it somewhere in your html folder (normally `/var/www/html`). You can place it inside a subfolder, but it normally resides in the root folder - something like `/var/www/html/404.html`. The name of the document is not important.

Next, you just need to modify an Apache config file to point to your new page in the event that a 404 error occurs. A lot of other guides direct you to create a `.htaccess` file, but I prefer to simply modify the main `VirtualHost` (plus you don't get the slight performance hit of accessing the `.htaccess` file upon every page load). The config file is located in `/etc/apache2/sites-enabled/000-default.conf`. Open it up in your favourite text editor (in this case nano, although feel free to use vim if you know how to exit it). You will need root privileges to be able to modify this file.

`$ sudo nano /etc/apache2/sites-enabled/000-default.conf`

(this is really just a symlink to /etc/apache2/sites-available/000-default.conf, so you could also directly modify this file instead)

Inside this file, you will see the main Apache `VirtualHost` serving files from `/var/www/html` on port 80. By default it will look something like:

    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

To include your custom 404 page, it's just a one line addition inside the `VirtualHost` tag. This basically just directs Apache to serve the 404.html file when it encounters a 404 error.

`ErrorDocument 404 /404.html`

Similarly, you can also add other custom pages for other error codes such as 500/503 etc. Afterwards, the file should look something like this (here I have also added custom pages for a couple other errors).

    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        ErrorDocument 404 /404.html
        ErrorDocument 500 /500.html
        ErrorDocument 503 /503.html
    </VirtualHost>

Finally, once you have made all your changes, restart the Apache server to pick up the new settings:

`$ sudo service apache2 restart`

Your new error pages should now be setup and running. To test, visit a page on your site which doesn't exist. You should be greeted with your new 404 page:

![404 page]({{ site.url }}/images/2015/404-page.jpg){: .center-image width="570"}

