---
layout: post
title: 'Git Bash - Refer to files without absolute paths'
tags:
  - bash
  - git
  - tip
  - trick
---
When using the `Git` version control system with Git Bash it can often become annoying when you have to manually type in the full absolute paths to particular files in your project. For example when trying to add changes to the staging area or checking out a file, in a large project typing out the full file path can be very tedious:

`git add src/uk/co/ryanharrison/snippetmanager/SnippetManager.java`

or

`git checkout src/uk/co/ryanharrison/snippetmanager/Snippet.java`

The problem is especially bad when working on Java projects as the folder structure follows the package names which can often get rather long.

Handily there is an alternative when using `Git Bash` to all this typing - the '\*' or '2-asterisk *globstar*; which searches recursively down your file structure for a file matching the given name.

The above commands can then be replaced with:

`git add **/SnippetManager.java`

which will add any file called `SnippetManager.java` Bash finds below the current working directory to the staging area. The same works with all other commands:

`git checkout **/Snippet.java`

Apparently for this to work in `Bash` you first have to activate `globstar` using this command:

`shopt -s globstar`

however the `Git Bash` in Windows does not seem to support this. The functionality seems to still work though, at least when using it within `Git` commands.