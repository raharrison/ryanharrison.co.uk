---
layout: post
title: Apache - Create a Custom 404 Page
tags:
  - jekyll
  - ruby
  - gem
---

Typically, just after I had converted my blog over from Wordpress (you can read more about the conversion [here][1]), the guys at Jekyll decided to have a major release - up now to version 3.0 over the 2.5.3 before. Some of the new features introduced include:

- Incremental regeneration (experimental, enable with --incremental)
- Liquid profiler (add --profile to a build or serve)
- Hook plugin API (no more monkey-patching!)
- Dependencies reduced from 14 to 8, none contain C extensions. We’re hoping to reduce this even more in the future.
- Changed version support: no support for Ruby 1.9.3, added basic JRuby support. Better Windows support.
- Extension-less URLs
- Default highlighter is now Rouge instead of Pygments
- Lots of performance improvements

More information about the release can be found over at it's [news page][2].

Luckily, migrations up to the new version don't seem to be too bad unless you are using a lot of plugins that haven't yet recieved an update. In my case, as of writing, I am just using `jekyll-sitemap` and `jekyll-paginate`. The latter of which is now deprecated which I will come on to.

To upgrade versions I simply ran:

    $ gem update jekyll

You can also omit the gem name which will update all gems you currently have installed. The update seemed to run fine and no errors were output, so I then tried a `jekyll build` (quietly hoping that it hadn't broken too much). As expected I was greeted with this message:

    /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/safe_yaml-1.0.4/lib/safe_yaml/psych_resolver.rb:4:in `<class:PsychResolver>': uninitialized constant Psych::Nodes (NameError)
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/safe_yaml-1.0.4/lib/safe_yaml/psych_resolver.rb:2:in `<module:SafeYAML          >'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/safe_yaml-1.0.4/lib/safe_yaml/psych_resolver.rb:1:in `<top (required)>          '
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/safe_yaml-1.0.4/lib/safe_yaml/load.rb:131:in `<module:SafeYAML>'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/safe_yaml-1.0.4/lib/safe_yaml/load.rb:26:in `<top (required)>'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/jekyll-3.0.0/lib/jekyll.rb:27:in `<top (required)>'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/2.2.0/rubygems/core_ext/kernel_require.rb:69:in `require'
        from /home/ryan/.rbenv/versions/2.2.3/lib/ruby/gems/2.2.0/gems/jekyll-3.0.0/bin/jekyll:6:in `<top (required)>'
        from /home/ryan/.rbenv/versions/2.2.3/bin/jekyll:23:in `load'
        from /home/ryan/.rbenv/versions/2.2.3/bin/jekyll:23:in `<main>'

It wasn't quite the kind of error I was expecting, and after a quick Google search I found a [GitHub issue][3] which has a quick fix of running `gem cleanup`. Must have been some old files laying around messing things up. I ran a Jekyll build again and it was a lot happier this time. I was however faced with a deprecation warning for jekyll-paginate and it seemed as though no posts were being output into my site. This decision seems to have gone under the radar somewhat - the only reference I could find was a short forum [post][4] on their site - and might catch out quite a few users making the jump to 3.0. As stated in the error message, you can continue to use the plugin by simply adding it into the `gems` section of your `config.yml` file.

It seems as though they don't want you to continue using jekyll-paginate, but haven't really supplied us with much of an alternative. The only real option I can find is the [Octopress Paginate][5] plugin which looks slightly more involved than the current offering. I might revisit my own pagination implementation at some point, but at the moment at least, it seems to work well and fits my simple needs.

Other than that, the upgrade to Jekyll 3.0 seems to have been pretty smooth. I particularly like the new incremental build option which can reduce some of the long-ish build times that Jekyll sometimes gives you.

[1]: {% post_url 2015-10-30-conversion-to-jekyll %}
[2]: http://jekyllrb.com/news/2015/10/26/jekyll-3-0-released/
[3]: https://github.com/jekyll/jekyll/issues/3201
[4]: https://talk.jekyllrb.com/t/announcement-retiring-jekyll-paginate/1004
[5]: https://github.com/octopress/paginate


