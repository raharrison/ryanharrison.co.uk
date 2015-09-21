---
layout: post
title: Inline code in WordPress
tags:
  - php
  - shortcode
  - wordpress
---
When posting recently it's become quite annoying that there is no default way of presenting inline code in posts. I've resorted to making the text italic, which does provide a small amount of differentiation, yet does not offer the quality provided in most programming forums where the text inside inline code is in a monospaced font and sometimes has a border.

Luckily though customising WordPress is very easy, and it requires a very small amount of code to achieve the desired effect for inline code.

First of all a custom CSS class needed to be added to the `styles.css` file of the WordPress theme. This is the class I used:

{% highlight css %}  
.inlinecode {  
    padding: 2px;  
    background: #FFF;  
    border: 1px dotted #000;  
    color: #000;  
    font-family: monospace!important;  
}  
{% endhighlight %}

Which simply forces the text into a black monospace font and adds a small border around the outside. The only thing to do now is hook up WordPress to use this new style. WordPress uses shortcodes to accomplish this. Essentially you provide a code inside square brackets and then put the content in between an ending brace. 

For example `migrated over to Jekyll`

For my site I use the `il` shortcode. We then need to tell WordPress what to do when it sees this new shortcode. In this case all that needs to happen is a span tag with the new CSS style is added to encapsulate the inline code. This is done through a simple PHP function:

{% highlight php startinline=true %}  
function inlinecode( $atts, $content = null ) {  
    return '<span class="inlinecode">'.$content.'</span>';
}  
{% endhighlight %}

Finally one more line is needed to hook this new function into wordpress with the chosen shortcode:

{% highlight php %}  
add_shortcode("il", "inlinecode");  
{% endhighlight %}

And that's it. This is one of the benefits of using WordPress – it's so easy to customise and there are a load of guides and tutorials online to help you do it. Here is the resulting inline code (although it has been used throughout this post already):

`Some example inline code (in Jekyll)`

I will also hopefully be gradually adding the use of this new inline code into previous posts in order to improve the overall presentation and readability.