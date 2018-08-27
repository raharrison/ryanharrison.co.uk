---
layout: post
title: Ubuntu Server Setup Part 5 - Install Git, Ruby and Jekyll
tags:
  - ubuntu
  - server
  - git
  - ruby
  - jekyll
typora-root-url: ..
---

- [Part 1 - Logging In]({{ site.baseurl }}{% post_url 2016-03-29-ubuntu-server-setup-part-1-logging-in %})
- [Part 2 - Securing Login]({{ site.baseurl }}{% post_url 2018-03-11-ubuntu-server-setup-part-2-securing-login %})
- [Part 3 - Installing a Firewall]({{ site.baseurl }}{% post_url 2018-07-31-ubuntu-server-setup-part-3-setup-firewall %})
- [Part 4 - Setup Nginx Web Server]({{ site.baseurl }}{% post_url 2018-08-08-ubuntu-server-setup-part-4-setup-nginx-server %})

This part will take care of installing everything necessary to allow the new server to host your personal blog (or other [Jekyll](https://jekyllrb.com/) site). As a prerequisite, you will also need some kind of web server installed (such as [Nginx](https://www.nginx.com/) or [Apache](https://httpd.apache.org/)) to take care of serving your `HTML` files over the web. Part 4 covers the steps for my favourite - Nginx.

## Install Git

As I store my blog as a public repo [on GitHub](https://github.com/raharrison/ryanharrison.co.uk), `Git` first needs to be installed to allow the repo to be cloned and new changes to be pulled. Git is available in the Ubuntu repositories so can be installed simply via `apt`:

```shell
sudo apt install git
```

You might also want to modify some Git config values. This is only really necessary if you plan on committing changes from your server (so that your commit is linked to your account). As I only tend to `pull` changes, this isn't strictly required.

```shell
sudo apt install git
git config --global color.ui true
git config --global user.name "me"
git config --global user.email "email
```

## Helpful Git Aliases

Here are a few useful Git aliases from my `.bashrc`. You can also add aliases through Git directly via the [alias command](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases).

```shell
alias gs='git status'
alias ga='git add'
alias gaa='git add .'
alias gp='git push'
alias gpom='git push origin master'
alias gpu='git pull'
alias gcm='git commit -m'
alias gcam='git commit -am'
alias gl='git log'
alias gd='git diff'
alias gdc='git diff --cached'
alias gb='git branch'
alias gc='git checkout'
alias gra='git remote add'
alias grr='git remote rm'
alias gcl='git clone'
alias glo='git log --pretty=format:"%C(yellow)%h\\ %ad%Cred%d\\ %Creset%s%Cblue\\ [%cn]" --decorate --date=short'
```

More helpful aliases:

- [Must Have Git Aliases: Advanced Examples](http://durdn.com/blog/2012/11/22/must-have-git-aliases-advanced-examples/)
- [16 Awesome Git Aliases](http://codersopinion.com/blog/16-awesome-git-aliases-that-you-will-love/)

## Install Ruby

[Ruby](https://www.ruby-lang.org/en/) is also available in the Ubuntu repositories. You will also need `build-essential` to allow you to compile `gems`.

```shell
sudo apt install ruby ruby-dev build-essential
```

It's a good idea to also tell Ruby where to install gems - in this case your home directory via the `GEM_HOME` environment variable. Two lines are added to `.bashrc` to ensure this change is kept for new shell sessions:

```shell
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME=$HOME/gems' >> ~/.bashrc
echo 'export PATH=$HOME/gems/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

You should now be able to run `ruby -v` to ensure everything is working.

To get more control over the Ruby installation (install new versions or change versions on the fly), check out [rbenv](https://github.com/rbenv/rbenv) or [rvm](http://rvm.io/rvm/install).

## Install Jekyll

Once Ruby is installed, the Jekyll gem can be installed via `gem`:

```shell
gem install jekyll bundler
```

I also use some extra [Jekyll plugins](https://jekyllrb.com/docs/plugins/) which can also be installed as gems:

```shell
gem install jekyll-paginate
gem install jekyll-sitemap
```

As the path to the Ruby gems directory has been added to the `PATH` (in the previous section), the `jekyll` command should now be available:

```shell
jekyll -v
jekyll build
```

## Automated Build

Here is a simple bash script which pulls the latest changes from Git, builds the Jekyll site and copies the site to a directory as to be served by your web server (default location is `/var/www/html`).

```bash
#!/bin/bash

echo "Pulling latest from Git";
cd ~/blog/ && git pull origin master;

echo "Building Jekyll Site";
jekyll build --source ~/blog/ --destination ~/blog/_site/;
echo "Jekyll Site Built";

echo "Copying Site to /var/www/html/";
cp -rf ~/blog/_site/* /var/www/html/;
echo "Site Copied Successfully";
```
