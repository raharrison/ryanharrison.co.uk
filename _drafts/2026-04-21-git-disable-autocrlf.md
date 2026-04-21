---
layout: post
title: Git - Disable autocrlf
tags:
  - git
  - windows
  - line endings
  - crlf
  - lf
  - wsl
  - config
---

If you're on Windows, Git has almost certainly been silently messing with your line endings since the day you installed it. 

**TLDR:** The fix is this one command:

```bash
git config --global core.autocrlf false
```

It's on by default. It's a terrible default. Mainly due to historical reasons that no longer exist.

<!--more-->

## What `core.autocrlf` Does

In short, Windows has historically used `CRLF` (`\r\n`) as its line ending character, while Linux and macOS use plain `LF` (`\n`). 
At some point, someone decided that Git on Windows should helpfully bridge this gap automatically. 
So by default, `core.autocrlf` is set to `true` on Windows, which means:

- On **checkout** - Git converts `LF` line endings in the repository to `CRLF` in your working directory
- On **commit** - Git converts `CRLF` back to `LF` before storing the file

In theory, this means your files always have Windows-style line endings locally, and the repository stays clean with Unix-style endings. 
Sounds reasonable enough. In practice though, it can be really quite annoying.

## Why It's a Bad Default

### WSL Makes It Worse

If you use [WSL](https://learn.microsoft.com/en-us/windows/wsl/about) (and you definitely should if you use Windows), this setting can cause issues. 
Your Linux environment expects `LF` line endings. 
Your Windows Git has helpfully checked out everything with `CRLF`. 
The result is that your scripts and config files have a stray `\r` at the end of every line, which causes failures. 
WSL and Git will also start warning you about line ending inconsistencies whenever you touch a repo:

```
warning: LF will be replaced by CRLF in some-file.sh.
The file will have its original line endings in your working directory
```

You've probably seen this warning before, or rather enough times that you have started ignoring it.

### Modern Editors Handle LF Just Fine

The argument for `CRLF` on Windows was that Notepad couldn't handle `LF`-only files - which was true in 2003. 
Notepad has supported `LF` line endings since Windows 10 (2018).
Every other editor - VS Code, Sublime, Vim, IntelliJ, Notepad++ etc - has handled it just fine for even longer. 
There is no editor you are realistically using today that will break on `LF` line endings.

### The Conversion Is Lossy in Practice

Even when it works as intended, the automatic conversion can cause issues. Binary files can get corrupted if Git misidentifies them as text. 
Files can show up as changed in `git diff` or `git status` purely because of line ending differences, with no actual content change. 

If you work in a team where some people have `autocrlf true` and others have it `false`, you'll end up with commits that are just line ending changes.

## Disable it

Set it to `false` like it should be by default:

```bash
git config --global core.autocrlf false
```

From then on, Git leaves your line endings exactly as they are - no silent conversions on checkout, no conversions on commit. 
If you want to be explicit about line endings across a team, a [`.gitattributes`](https://git-scm.com/docs/gitattributes) file in the repository is a much better approach since it applies the same rules for everyone regardless of their local config.

Use `LF` everywhere, configure your editor to save with `LF` by default. Don't think about it again (until your move machine).

## Further Reading

- [Git Documentation - `core.autocrlf`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreautocrlf)
- [`.gitattributes` reference](https://git-scm.com/docs/gitattributes)
