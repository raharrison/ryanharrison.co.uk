---
layout: post
title: My Experiences with Hostgator
tags:
  - hostgator
  - hosting
  - server
---

When I first launched my blog way back [in 2011][1] I didn't really know a whole lot about web hosting at all and just wanted to get something tangible up and running as quick as possible. Therefore of course I had no idea what constituted a half decent web hosting company. At the time I think I was just following some online tutorial which ran through the process of setting up and hosting your own site. I registered my domain with GoDaddy as recommended (and still do with no issues) and then had to move on to actually hosting my site. The tutorial recommended Hostgator and that seemed fine to me. They had pretty good reviews and the prices for shared hosting were good for a minimal setup like mine.

I got myself their most basic shared web hosting plan which consists of a single domain and unlimited (yeah, until you start using too much of course) bandwidth/email/databases. To be honest even by today's standards that's pretty good going. At the time I payed $5.95/mo for 2 years of hosting which included a 20% promotion (which I later learnt is pretty much a constant thing).

![Hostgator Logo](/images/2015/hostgator.jpg){: .center-image width="300"}

They provided a good service to me for the duration of my stay. I was able to host my Wordpress blog with no issues and could easily play around with FTP and a few MySql databases on the side. Most importantly actually was the ease of getting hold of personalised email with my domain - something that it turns out is quite messy without cPanel as I found out recently.

Throughout my use of Hostgator speed wasn't an issue - although granted I wasn't using it for any real strenuous activity. I also didn't get notified of any usage issues as a lot of people do with shared hosting (again this was really only Wordpress so that's to be as expected). cPanel is ridiculously easy to use as well so no issues there setting things up.

Then my initial two year contract expired and I realised why the initial price was so cheap. The renewal invoice was sent to me and the price had increased by a third (about $70 for the two years). Not only had the base price increased slightly, but you don't get that nice 20% discount that you take for granted when you initially sign on. There are never any renewal discounts that I can make out. Even if you have marketing emails from them, their offers are always for new accounts - never for existing customers which is a real shame. I can of course understand why they do that in the business sense, but still I would expect some kind of special offer on renewals once in a blue moon. With hindsight, I should have threatened to leave which is when they start trying to discount things, but at the time I really didn't want the hassle of moving everything over to a new host and was happy with the service I was getting. Another two years with Hostgator it was.

[1]: {% post_url 2011-06-08-hello-world %}

<!--more-->

I had the hosting throughout the bulk of University which was fine at first, but as your knowledge increases (particularly after placement), you start wanting to try out different things. It became clear that shared hosting simply wouldn't cut it anymore. I needed root ssh access and some more powerful hardware to play around with.

I planned to switch to a VPS when the existing plan ended, but it crept up on me and I was blissfully unaware when it eneded and I was completely unprepared. So I switched over from a two year plan to rolling monthly to get me through the search for a new host. I would have just ended immediately and have the site down for a few months, but I still needed access to my domain email. That's where hosting companies really sting you - $9/mo when you are on a rolling monthly plan vs. one/two years. Again I can see why they do this, but still that's pretty unbelievable pricing for shared hosting.

And so started the search for a new VPS plan. I first started at Hostgator, but man are those expensive. The cheapest is $12/mo and you get 0.5 cores (seriously), 512MB of memory and 25GB's of disk space. To get anything half decent you have to fork out $50/mo - and that's just 2 cores, 2GB's of memory and 120GB's of disk space, so hardly ground-breaking. It should be said however that this is more managed hosting with 24/7 support, which of course is included in the price. For me however, I didn't want to fork out for support I probably wouldn't ever use.

I will write another post on the hosting I eventually settled on, but it did however unfortunately mean an end to my days with Hostgator. The process of cancelling your account is pretty easy - just have to create a ticket and state why you are leaving. I told them how I was looking to upgrade to a VPS and that I thought they were too expensive compared to similar solutions on the market. I waited a couple days for them to get back to me, probably give me some kind of discount on their VPS's to try and keep me as a customer and that would be that. Strangely enough I was offered the same original 20% discount on shared hosting packages - exactly what I was trying to get away from. I think their custom retention department needs a little work. After I obviously refused their offer, it took another week and a half for my plan to actually get cancelled. Not a massive problem for me as I wasn't paying for anything at this point, but getting to the point where I would have to start following up on it myself.

To be clear, this isn't in any way a bash on Hostgator. I had no problems with them through 4 years of hosting and I still think the pricing for shared hosting is reasonable (as long as you pick at least the 2 year option, which of course might not be for some people). I'm not sure what other companies offer these days in terms of shared hosting but I doubt you could do much better. It's a lot more work now with no cPanel, but still a really useful experience in setting up and securing a Unix environment from scratch. I would recommend it to any developer and you don't even need a fully fledged VPS or dedicated server - you can just spin up an environment at [DigitalOcean](https://www.digitalocean.com/) for an hour or two and then pull it down as needed.



