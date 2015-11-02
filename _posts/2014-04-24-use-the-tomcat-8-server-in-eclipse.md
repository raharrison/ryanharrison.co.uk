---
layout: post
title: Use the Tomcat 8 server in Eclipse
tags:
  - eclipse
  - java
  - server
  - tip
  - tomcat
  - trick
---
The current version of Eclipse (Kepler as of writing) doesn’t natively support version 8 of the Tomcat server. Although support will be added eventually, this is not likely to be until the release of Eclipse Luna in late June 2014. In the meantime, to add support you can download and install the latest version of the WTP (Web Tools Platform) into your current Eclipse environment.

  1. Go to the [WTP Downloads Page][1] and select the link to the latest release (easiest to look at the most recent build date). As of writing the latest version is 3.6.0.
  1. Under the ‘Traditional Zip Files’ section, download the .zip file for Web App Developers.
  1. Extract the archive somewhere and copy all of the files in the ‘features’ and ‘plugins’ directories’ into the corresponding directories in your Eclipse folder (overwriting the existing files).
  1. That’s it. Open up Eclipse and you should see the option for a Tomcat 8 server.

![Tomcat 8 Server in Eclipse]({{ site.url }}/images/2014/tomcat8.jpg){: .center-image width="508"}

 [1]: http://download.eclipse.org/webtools/downloads/