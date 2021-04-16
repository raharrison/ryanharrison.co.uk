---
layout: post
title: Helpful Extensions for Visual Studio Code
tags:
  - vscode
  - extensions
  - visual studio code
---

### UI

**[Icons](https://marketplace.visualstudio.com/items?itemName=robertohuertasm.vscode-icons) or [Material Icons](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)**

Much needed icons for pretty much every common folder/file combination you can imagine.

**[File Utils](https://marketplace.visualstudio.com/items?itemName=sleistner.vscode-fileutils)**

A convenient way of creating, duplicating, moving, renaming, deleting files and directories. Similar to the Sidebar Enhancement extension in Sublime Text. This again is something I see no reason can't be integrated directly into VSCode.

**[Code Runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner)**

Run code snippets or code file for many languages directly from the editor. Run the selected code snippet/file or provide a custom command as needed. Kind of surprised that VSCode doesn't have this built in.

### Languages/Snippets

**[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)**

Rich support for the Python language (including Python 3.6), including features such as linting, debugging, IntelliSense, code navigation, code formatting, refactoring, unit tests and snippets. Definitely a must have if you do any Python development at all in VSCode.

**[React Code Snippets](https://marketplace.visualstudio.com/items?itemName=xabikos.ReactSnippets)**

This extension contains code snippets for Reactjs and is based on the babel-sublime-snippets package. Pretty much a must have if you any React development and use snippets.

**[ES6 Code Snippets](https://marketplace.visualstudio.com/items?itemName=xabikos.JavaScriptSnippets)**

This extension contains code snippets for JavaScript in ES6 syntax for VS Code editor (supports both JavaScript and TypeScript). Very useful for class definitions, import, exports etc.

### Linting

**[ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)**

Integrates [ESLint](https://eslint.org/) into VS Code. It can be very picky at times and suggests issues that I sometimes don't care about, but you can get it into a decent place after some customisation.

The extension uses the ESLint library installed in the opened workspace folder. If the folder doesn't provide one the extension looks for a global install version (npm install -g eslint for a global install).

**[Markdown Lint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)**

Provides linting for the Markdown language. Includes a library of rules to encourage standards and consistency for Markdown files. It is powered by markdownlint for Node.js which is based on markdownlint for Ruby.

**[Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)**

A basic spell checker that works well with camelCase code. The goal of this spell checker is to help with catching common spelling errors while keeping the number of false positives low.

I only use this for Markdown files as a spell checker and it does an ok job. It's probably the best extension that provides this functionality, but it's still fairly limited. I wish the dev team would integrate this feature natively. You have to click on the quick fix menu (lightbulb icon) to see spelling suggestions as opposed to right clicking on the word as you would think. I guess this is a limitation of the extension framework so there's definitely some room for improvements.

### Misc

**[Auto Close Tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)**

Automatically add HTML/XML close tags. Same as how Visual Studio or Sublime Text do it so very useful if you're used to that behaviour already.

**[Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)**

Extension that autocompletes filenames from the local workspace. E.g typing `./` will suggest all files in the current folder. Very handy.

I'm no doubt missing a bunch of other great extensions, but I try to limit the number to keep things as responsive as possible. Visual Studio code is already a resource hog (pointing at you Electron) without a bunch of background addons making the problem worse.
