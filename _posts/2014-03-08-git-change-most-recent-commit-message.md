---
layout: post
title: 'Git - Change most recent commit message'
tags:
  - git
  - tip
---
When using any version control system it’s inevitable that you're going to make some kind of mistake when writing out your commit messages. Luckily Git makes it extremely simple to change the message of your most recent commit. Simply use the `amend` command:

`git commit --amend -m "new message"`

For example given this test repository with three previous commits:

![Before ammended message](/images/2014/beforeAmend.png){: .center-image width="570"}

To change the message of the most recent commit - in this case “Third commit”, you can use `git commit --amend -m "This is a modified message"`

This gives the updated log messages:

![After ammended message](/images/2014/afterAmend.png){: .center-image width="570"}
