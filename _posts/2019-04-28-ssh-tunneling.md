---
layout: post
title: SSH Tunneling
tags:
  - ssh
  - tunnel
  - tunneling
  - port forwarding
  - server
typora-root-url: ..
---

SSH Tunneling, is the ability to use `ssh` to create a bi-directional encrypted network connections between machines over which data can be exchanged, typically TCP/IP. This allows us to easily & securely make services available between machines with minimal effort, while at the same time leveraging `ssh` for user authentication (public-key) and encryption with little overhead.

### Local Port Forwarding

```
$ ssh -nNT -L 8000:localhost:3306 user@server.com
```

The above command sets up an `ssh` tunnel between your machine and the server and forwards all traffic from `localhost:3306` (on the remote server) to `localhost:8000` (on your local machine).

Since port `3306` is the default for MySQL, you could now access a database running on your remote machine through `localhost:8000` (as if it was setup and running locally). This is useful as you don't have to configure the remote server to allow extra ports through the firewall and handle the security implications of locking all your services down just to access a dev database for example. In this case, the MySQL instance is still not visible to the outside world (just how we like it).

In the above command, the `-nNT` options prevent a shell from being created, so we just get the port forwarding behaviour (not strictly needed but you probably don't also want a new `tty` session).

### Remote Port Forwarding

```
$ ssh -nNT -R 4000:localhost:3000 user@server.com
```

The  above command sets up an `ssh` tunnel between your machine and the  server, and forwards all traffic from `localhost:3000` (on your local machine)  to `localhost:4000` (on the remote server).

You could then access a service running locally on port `3000` on the remote server through port `4000` (again as if it was running locally on the remote server). This is useful because it allows you to expose a  locally running service through your server to others on the internet  without having to deploy it / setup on the server. Note: to get this working you also need to set `GatewayPorts yes` in the `/etc/ssh/sshd_config` file as `ssh` doesn't allow remote hosts to forward ports by default.

### SOCKS Proxy

```
$ ssh -D 5000 -nNT user@server.com
```

The above command sets up a `SOCKS` proxy server supporting `SOCKS4` and `SOCKS5` protocols leveraging dynamic application-level port forwarding through the `ssh` tunnel. You could now configure your network proxy (within the browser or the OS) to `localhost:5000` as the `SOCKS` proxy and then when you browse, all the traffic is proxied through the `ssh` tunnel using your remote server.

- It protects against eavesdropping (perhaps in an airport or coffee shop) since all the traffic is encrypted (even if you are accessing `HTTP` pages).
- As all web traffic goes through the `SOCKS` proxy, you will be able to access web sites that your ISP/firewall may have blocked.
- Potentially helps protect your privacy since the web services you access will see requests coming from the remote server and not from your local machine. This could prevent some (IP based) identity/location tracking for example.

### Advanced Use Cases

The  above-mentioned use cases are the most commonly used, however, they can  be modified slightly and used in interesting ways to be able to establish the `ssh` tunnel not only between your local machine and your server, but also additional machines, either internal to your network or internal to your servers network:

```
$ ssh -nNT -R 0.0.0.0:4000:192.168.1.101:631 user@server.com
```

- Instead  of using the default bind address, I explicitly use `0.0.0.0`. This implies that the service available on the remote server on port `4000` (forwarded from local port `631`), will be accessible internally to the remote server network across all network interfaces, including bridge networks & virtual networks such as those used by container environments like Docker.
- Instead  of using `localhost` as the bind address for the local machine, I have explicitly used the `192.168.1.101` IP Address, which can be the IP Address of an internal machine (other than the machine you’re using this command on), such as a network printer. This allows you to be able to  expose and use my internal network printer directly from the remote server, without any additional changes from within my internal network either on  the router or the network printer.

This technique can also be used while doing a local port forwarding or for  setting up the socks proxy server in a similar manner.