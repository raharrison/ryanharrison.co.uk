---
layout: post
title: Ubuntu - Clear Disk Cache
tags:
  - linux
  - ubuntu
  - disk
  - cache
  - memory
---

The Linux kernel often uses available memory for disk caching unless its otherwise needed by a program running on the system. This feature can speed up the system, but the RAM will be marked as used in the top command. It might seem that you are out of memory and need to do something to resolve the problem, when in fact everything is normal and the kernel will simply give programs resources from the disk cache when required. It never takes resources away from programs, just makes use of idle memory sitting in your system. This is such a common question that it even has its own website - <http://www.linuxatemyram.com/>.

If you really want to clear the disk cache and free the memory, run the following command:

`sudo sync && sudo echo 3 | sudo tee /proc/sys/vm/drop_caches`

**Note**: there isn't much point though, as the kernel will just start using the memory again for disk caching straight after you free it.