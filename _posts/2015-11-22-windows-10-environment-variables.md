---
layout: post
title: New Environment Variable Editor in Windows 10
tags:
  - windows 10
  - environment variables
  - PATH
  - november update
---

The old environment variable editor in Windows has never been the best in terms of user experience. The main editor window was not resizeable and the two listboxes showing user and system environment variables were both small - making it awkward to manage a lot of variables. The problem got even worth when editing the `PATH` environment variable, which can often grow to become a rather large and unwieldy string. Previously, again the variable editor itself was not resizeable, forcing you to scroll through a small textbox to read or make changes to your `PATH`.

![Old Windows Environment Variable Editor](/images/2015/windows_old_path.png){: .center-image}

Thankfully, in the new November Update for Windows 10 (build 10586), which includes enhancements to the Edge browser, Cortana, Start Menu and more, Microsoft have finally updated the Environment Variable manager.

![New Windows Environment Variable Editor](/images/2015/windows_new_path.png){: .center-image width="570"}

The main editor window is now resizeable, making it much easier to navigate through your list of variables. The real magic however happens when editing the `PATH` variable, which now gets it's own dedicated editor. Each path in the variable is now listed separately in a convenient listview, allowing you to quickly add or delete entries or change the order without having to scroll the whole string or worry about any semi-colon separators.

This new enhancement hasn't had much attention in the latest update, but is definitely welcome nonetheless. Hopefully Microsoft will continue to update similar areas in Windows which haven't seen any attention in years.