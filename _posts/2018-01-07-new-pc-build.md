---
layout: post
title: New PC Build
tags:
  - system
  - build
  - new
---

Late last year I finally got around to buying and building my new computer after many months of research, waiting for releases and price monitoring on [PCPartPicker](https://uk.pcpartpicker.com/list/4cGnbj). It was definitely massively overdue as I was running an AMD Phenom II X4 955 (3.2ghz) on an AM3 board for the preceeding 7 years! It's age was definitely beginning to show, whereby new AAA games would be massively CPU bottlenecked and Battlefield 1 would hardly run at all due to missing some modern instructions. Not to mention how a Youtube video running in the background would intermittently freeze when doing basic work in IntelliJ.

My overall plan and thought process was to go full out on the new parts - which should hopefully last for the next years years easily. I could also make use of one of the best things about building your own desktop computers - reusing old parts to save money. Follows is an explanation of each of the parts I chose and how they have been performing ~1 month after the build:

### CPU - Intel Core i7 8700k @ 4.8ghz

![Intel Core i7 8700k](/images/2018/i7-8700k.png)

Starting with perhaps the main part which ultimately determines the platform you will need - this one changed significantly over the course of last year. With the very successful launch of the Ryzen series of processors by AMD last year, I was initially planning on getting a Ryzen 1700 (8 cores/16 threads) as for raw price/performance you couldn't (and still can't really) do much better. The launch didn't go without a few hiccups, mainly around memory compatibility on a new platform, but it seems to have gotten a lot better. With a very significant ~50%+ improvement to IPC, AMD are finally able to compete with Intel again in the CPU space. The problem however is the clock speeds are still very limited compared to their Intel counterparts. They provide a staggering number of cores for the price point, but the vast majority of users are never going to utilise them all unless you are a hardcore video editor etc. For me personally, having 16 threads isn't all that important when compared to clock speed - which undeniably still causes the biggest performance difference in todays (mainly single threaded) applications. The low powered 14nm process used in the Ryzen processors can barely break 4ghz even with an overclock, although hopefully this will improve with the next generation on the 12nm high powered process.

Regardless of the low clocks, I was still planning on a Ryzen build until Intel obviously felt threatened by AMD and significantly brought forward the release of their 8th generation Coffee Lake CPU's. The rumours were that they were adding cores whilst maintaining their high clock speeds so I decided to wait until they were (paper) released and see how they performed in the reviews. And man am I glad that I did, because the high end parts in particular destroy Ryzen in most workloads. I was always focused only on the 8700k which has 12 threads (more than enough for me) and at stock clocks at 3.7ghz but turbos all the way up to 4.7ghz on one core. According to Reddit, most Ryzen 1700/1700x can overclock to around 3.8ghz max. That ~1ghz+ delta in clock speeds is very substantial and means the 8700k can still keep up in multithreaded workloads even when it lacks 2 full cores.

The release of Coffee Lake wasn't without it's problems either though. Global stock of the 8700k in particular was extremely short, probably because Intel hadn't had enough time to manufacture them after brining forward the release date. As such, the prices were massively inflated initially due to poor supply. After waiting out the initial rush I did manage to get my unit for a reasonable price - even if I did have to order it from the Czech Republic. I did pay more for it, even compared to current pricing, but I still think it was worth it and I was pretty desperate to upgrade last year!

The only thing I can really say about the 8700k is that it's a complete beast. It doesn't take a lot to be a significant improvement over my last system, but the 8700k chews through any workload that I can throw at it without hardly breaking a sweat. Games are completely GPU bottlenecked again (as they should be) and overall performance is excellent. I've currently dialled in a 4.8ghz overclock on my CPU across all cores which is pretty mad really. I think I also got a golden chip as well because a 5ghz overclock was also possible at reasonable voltages/temperatures. I'm still playing around with the overclock though so more to come on that front. If I can get a good 5ghz overclock though, that's a mad amount of performance on a 6 core chip. We will see what happens around the whole Meltdown and Spectre thing, which looks like it might impact performance by a couple percent, but overall I definitely recommend the 8700k. Hopefully AMD can once again catch up though with Pinnacle Ridge and then Zen 2 which should promise much higher clocks. For the meantime though, the performance crown still belongs to Intel.

### CPU Cooler - Noctua NH-D15S

![Noctua NH-D15S](/images/2018/noctua-nh-d15s.jpg)

