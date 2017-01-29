---
layout: post
title: Git - Undo Last Commit
tags:
  - git
  - reset
  - commit
---

Sometimes in Git I find myself accidentally redoing my last commit - normally when I press up to get to the last command I ran - expecting it to be something else. This is especially annoying when using `git commit -am` which will include all of the changed files in the new commit.

Fortunately, in Git it's easy to undo your last commit (as long as you haven't pushed it to any remotes yet). Just the one command is needed to revert the last commit to your local repository:

`git reset HEAD~1`

This is demonstrated in the below contrived example where I do an accidental commit, undo the commit using the above command and finally do a quick `git status` to confirm that the file in the commit has been reverted and is outside of the staging area. After this, the commit is no longer included in the `git log` and you would be free to make further changes to it (and others) and do a new commit as normal when ready.

![Git Undo Commit Example](/images/2015/git_undo_commit.png){: .center-image}