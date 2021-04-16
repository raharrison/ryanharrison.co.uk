---
layout: post
title: Conversion to Jekyll
tags:
  - jekyll
  - wordpress
---

Over the past few weeks I've been working on a facelift for my blog, which hasn't really seen much of a change since I launched it over 4 years ago. One of the key factors that brought this about was the need to introduce some kind of responsive design, as the last version looked pretty terrible on mobile devices. This is particularly important nowadays as search engines have started to demote any sites which aren't responsive.

Initially I had thought about just updating the Wordpress theme to something a bit more modern and simplistic, but then at the same time my shared hosting plan expired and I moved onto a completely new server. As I was installing things, I came around to porting my blog over. This of course would be pretty easy to do, but I would need to install Wordpress again on my shiny new server - something that suddenly really bothered me. As is common knowledge, Wordpress isn't exactly small and lightweight, and I started to question why I would need this behemoth for my simple blog. I didn't even use most of the features that Wordpress offered previously. I shouldn't have to have a whole mess of PHP and a database just for my blog - so I started looking around for alternatives.

Luckily at this point a colleague at work had just gone though the exact same process. He directed me towards [Jekyll](https://jekyllrb.com/), which he had just converted his old Wordpress blog over to. Jekyll is a template based blogging system that generates static html pages from Markdown files containing your posts. It doesn't have all the bells and whistles of Wordpress, but it's very simple and very fast as it just spits out html pages. Sounded good to me.

Jekyll itself is written in Ruby and was really quick and simple to get started with - basically just install a gem and create a new site using the `jekyll` command. After that you can write your posts in Markdown, which is everywhere these days anyway, and run `jekyll build` to generate your site in plain-old html.

There are some limitations of Jekyll which I may run through in some future post, but for the most part it's lived up to it's name of being very quick and simple. One of the best things about it is how everything is done through partials and layouts with standard HTML and SCSS (Jekyll will do the SCSS build for you). No horrible PHP to trawl through in the old Wordpress themes to just change a small detail. Everything is where it should be and everything is very easy to customise. 

Converting my Wordpress posts over to Markdown was a bit of a pain, but at least it was just a one time thing and now I can forget about it. You also lose some of the things you take for granted in Wordpress like categories and search, but Jekyll is very expandable and has a wide array of plugins that you can make use of. So far I'm really enjoying my experience with Jekyll. No bloated Wordpress dashboard, security holes and mess of PHP themes and plugins - just Markdown and static HTML files. Page load times are also a real dream now by the way.

If you're looking for a simpler alternative to Wordpressm I would recommend at least taking a look at [Jekyll here](https://jekyllrb.com/) and seeing if it fits your needs. A quick warning though - you do have to do some work in order to get things set up how you want them - something that I'm quite enjoying - but maybe not if you want a shiny dashboard and a fully featured blog up and running in 5 minutes.