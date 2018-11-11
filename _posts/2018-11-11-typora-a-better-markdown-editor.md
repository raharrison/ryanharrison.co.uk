---
layout: post
title: Typora - A Better Markdown Editor
tags:
  - typora
  - markdown
  - editor
  - vs code
typora-root-url: ..
---

## VS Code Doesn't Cut It

Since [VS Code](https://code.visualstudio.com/) has come into popularity, I had always used it to write blog posts like this one in markdown. It worked just fine, it's really just a text editor, but there is autocomplete templates and syntax highlighting etc for markdown files.

For small dev markdown files and documentation this is all that's really needed, but for longer pieces of text, I found myself wanting something a little better (more like Word I will admit). Even with all the extensions available for markdown and the live preview version you can get in another pane, there are some big holes in the overall experience when you want to get away from the markup. I can't imagine writing a book etc in VS Code for example, even if markdown is a pretty good option for it.

![VS Code markdown editor](/images/2018/vscode-markdown-editor.png)

The live preview is good, but I never really found myself using it apart from quick checks to see if I hadn't screwed up the markup and that everything looks the way I intended. For the actual writing part however, my attention was forced on the other pane - the markdown itself where, apart from the syntax highlighting, could really be any generic text editor. You have the nice shiny live version sitting right next to your eye, with all the nice CSS applied, but you can't really use it much because the actual editing happens elsewhere - shame really.

The other really big hole in VS Code is the lack of good spell/grammar checking. Yes, there are a few extensions available for this, but they don't hit the mark. One even relies on sending your text to an external web service to report back on spelling errors, seriously. There is one I used that held a local database, but it was far from extensive and you can't right click on a word to change it. In VS Code all 'quick fixes' like this have to go through the lightbulb menu near the gutter - very annoying. I really hope VS Code gets updated to include a good built-in spell/grammar checker.

## [Typora](https://typora.io/)

In [Typora](https://typora.io/), you basically get to edit directly in the VS Code live preview equivalent. The actual underlying markdown is still there, but is kept behind the scenes and is not a distraction in the main editing experience. Things work pretty much how you would expect in most rich text editors, the significant difference being that Typora is converting everything to markdown for you.

![Typora markdown editor](/images/2018/typora-editor.png)

The overall user experience in Typora takes on a minimal and distraction free form. In the left panel, you have your project markdown files, and then you have the great looking preview straight in front of your eye - I think it looks great. The main preview is GitHub like by default, although there are other themes available as well.

You write the actual text the same way as you would do in VS Code, but elements are converted into the final result live as you type. For example, starting off a paragraph with a hash, will look just like you would expect. Give it some content and hit return however, and you have the generated header right there. Same goes for bullet points and images - type the markup and see the results live. It also makes error handling in the markup a lot easier, if the element doesn't show up you must have done something wrong.

Typora is built as an Electron app, which is bit of shame as you'll be running yet more Chrome instances and it is far from conservative in terms of download size and memory usage. But to be honest, for desktop development that seems to be the only really option nowadays and it is far from the worst example of an Electron app I have seen.

Oh, and did I mention that it has built in spell check which works the way you would expect!?

![Typora spell check](/images/2018/typora-spellcheck.png)

[Typora](https://typora.io/) is still in beta and receives constant updates. Plus it's also still free until it has a full stable release. I would definitely recommend for your markdown needs.