The 8700k runs hot and that isn't an overstatement. There has been a fair amount of controversy online about the bad TIM (Thermal Interface Material) that Intel uses to combine the CPU die with the heatspreader and there are also mentions of air gaps between the two causing issues. Why they choose not to solder like AMD have with Ryzen I don't know (although I'm sure there are reasons above just cost saving), but the result is that the 8700k runs hot and requires top end cooling to keep under control - especially if you also want to overclock and it's a K-series unlocked chip so you should want to (P.S the i7 8700 is pretty great price/performance if you don't want to overclock).

Most people with the 8700k are using all in one liquid CPU coolers or even custom loops, but using water in a computer still seems strange to me and I don't particularly like the idea of the pump suddenly dying and the increased maintenance required. Luckily however, there are now air coolers available which, although might look worse, offer similar performance to water cooling whilst being cheaper and very quiet.

It didn't take much research to find that Noctua is the clear winner in this department. Their coolers are very well manufactured, perform brilliantly and also use their own fans which are already some of the best in the market. Put all that together and you get something that can easily tame even the 8700k. I eventually chose the NH-D15S dual tower cooler over the very similar NH-D15, which although only includes one fan, still performs very similarly and is slightly less large.

The Noctua coolers aren't cheap by any means, but I think it's definitely worth the price. The packaging is great and their unique mounting system is probably the best out of any manufacturer. At idle, my 8700k barely breaks 30C (it downclocks to 800mhz) and at full load doesn't go much above 80C even when running Prime95 (which is the worst case scenario that won't be met in every day use). The best thing however, is just how quiet it is. At idle I can't really hear it at all and even at full load it remains surprisingly quiet considering how much heat it manages to dissipate. Again, I would definitely recommend these Noctua coolers, just make sure you have enough room in your case to accommodate them.

### Motherboard - Gigabyte Z370 Gaming 5

![Gigabyte Z370 Gaming 5](/images/2018/z370-gaming-5.png)

The Z370 chipset is the flavour of choice for Coffee Lake at the moment pending the lower end chipset releases early this year (although for an 8700k you really want a pretty high end Z370). I ended up with the Gaming 5 as it had some good reviews and has a well rounded feature set for the price point. I also got £20 worth of Steam vouchers through a promotion offered by Gigabyte and am about to get another £20 through another promotion to leave a review. In real terms that makes this board excellent value for money.

It's a very solid board and I have no complaints so far after a month of good use. The VRM's are some of the best at this price range and easily support my 8700k running at 4.8ghz (and event at 5ghz) with good temperatures - something which cannot be said of some other cheaper Z370 motherboards. No issues setting up with an NVME drive either (which can also be placed above the graphics card not only below for better thermals).

Overall connectivity is definitely a strong point as some competitors seem to be lacking in USB ports on the back panel. The inclusion of a USB type C port on the back plus a header is also a nice to have to future-proof yourself. AC WiFi is also definitely a good selling point (and is interestingly missing from the Gaming 7 model) and works as expected for those of us who are unable to have wired connections.

The BIOS is nothing outstanding, but has all of the settings you could pretty much ever need. The XMP profile on my RAM kit was easy to enable and runs at 3200mhz without issue, overclocking is also straightforward with multiple guides available if you need pointers. It's good to see Multi-core enhancement (MCE which auto overclocks k-series processors to max turbo across all cores) turned off by default as it should be - something which cannot be said of the Asus boards. Fan control is very easy and the board has plenty of hybrid fan ports - which is great to see for complex watercooling setups.

Build quality is good and the reinforced PCI-e slots are nice for heavy graphics cards. My favourite feature has to be the ALC1220 audio though which (coming admittedly from poor onboard audio) sounds fantastic in comparison.

I'm not that into the whole RGB lighting game, but this board definitely suits those who are, as there are plenty of lights scattered all over. There are also options for adding additional lighting strips if that's your thing. Everything can be configured both in the BIOS and in the extra software (including turning it all off if needed) but my case doesn't have a window so I don't see it anyway.

Overall at this price point this board is a very solid all rounder and I would recommend to any prospective Coffee Lake buyers. The more expensive Gaming 7 is also an option which includes very beefy VRM's and better onboard audio. For me though these features weren't worth the extra money and the loss of WiFi/Bluetooth.

### Memory - Corsair Vengeance LPX 16gb @ 3200mhz

![Corsair Vengeance LPX 16gb](/images/2018/corsair-lpx.jpg)

RAM prices at the moment are crazy. Monitoring the pricing of this kit via PCPartPicker showed multiple price hikes over the course of last year which now put this kit at over £200. I got it for a bit cheaper than that, but it definitely hurt a bit. Hopefully the situation improves as the new NAND factories open this year (and maybe some investigation into possible price fixing).

The kit itself is pretty standard and nothing really to write home about. It has a plain black look and wide support across many motherboards. I'm not interested in fancy RGB memory or large heatspreaders, so it fits my build well.

16gb is the sweetspot at the moment with 32gb being incredibly expensive and unnecessary for most workloads. Meanwhile, 8gb is starting to become too little in some modern games and applications. I don't expect to need additional memory in the near future. The speed however is something I was willing to pay more for. The difference between stock DDR4 2133mhz and 3200mhz can be quite substantial - even more so in Ryzen due to Infinity Fabric, but also makes a difference in Intel systems. I think 3200mhz is currently the max I would recommend whilst staying reasonably priced and easy to apply as an XMP profile in your motherboard. I had no issues enabling it and run at the rated speed in my system. Moving forward I would definitely stay above 3000mhz for any new builds, and ideally settle at 3200mhz+ to get some future-proofing.

### Graphics Card - MSI GeForce GTX 960 2G

I'm currently reusing the GPU from my old machine and yes, I know this card is massively underpowered considering I am pairing it with an overclocked 8700k. It definitely starts to struggle a bit in some modern games, but I only play at 1080p 60hz anyway so it does the job for the time being. Nevertheless, I can still maintain reasonable frame rates in most games at high settings. The fact that the fans only start spinning when load is applied also means that the build is virtually silent at idle.

I was planning on upgrading the GPU at the same time (to a 1070, maybe a 1080), but I didn't see the point as these cards have already been out for multiple years now and at the rate the industry is moving, will be obsolete when the next generation gets released. On that note, I expect Nvidia will be releasing their new Volta (or Ampere?) cards at some point this year, so I will likely upgrade to one of them. Hopefully crypto mining doesn't inflate the pricing too much. We have already been teased about Volta with the new Titan V, so we should expect a decent performance bump with the new models.

### Storage - Samsung 960 EVO 250gb NVME Drive + Crucial 256gb SATA SSD & 3TB Western Digital HDD

![Samsung 960 EVO 250gb](/images/2018/samsung-960-evo.jpg)

I really wanted to get a good M.2 NVME drive for this new build and I settled on the popular Samsung EVO lineup. They are very expensive so I only got the 250gb model, but this drive just holds the OS and applications so it's more than enough. This drive is blisteringly fast. It took barely 1.5 minutes to install Windows and to be honest pretty much everything loads extremely quickly. Boot times are also pretty crazy even compared to using a SATA based SSD. It's almost definitely overkill for me, but I love it nonetheless and would recommend if you are an speed enthusiast and have the budget.

In addition to the NVME drive I also took my old SATA SSD and spinning hard drive from my old system. The SSD holds games and the HDD is the main data storage drive. This configuration works very well I think. It isn't unreasonably expensive and still gives you a good overall amount of storage and great speeds. The NAND shortage hasn't seemed to effect the 960 EVO drives too much either which is good.

### Case - Fractal Design Define S

![Fractal Design Define S](/images/2018/fractal-design-define-s.jpg)

For some, choosing a case can be one of the most tricky parts. Personally however, I settled on the Define S very early on. In terms of looks it's a very no thrills case (even more so because I chose the windowless model), but the build quality is great, it's easy to build in and best of all it's very cheap for what you get.

The packaging the case came in was good, with very little chance of damage during transit and the included manual is nicely detailed to make building within the case very simple. It's clear that each section has been thought out well and it definitely shows in the generally excellent reviews it gets. There are a number of similar models by Fractal Design as well including the Define C and variants which include windows.

A couple of things to note include the fact that the case does not include space for any 5.25" drives. Initially I thought this to be a downside, but really it doesn't matter a lot to me as, to be honest, I can't remember the last time I used the CD/DVD drive in my old machine. The bonuses of removing the cage mean that the interior of the case is extremely roomly with plenty of space for large watercooling setups and good ventilation for air coolers. There are plenty of good cable management holes which make a tidy system relatively straightforward. The case comes with two 140mm case fans which are extremely quiet and perform well.

Overall, I think this case definitely lives up to the reviews. It would be nice to have an enclosure around the PSU to hide some of the cables (more of an issue for those with the window), but considering I got it for less than £60, I think it's great.

### Power Supply - EVGA SuperNOVA G2 650W 80+ Gold

![EVGA SuperNOVA G2 650W](/images/2018/evga-supernova-g2.jpg)

Nothing too fancy in the power supply department. The EVGA SuperNOVA G2 however is an 80+ gold rated unit with great reviews (especially from [JonnyGuru](http://www.jonnyguru.com/modules.php?name=NDReviews&op=Story&reid=429)) and should be solid for many years to come. Interestingly, there is an updated G3 variant, but it doesn't seem to be particularly popular here in the UK, with many retailers preferring to stock the G2 model. The unit also has a mode whereby the fan will only turn on when needed (similar to most modern GPU's) which makes the system quieter. There are a number of other models for those who need more wattage. I did consider the 750w model, but the 650w is cheaper and should be more than enough for me with a single GPU. Being gold rated also means it should stay efficient even when drawing near the top end of the rated wattage. Remember - never cheap out on your power supply.

### Conclusion

Overall, I'm very happy with the build. All in, the parts above (excluding those parts which I am reusing) came to ~£1100 including delivery costs which, when considering the performance it gives, is good value for money. You can easily spend considerably more on a prebuilt with lower quality components and less overall performance.

It still seems like building your own system would be a hard thing to do, but these days the process is rather simple. The hardest thing is selecting your components, but there are so many guides and sources of help online for this that you should end up with compatible components if you have any sense. The actual process of building has become significantly simpler of the years and these days literally just consists of plugging everything together. With the number of Youtube build guides to follow, again building your system should be open to everyone.

As is (excluding a GPU upgrade) this systems should remain performant for many years to come. Hopefully this time however I will get around to upgrading it before the 7 year mark.

[PCPartPicker for this build](https://uk.pcpartpicker.com/list/4cGnbj)