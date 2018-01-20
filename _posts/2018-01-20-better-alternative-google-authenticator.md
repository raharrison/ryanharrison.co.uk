---
layout: post
title: A Better Alternative to Google Authenticator
tags:
  - google
  - authenticator
  - 2fa
  - authy
---

2-Factor authentication is, for very good reasons, becoming increasingly popular as a way to further protect yourself online. The sole use of passwords has long been inadequate for secure authentication and so has been augmented by additional systems. A lot of online services provide SMS messages a a main method for 2-factor authentication, whereby a code will be sent to your phone. This solves part of the problem, but is still susceptible to the inherent insecurity of SMS as a whole, let alone SIM cloning and number spoofing issues.

As a better alternative, many providers have been offering the use of [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) (Time-based One Time Passwords) to generate such codes. The [protocol behind this](https://tools.ietf.org/html/rfc6238) is open, however the most popular implementation is by far the [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en_GB) app, which allows you to scan QR codes to add accounts and will constantly generate one-time-use codes as needed. Its popularity has also meant that most online services directly link to the app and include it in their usage instructions for 2FA auth.

![Google Authenticator app](/images/2018/google-authenticator.jpg)

### The Problem

The Google Authenticator app is all well and good, works well and is very easy to use. It does however open up another problem - what do you do when you lose your phone? It's pretty plausible that for a significant number of users, their phone will either be lost, broken or stolen whilst they are using it to generate 2FA codes. What can you do when you can no longer login to many of your accounts because you aren't able to generate the TOTP?

Many websites will also give you another security code when you enable 2-factor authentication, that you can use in this exact case. But isn't that kind of defeating the whole point? Where are people going to store this code? You're pretty screwed if you lose this recovery code, so you might end up writing it down somewhere insecure or store it online somewhere equally insecure. In my opinion, this is solving a problem by creating a new one.

And that's only taking into account those sites which *do* offer you a recovery code. For the no doubt significant number which do not, you are locked out of your account if you lose your phone. It's going to be in a case by case basis that some providers may let you back in if you contact them, but I'm not sure how they are going to know it's you. For any site that stores sensitive data, I don't see this as an option.

### A Solution

Maybe a lot of users will be put off enabling 2FA for this reason, or more likely a lot of people have never really thought about the potential consequences. Either way, just like your main data, you need to also have a solid backup solution for your 2FA codes.

I mentioned before that the TOTP protocol is not proprietary - so can be implemented by anyone. A think many think that this technology is something Google have magicked up, but in reality there are a number of alternate apps out there.

One such app is called [Authy](https://play.google.com/store/apps/details?id=com.authy.authy&hl=en_GB), which aims to solve the problem mentioned above. In the basic sense, it is very similar to Google Authenticator, whereby you scan the same QR codes and it generates TOTP codes for you. The difference however, is that it provides a method of automatic backup of your accounts. In a similar manner to conventional password managers, such as [LastPass](https://www.lastpass.com/) which you should definitely be using, Authy will encrypt and upload your account strings up to their servers when you add them to the app. This is tied to a password you specify, which they don't ever know - so if you trust password managers then this should be no different.

Your account itself is tied to your phone number, so when you lose you physical device, you can recover all your accounts as long as you move over you number. There are also features which allow sharing of your accounts to your other devices in a similar manner.

![Authy app](/images/2018/authy-app.jpg)

Yes, I know you can just screenshot the QR codes which are generated, or add them to your other devices at the same time, but this is putting all the pressure of the backup on the user. Where are you meant to store the QR codes (how do you backup the backup?), will you encrypt them, how are you going to keep them in sync etc? Again, in this case you are solving a problem by generating another problem - for yourself.

### It's not perfect

The app isn't perfect. For such a simple set of use cases, I have no idea why the app misses on some key features to make it more user friendly (and more approachable over the Google offering).

- You can tie your accounts to a predefined set of providers that the Authy developers maintain (e.g Facebook, Google, Amazon etc). By doing so you can get a nice looking logo and some customised colours for your troubles. This does make the app look a lot nicer, but you rely on the site being in the set that the developers give you. Why the hell can I not provide my own logo? Why the hell can other users not upload their own customisations? Why the hell isn't the existing set bigger? I mean seriously, the look and feel of the app is one of the main selling points given by the devs themselves, this should be so easy to add and contributes to one of your main features. The Google Authenticator app does look bland in comparison - but only when I don't have to use the crappy 'other account' template.
- You can rename your accounts to what you like, but this name doesn't seem to be used when you choose the grid view. Why? Do you think I changed the name just for fun? If I changed it then it's because I want to see it. The changed names are even used in the list view!
- The QR scanner isn't great. I mean, it's definitely functional for sure, but it's nowhere near as good as the one used in the Google Authenticator app. You have to really line up the code in the camera and get it into focus for it to work. In the Google app I can just point it somewhere close and it picks it up immediately.

For sure I am knitpicking with these annoyances, but if you want to draw people away from an app provided by Google, then you're going to have to get it completely right. Hopefully the devs can get on top of this, because for me the main selling point - automated backups - works very well. For most users I would still definitely recommend the Authy app (or others which offer similar features) over the Google Authenticator app.
