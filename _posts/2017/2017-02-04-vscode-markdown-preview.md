---
layout: post
title: Visual Studio Code - Markdown Preview
tags:
  - vscode
  - code
  - visual studio
  - markdown
  - preview
---

[Visual Studio Code ](https://code.visualstudio.com/) has now replaced Sublime Text as my editor of choice due to it's speed and first class support for a number of features that were previously only available through extensions (of varying quality and often outdated). One such example is a live preview of a markdown page - something essential when writing blog posts or pretty much any documentation these days.

Thankfully, Visual Studio Code not only provides native support for Markdown, but also a great live preview of the results as you type - all without any extensions. To enable the live preview within a new editor tab, use the keyboard shortcut `Ctrl+Shift+V` when any Markdown (.md) file is open. This works, but it's much better to have the live preview of the HTML in a split editor so you can see it as you type. VS Code allows you to do this through the shortcut `Ctrl+K V`. Alternatively, for either of these options you can go through the Command Palette `Ctrl+Shift+P` and select either of the 'Markdown Preview' options.

![Jekyll WSL](/images/2017/vscode_markdown_preview.png)

As of [version 1.9](https://code.visualstudio.com/updates/v1_9#_markdown-preview-and-editor-integration), the markdown preview and editor window both scroll in sync. The preview window now loads in local files and you can also now double click on any element within the preview to jump directly to the corresponding line in the editor tab.

Spelling and grammar checking isn't currently available within Visual Studio Code out of the box (hopefully this will also be added in a future update). There is however a great extension available [on the marketplace](https://marketplace.visualstudio.com/items?itemName=seanmcbreen.Spell) which does a great job (when the API it relies on is up).



