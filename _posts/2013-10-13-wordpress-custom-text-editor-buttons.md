---
layout: post
title: WordPress Custom Text Editor Buttons
tags:
  - button
  - php
  - shortcode
  - wordpress
---
As a follow up to my previous post on adding a new custom inline code shortcode to the WordPress editor, I figured it what also prove helpful to add a custom button to the text editor itself to surround the current text selection inside the inline code shortcode tags.

Again, in WordPress this is pretty easy to do and can be accomplished in a couple lines of code. I found on my searches that there were many tutorials online about adding custom buttons to the WordPress Visual editor, however not so many about custom buttons in the Text editor – which is what I use most of the time when making posts. I did however find a [short article][1] which includes a quick and simple answer. The following code is taken from this post.

To add a new button to the text editor, simply open up `functions.php`, which should be located in your theme folder, and add in the following code (this example adds the inline code tags, but can easily be modified to insert any HTML or shortcode tags that you like). These button in the text editor are known as `Quicktag buttons`. In the code below replace the `your_shortcode` text with your custom shortcode.

{% highlight php startinline=true %}  
add_action('admin_print_footer_scripts','add_button');

function add_button() {
?>  
  
<?php
}
{% endhighlight %}

The parameters to the addButton method are:

  - Button HTML ID (required)
  - Button display, value="" attribute (required)
  - Opening Tag (required)
  - Closing Tag (required)
  - Access key, accesskey="" attribute for the button (optional)
  - Title, title="" attribute (optional)
  - Priority/position on bar, 1-9 = first, 11-19 = second, 21-29 = third, etc. (optional)

The new button should then show up in the WordPress text editor. Clicking on it will add your chosen tags to the editor.

![Wordpress custom button]({{ site.url }}/images/2013/custom_button.jpg){: .center-image width="584" height="37"}

[Source][1]

 [1]: http://witnesswebdesign.com/web-design-blog/web-design-technical-blog/wordpress-add-buttons-to-text-editor-container-quicktags-toolbar/