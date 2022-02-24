---
layout: post
title: Ubuntu Server Setup Part 10 - Install Docker and Docker Compose
tags:
    - ubuntu
    - server
    - docker
    - container
    - compose
    - install
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
-   [Part 9 - Setup a Reverse Proxy with Nginx]({{ site.baseurl }}{% post_url 2019/2019-06-16-ubuntu-server-setup-part-9-reverse-proxy-nginx %})

It's likely that you will want to run containers of some kind on your server, for that we'll be installing and using `Docker`. This consists of a couple different parts - the `Docker Engine` itself which runs in the background as a daemon process, the `docker` CLI commands which allow you to interact with the Engine, and finally `docker-compose` which is another tool for easily managing multiple containers. On Ubuntu based machines the recommended way of installation is to use the official Docker repository.

### Install Prerequisites and Set Up the Repository

Before we do anything more, update your local `apt` repositories and install a few prerequisite packages which are required in later steps:

```bash
$ sudo apt-get update

$ sudo apt-get install ca-certificates curl gnupg
```

Next, we need to add the official `GPG` key provided by Docker for their repository:

```bash
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Finally, we can add the official Docker repository, specifying that the releases must be signed by the `GPG` key we downloaded in the previous step. The command below will point to the `stable` repository, but you can use the `nightly` or `test` channels if you prefer:

```bash
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker

Now we have the Docker repository and keys setup, we can pull down the latest packages again and directly install Docker directly through `apt`:

```bash
$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

If everything completed successfully you should now have Docker Engine running in the background and the ability to run the `docker` CLI commands to run and manage images/containers. To verify things are working correctly, start an instance of the `hello-world` image:

```bash
$ sudo docker run hello-world
```

More details at <https://docs.docker.com/engine/install/ubuntu/>

### Configuration Tips

**Run Docker CLI as a non-root user**

You may have noticed in the verify step above that we had to invoke the `docker run` command as `root` in order to successfully run a new container. This is required since the Docker daemon always runs as the `root` user and it binds to a Unix socket which is also owned by `root`. This is quite painful when interacting with the CLI however, so there is a workaround using groups:

```bash
# add a new group called 'docker' (it might already exist)
$ sudo groupadd docker

# add the current user to the docker group
$ sudo usermod -aG docker $USER

# after logging out and back in again you should be able to run docker without sudo
$ docker run hello-world
```

Note that this is not the same as running the daemon itself as a non-root user, so all the same security implications still remain when running containers.

**Run Docker on startup**

By default the daemon processes required to interact with Docker are not configured to start when the system boots. To rectify this we can instruct `systemd` to automatically start them for us:

```bash
$ sudo systemctl enable docker.service
$ sudo systemctl enable containerd.service
```

More details at <https://docs.docker.com/engine/install/linux-postinstall/>

### Install Docker Compose

For reasons I don't fully understand `docker-compose` doesn't ship with the core Docker packages and so requires an extra installation step. Fortunately, it's just a single binary so we can just directly download it into a location within the current `PATH` and start using it:

```bash
# download the latest release binary (replace the version from https://github.com/docker/compose/releases)
$ sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# add execute permissions
$ sudo chmod +x /usr/local/bin/docker-compose

# verify everything is working
$ docker-compose --version
Docker Compose version v2.2.3
```

More details at <https://github.com/docker/compose>
