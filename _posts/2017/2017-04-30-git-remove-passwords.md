---
layout: post
title: Git - Remove Passwords or Sensitive Data
tags:
    - git
    - bfg
    - password
    - sensitive
---

If you have accidentally committed a password or other sensitive data to your Git repository, make sure to remove it before pushing it to GitHub or making it open source. When working with databases or other external systems, it's incredibly easy to put a password into a configuration file, commit it and forget about it - only for it to be subsequently completely visible to everyone on the internet thereafter.

Thankfully, there are a few ways to remove private data from your Git repos. The most bare-metal approach would be to use the [git-filter-branch](https://git-scm.com/docs/git-filter-branch) command which is able to rewrite your Git history whilst applying filters. It's a very powerful command and therefore has many configuration options and is quite difficult to use directly.

A much easier solution is to use the [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/). This is a separate tool which offers a much faster and simpler method of cleaning your repo of private data or very large files.

To make use of this tool, first make sure you have Java installed and available on the `PATH` - follow the steps [in this post][1] to do so. Then download the `.jar` file from [their site](C:\Users\Ryan\Documents\Projects\blog_posts\2011-06-29-compile-from-the-command-line.md).

### Find sensitive data within your repository

If you have a password or other credential that you think you may have accidentally committed into your repo, run the following command to find out. This uses the 'pickaxe' option of [git log](https://git-scm.com/docs/git-log) to find revisions in which the number of occurences of a search time has changed.

`$ git log -S<password>`

From the docs:

-   -S Look for differences that change the number of occurrences of the specified string (i.e. addition/deletion) in a file.
-   -G: looks for differences whose added or removed line matches the given regexp, as opposed to -S, which "looks for differences that introduce or remove an instance of string".
-   --all: searches over all branches and tags

### Remove passwords and private data using BFG

1. Create a file called `passwords.txt`, in which place all your passwords or sensitive data.
1. Run the command `$ java -jar bfg.jar --replace-text passwords.txt <your-repo>`

More documentation and examples, along with how to remove large files from your repo can found on the [BFG project page](https://rtyley.github.io/bfg-repo-cleaner/).

**Note: This will completely rewrite your Git history, the hashes or all commits will be re-generated.**

[1]: {% post_url 2011/2011-06-29-compile-from-the-command-line %}
