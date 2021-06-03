---
layout: post
title: WSL2 - Better Managing System Resources
tags:
    - wsl2
    - memory
    - docker
    - disk
    - reclaim
typora-root-url: ../..
---

WSL2 is great, but unfortunately after moderate usage it’s easy to get in a situation where it will eat up all of your disk space and use up to 50% of your total system memory. We’ll go over how to address these issues below.

## Setting a WSL2 Memory Limit

By default the WSL2 will consume up to 50% of your total system memory (or 8GB whichever is lower). You can configure an upper limit for the WSL2 VM by creating a `.wslconfig` file in your home directory (`C:\Users\<user>\.wslconfig`).

```plain
[wsl2]
memory=6GB
swap=0
```

Note that in this case the Linux VM will consume the entire amount regardless of actual usage by your apps, but it will at least prevent it growing beyond this limit.

## Free Unused Memory

As described in [this post]({{ site.baseurl }}{% post_url 2016/2016-05-08-ubuntu-clear-disk-cache %}) the Linux kernel often uses available memory for it's page cache unless its otherwise needed by a program running on the system. This is good for performance, but for WSL2 it can often mean the VM uses a lot more memory than it really needs (especially for file-intensive operations).

Whilst the WSL2 VM is running can you also run a simple command to drop the memory caches and free up some memory:

`sudo sh -c \"echo 3 >'/proc/sys/vm/drop_caches' && swapoff -a && swapon -a && printf '\n%s\n' 'Ram-cache and Swap Cleared'\"`

## Compact the WSL2 Virtual Disk

If you copy some large files into WSL2 and then delete them, they will disappear from the filesystem but the underlying virtual disk may have still grown in size and the extra space will not be re-used. We can run a command to optimize/vacuum the virtual disk file to reclaim some space.

```powershell
## Must be run in PowerShell as Administrator user
# Distro Examples:
#   CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc
#   CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc

cd C:\Users\user\AppData\Local\Packages<Replace-Eg-CanonicalGroupLimited\LocalState
wsl --shutdown
optimize-vhd -Path .\ext4.vhdx -Mode full
```

<https://github.com/microsoft/WSL/issues/4699>

## Docker

If you run a lot of Docker containers within WSL2m a lot of disk space may be used unnesessarily by old images. We can run the standard Docker command to remove any old/dangling images, networks and volumes:

`docker system prune`

Along the same lines as above as we can also compact the VM file that Docker Desktop creates to get some disk space back. You’ll want to open PowerShell as an admin and then run these commands:

```powershell
# Close all WSL terminals and run this to fully shut down WSL.
wsl.exe --shutdown

# Replace <user> with your Windows user name. This is where Docker stores its VM file.
cd C:\Users\user\AppData\Local\Docker\wsl\data

# Compact the Docker Desktop WSL VM file
optimize-vhd -Path .\ext4.vhdx -Mode full
```

The above `optimize-vhd` command will only work on Windows 10 Pro. For folks on the Home edition there are some scripts with workarounds:

-   <https://github.com/mikemaccana/compact-wsl2-disk>
