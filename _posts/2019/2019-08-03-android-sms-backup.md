---

layout: post
title: How to backup and restore SMS Messages in Android
tags:
  - android
  - backup
  - restore
  - sms
  - message
typora-root-url: ..
---

Moving all of your apps and data over to a new device has thankfully got a lot easier these days as everything is now stored in the cloud. But there is a glaring omission in the automated process Google provides on Android devices - restoring your SMS/MMS messages and call logs. Not sure why this is still left out considering pretty much all other messaging apps will automatically migrate your data and preferences seamlessly.

The good news is there is of course "an app for that". A lot of the guides on the web direct you to paid apps, but there are numerous free alternatives on the Play Store.

### [SMS Backup & Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en)

Probably the most popular currently on the store and still actively developed - it's a simple app that backs up and restores your phone's SMS and MMS messages and call logs. I just went through the process of migrating everything over to a new Android phone and this app did the job just fine.

Basically, it will backup all of your messages and call logs into two separate XML files which can later be restored by using the same app on the new device. There are a bunch of options to setup automated backups etc. if that's useful for you.

![Android SMS Backup and Restore App](/images/2019/android-sms-backup.jpg)



Within the app just select where you want the backups to be stored - Google Drive probably being the best choice and hit the 'Back Up' button - that's it for your old device. On your new device I found it easiest to download the two XML files onto your local storage and then point the app to them within the restore tab. After a little processing, everything should look identical between the two devices. The Messages app got a little confused at first trying to process all the new threads, but if you just leave it open for a while it will eventually sort itself out. Job done with little hassle, but Google please add this is in!