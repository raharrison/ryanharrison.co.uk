---
layout: post
title: Sending Email with Python 3
tags:
  - python
  - email
  - send
---

A common task in any popular programming language is the ability to send emails to your users, be it as a password reset or as a contact page submission on a blog just like this one.

The below snippet can be used to accomplish this, just change the variables depending on your use case. It assumes that you have a local SMTP server running on the machine you are running the script on (`Postfix` for example), however you can also login to another service if you want to send via Gmail or Outlook etc.

{% highlight python %}  
sender = "sender@domain.co.uk"
sender_name = "Sender Name
receiver = "receiver@example.co.uk"
receiver_name = "Receiver Name"
subject = "This is the subject line"

message_str = "This is the body of the message"

mime = """From: {0} <{1}>
To: {2} <{3}>
MIME-Version: 1.0
Content-type: text/plain
Subject: {4}
{5}
""".format(sender_name, sender, receiver_name, receiver, subject, message_str)

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receiver, mime)
    return "Successfully sent email"
except smtplib.SMTPException:
    return "Error: unable to send email"
{% endhighlight %}

You can also add additional properties to the MIME message for extra functionality:

  * `Reply-To: Name <address>` to specify who the receiver should send their replies to
  * Change the `Content-type` to `text/html` if you want to use HTML within your message body for styling
