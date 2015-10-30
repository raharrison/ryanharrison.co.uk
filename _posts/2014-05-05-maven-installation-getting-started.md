---
title: 'Maven – Installation and Getting Started'
layout: post
tags:
  - java
  - maven
---
### What is Maven?

From their [page][1]:

  > "a tool that can now be used for building and managing any Java-based project. We hope that we have created something that will make the day-to-day work of Java developers easier and generally help with the comprehension of any Java-based project."

Essentially Maven makes it much easier for developers to manage their Java projects. Where it really shines is with the build process (particularly when handling dependencies, but we'll get onto that in a later tutorial) –

  > "Maven allows a project to build using its project object model (POM) and a set of plugins that are shared by all projects using Maven, providing a uniform build system. Once you familiarize yourself with how one Maven project builds you automatically know how all Maven projects build saving you immense amounts of time when trying to navigate many projects."

Sounds pretty cool huh? In addition, it turns out that Maven is really easy to install and get started with using on all your Java projects.

### Installation –

First step is to download the current Maven build from their website [http://maven.apache.org/download.html][2]. Pick whichever archive format you prefer and download and extract the most recent release to somewhere on your machine.

#### Windows –

Now if you are on Windows, all we have to do is set up some environment variables and we are good to go.

Go to your `System properties page` -> `Advanced system settings` -> `Advanced` -> `Environment Variables`

Add the following variables:

  * JAVA_HOME -> Point to your Java installation directory e.g `C:\Program Files\Java\jdk1.7.0_51`
    
  * MAVEN_HOME -> Point to your extracted Maven directory e.g `C:\Users\Name\Java\apache-maven-3.2.1`

  * PATH -> Locate the existing `PATH` variable and `Edit` it. At the end add the this: `;%MAVEN_HOME%\bin;` (make sure all the entries are separated by one semi-colon).

That's all you need to do. You should now be ready to get started with using Maven.

#### Unix –

Run the command `sudo apt-get install maven` and you should be good to go straight away! Skip to the verify your installation stage to make sure you are good to go.

### Verifying your installation –

Once you have followed the installation steps depending on on your operating system, open up a command line/terminal window and enter the following command to make sure everything is working correctly:

    mvn -version

You should see some output that looks something like this:

    > C:\>mvn -version  
    > Apache Maven 3.2.1 (ea8b2b07643dbb1b84b6d16e1f08391b666bc1e9; 2014-02-14T17:37:5  
    > 2+00:00)  
    > Maven home: C:\Users\Name\Java\apache-maven-3.2.1\bin\..  
    > Java version: 1.7.0_51, vendor: Oracle Corporation  
    > Java home: C:\Program Files\Java\jdk1.7.0_51\jre  
    > Default locale: en_GB, platform encoding: Cp1252  
    > OS name: "windows 8", version: "6.2", arch: "amd64", family: "windows"

If not then you may need to try the above steps again or search online for solutions.

If on the other hand you did get output that looked like the above, then that's it. You are ready to use Maven in your projects!

[1]: http://maven.apache.org/what-is-maven.html
[2]: http://maven.apache.org/download.html
[3]: http://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html

### Creating a Project

To create a project with Maven, you make use of its `archetype` mechanism. This is basically a large collection of pre-made project templates that you can base your project from. There are a ton of different types of `archetypes` available so you there should already be one that matches your requirements. In this tutorial we will be using a `quickstart archetype` which is one of the simpler models of a basic Java application.

To construct this project first open up a terminal or command prompt window and navigate to the location on your machine where you want your project to be stored. In this example I am using a 'Projects' folder sitting on the root C: drive directory.

<!--more-->

Once there issue the command:

    mvn archetype:generate

This will first of all download a few things and then display a massive list of available `archetypes` you can base your project from.

    > …. omitted  
    > 947: remote -> org.tinygroup:buproject (-)  
    > 948: remote -> org.tinygroup:flowcomponent (-)  
    > 949: remote -> org.tinygroup:plugincomponent (-)  
    > 950: remote -> org.tinygroup:uicomponent-archetype (-)  
    > 951: remote -> org.tinygroup:webappproject (-)  
    > 952: remote -> org.trailsframework:trails-archetype (-)  
    > 953: remote -> org.trailsframework:trails-secure-archetype (-)  
    > 954: remote -> org.tynamo:tynamo-archetype (-)  
    > 955: remote -> org.uberfire:uberfire-component-archetype (UberFire Component Archetype)  
    > 956: remote -> org.uberfire:uberfire-project-archetype (UberFire Project Archetype)  
    > 957: remote -> org.wicketstuff.scala:wicket-scala-archetype (-)  
    > 958: remote -> org.wicketstuff.scala:wicketstuff-scala-archetype (Basic setup fo  
    > r a project that combines Scala and Wicket, depending on the Wicket-Scala project. Includes an example Spectest.)  
    > 959: remote -> org.wikbook:wikbook.archetype (-)  
    > 960: remote -> org.xaloon.archetype:xaloon-archetype-wicket-jpa-glassfish (-)  
    > 961: remote -> org.xaloon.archetype:xaloon-archetype-wicket-jpa-spring (-)  
    > 962: remote -> org.xwiki.commons:xwiki-commons-component-archetype (Make it easy  
    > to create a maven project for creating XWiki Components.)  
    > 963: remote -> org.xwiki.rendering:xwiki-rendering-archetype-macro (Make it easy  
    > to create a maven project for creating XWiki Rendering Macros.)  
    > 964: remote -> org.zkoss:zk-archetype-component (An archetype that generates a s  
    > tarter ZK component project)  
    > 965: remote -> org.zkoss:zk-archetype-extension (An archetype that generates a s  
    > tarter ZK extension project)  
    > 966: remote -> org.zkoss:zk-archetype-theme (An archetype that generates a start  
    > er ZK theme project)  
    > …. omitted  
    > Choose a number or apply filter (format: [groupId:]artifactId, case sensitive co  
    > ntains): 383:

As you can see there are quite a few. We are prompted by Maven to input the index of the `archetype` we wish to use. In this tutorial we are using a simple quickstart `archetype` with the index `383`. Handily Maven enters this by default so we can just hit return at this point.

We are then prompted by Maven to choose which version of the `archetype` to use:

    > Choose org.apache.maven.archetypes:maven-archetype-quickstart version:  
    > 1: 1.0-alpha-1  
    > 2: 1.0-alpha-2  
    > 3: 1.0-alpha-3  
    > 4: 1.0-alpha-4  
    > 5: 1.0  
    > 6: 1.1  
    > Choose a number: 6:

In this case we want to use the latest version (1.1 in this case) so we choose option 6. Again Maven fills this in by default so we can hit return again.

We are then prompted by Maven to supply a `'groupId'`. From the docs:

  > groupId – This element indicates the unique identifier of the organization or group that created the project. The groupId is one of the key identifiers of a project and is typically based on the fully qualified domain name of your organization. For example org.apache.maven.plugins is the designated groupId for all Maven plug-ins.

The `groupId` is essentially the same thing as what you would normally use as a root package for your application. In this example we will use `net.ryanharrison.app`.

We are then asked to give an `artifactId`. Again from the docs:

  > artifactId – This element indicates the unique base name of the primary artifact being generated by this project. The primary artifact for a project is typically a JAR file. Secondary artifacts like source bundles also use the artifactId as part of their final name. A typical artifact produced by Maven would have the form <artifactId>-<version>.<extension> (for example, myapp-1.0.jar).

This property is essentially just the name of your project. Simple enough. In this example I will use `MavenTutorial`.

We are then prompted to give a version. Maven includes some good version management tools, but we won't cover that in this tutorial. The general convention is to use `SNAPSHOT` when the project is still in development, and to then switch to a solid version number when deployed. For now we will use the default value of `1.0-SNAPSHOT`. This can of course be changed later on in the development cycle.

Finally Maven wants a package name from us. This should be pretty familiar to any Java programmer. By default Maven gives us the `groupId` value we previously entered (net.ryanharrison.app) which is fine for us.

Maven then gives as a summary of the project properties we just entered:

    > Define value for property 'groupId': : net.ryanharrison.app  
    > Define value for property 'artifactId': : MavenTutorial  
    > Define value for property 'version': 1.0-SNAPSHOT: :  
    > Define value for property 'package': net.ryanharrison.app: :  
    > Confirm properties configuration:  
    > groupId: net.ryanharrison.app  
    > artifactId: MavenTutorial  
    > version: 1.0-SNAPSHOT  
    > package: net.ryanharrison.app  
    > Y: :

Type `Y` to accept these properties and get Maven to create the project. After a short while you should see a `BUILD SUCCESS` message if the project was created successfully.

### Analysing what we just created

Once created you should notice that a new folder has been created at your location with the same name as the `artifactId` you supplied earlier. `cd` into that directory and have a look around. It should have this rough structure which follows Maven's [Standard Directory Layout][3]:

  MavenTutorial  
    |-src  
    |—main  
    |—–java  
    |——-net  
    |———ryanharrison  
    |———–app  
    |————-App.java  
    |—test  
    |—–java  
    |——-net  
    |———ryanharrison  
    |———–app  
    |————-AppTest.java  
    |-pom.xml

Essentially there are two parallel source trees that have been created:

  * src/main/java -> houses your application's source files  
  * src/test/java -> houses your test source files

Maven has also created the `pom.xml` (Project Object Model) file. This is an essential file in Maven and basically contains every important piece of information about your project. It is a single configuration file that Maven uses to build your application. This is the core component of any Maven project and is essential to come familiar with in order to make the most out of Maven.

### pom.xml (Project Object Model)

Take a look inside the `pom.xml` file that Maven created for us:

{% highlight xml %}
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
  <modelVersion>4.0.0</modelVersion>

  <groupId>net.ryanharrison.app</groupId>  
  <artifactId>MavenTutorial</artifactId>  
  <version>1.0-SNAPSHOT</version>  
  <packaging>jar</packaging>

  <name>MavenTutorial</name>  
  <url>http://maven.apache.org</url>

  <properties>  
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>  
  </properties>

  <dependencies>  
    <dependency>  
      <groupId>junit</groupId>  
      <artifactId>junit</artifactId>  
      <version>3.8.1</version>  
      <scope>test</scope>  
    </dependency>  
  </dependencies>  
</project>
{% endhighlight %}

Most of this should be pretty self-explanatory. At the root we have the `project` node which will be the base of all `pom.xml` files. Under that we have the `version` of the object model Maven is using (shouldn't need to change this). Then we have the `groupId`, `artifactId` and `version` just as we entered them when we created the project in the command line.

Next however we have the `packaging` type. We will cover this more in the next tutorial, but it basically tells Maven what type of file to create when we 'package' the project. This is a `.jar` file for this simple Java application, but may be a `.war` file for example in web applications.

Following the packaging tag we have the `name` and `url` of the project. The name is the display name used for the project and the url is indicates where the website of the project can be found. Both of which are used when Maven generates documentation for us (we will again see this in action in a later tutorial).

We then have a property stating the encoding of a source files, and finally a set of `dependencies` for our project. This is where Maven really shines. Instead of having to manually download an external library (and all of its dependencies!), we can simply add it as a `dependency` in the `pom.xml` file, and Maven will automatically download that library and all needed dependencies it needs to operate. Not only that but it will also configure the build path to add these libraries which cuts out a lot of potential hassle for us developers.

We will cover dependencies more in the next tutorial, but for now just know that at the moment we have one dependency (`jUnit` that gets used in the test source tree).

### Compiling our Project

Now, at this point to compile our application we could use the `javac` command and play around with the build path to handle `jUnit` (and any other dependencies we may have). But we don't want to do that now do we?

Handily Maven will take care of all that for us, after all it is a build tool. To compile our project simply make sure you are in the main project directory (the one with `pom.xml`) in it, and issue the command:

    mvn compile

If this is the first time you run the command, then this may take a while to complete. Maven is essentially downloading all of the dependencies and plugins it needs to compile your project (there are quite a few to get through). The good news is, once you've downloaded them once, they will remain in your local repository, so the command will take much less time in the future.

Once it's finished you should see output like:

    > [INFO] Compiling 1 source file to C:\Projects\MavenTutorial\target\classes  
    > [INFO] ————————————————————————  
    > [INFO] BUILD SUCCESS  
    > [INFO] ————————————————————————  
    > [INFO] Total time: 6.981 s  
    > [INFO] Finished at: 2014-04-30T16:25:50+00:00  
    > [INFO] Final Memory: 10M/125M  
    > [INFO] ————————————————————————

A new folder `'target'` has also been created which houses all of the .class files for your project. To make sure it works we will run the project (this `archetype` gives us a 'Hello World' example to execute):

    > C:\Projects\MavenTutorial>cd target/classes
    > 
    > C:\Projects\MavenTutorial\target\classes>java net.ryanharrison.app.App  
    > Hello World!

If you get this output then everything is working correctly!