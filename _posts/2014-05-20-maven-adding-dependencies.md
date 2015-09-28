---
layout: post
title: 'Maven – Adding Dependencies'
tags:
  - java
  - maven
---
### Prerequisites –

It is assumed that before starting this tutorial, you have read and understand the first part of this series which includes an overview of Maven and [creating a simple Maven project][1].

### What are dependencies?

In this context, dependencies are any modules of code that your application requires in order to function properly. In this case, this mainly consists of large public libraries that are often needed for Java programs. Such examples include logging frameworks such as `Log4J`, unit testing frameworks such as `JUnit`, or a whole multitude of other frameworks and libraries such as `Spring` for dependency injection, `Hibernate` for object relational mapping and `Struts` for MVC web applications. In this example we will be using `Guava` which is a commonly used collections library from Google.

The dependency capabilities of Maven don't just end with managing dependencies for a single a project however. Maven really starts to excel when you start getting into dealing with multi-module projects and applications that consist of maybe tens or even hundreds of modules – each of which may depend on a selection of the others.

### Why do we need Maven for this?

At this point you may be asking why we even need Maven to handle this at all. You may be used to adding libraries to your project by visiting their website and downloading the latest release. You then copy the relevant `.jar` files into your project and modify the `classpath` so that the compiler can see and use them. This method however does present quite a few potential problems that Maven tries to fix.

Perhaps the biggest potential problem is handling the dependencies of those libraries themselves (the dependencies of the dependencies if you will). You've probably been there at some point. You download a library and find out that it itself needs a few other libraries or frameworks in order to operate. You then have to try and locate those files just to find that each of those has a whole set of other dependencies. After a while you end up with quite a headache on your hands. This is perhaps not readily apparent on smaller libraries, but when you start dealing with the big frameworks (think `Spring` and `Hibernate` etc), this can start to become a a real problem – and a big waste of time.

Another common problem with libraries is making sure you are using the correct version. Maybe one library needs a specific version of another in order to function properly. You then start having to delve deeper into the relevant websites in order to try and track down the right version. You then have to do it all over again if that library depends on others. Another example is when migrating to a new versions. Particularly with new JDK releases, you end up at some point updating to new supporting versions of the libraries that you're using. You then end up going through the same problem as described above.

There are a whole load of other big problems you can run into with larger applications, but these examples alone are hopefully reason enough to start doing something about it – using Maven.

Maven tries to solve these problems by managing a `repository` that contains a whole load of libraries and frameworks that you could use in your application (there are also local repositories often for use with multi-module projects). When we want to start using a certain library, we can simply tell Maven what it is and what version we want to use. As long as the dependency is in the repository somewhere, Maven will run off, collect all the relevant files for that specific version and add them to your project for you – no manual work needed at all. In addition Maven also stores all the dependencies that library needs to operate. When you tell Maven about the new library, it will not only download the files for that library, but it will also collect each and every dependency – all automatically. When you want to update or change versions, simply tell Maven about it and everything will be sorted for you.

### Collecting dependency information –

In order to add a new dependency to our project with Maven, we first need to collect the relevant information about that dependency in order for Maven to be able to correctly identify it in the repository. You can either memorise this information, or preferably use one of the many website that allow you to search for a library in the Maven repository. In this case we will be using the popular site <http://mvnrepository.com/>

In this example we will be adding the `Guava` collections library to our project. In order to get the information simply search for `'guava'` in the search-bar. A list of search results will appear containing all the relevant `artifacts` in the repository. In this case (and in most cases), the top result is what we are looking for. When you click on the link, you will be presented with a page allowing you to select which version of the library to use. In this case we will be using the most recent release – `17.0` as of writing. By clicking on the version you will be presented with information about that particular version – including any of its dependencies and what other `artifacts` depend on it. What we are interested in however is the small snippet of `XML` near the top that defines the dependency to Maven. Snippets for various other dependency management systems are also provided by the site.

### Adding the dependency to the project –

Here is the XML snippet we obtained from the repository explorer:

{% highlight xml %}  
<dependency>  
    <groupId>com.google.guava</groupId>  
    <artifactId>guava</artifactId>  
    <version>17.0</version>  
</dependency>  
{% endhighlight %}

As you can see it's really quite simple. It merely defines the `groupId` and `artifactId` of that particular dependency – much like we did when we created our project in the first tutorial. The `groupId` can be thought of as a kind of container which can potentially hold many projects. The `artifactId` defines the specific `artifact` in the container that we want to access.

In order to tell Maven about this new dependency, we simply add it to the existing `pom.xml` for your project. The `dependency` tag goes inside a container `dependencies` tag – meaning that we can have as many dependencies as we like in our project. The edited `pom.xml` looks like this:

{% highlight xml %} 
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
    <modelVersion>4.0.0</modelVersion>

    <groupId>net.ryanharrison.app</groupId>  
    <artifactId>MavenTutorial</artifactId>  
    <version>1.0-SNAPSHOT</version><packaging>jar</packaging> 

    <name>MavenTutorial</name>  
    <url>http://maven.apache.org</url><properties> <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding> </properties> 

    <dependencies>  
        <dependency>  
            <groupId>com.google.guava</groupId>  
            <artifactId>guava</artifactId>  
            <version>17.0</version>  
        </dependency>  
        <dependency>  
            <groupId>junit</groupId>  
            <artifactId>junit</artifactId>  
            <version>3.8.1</version>  
            <scope>test</scope>  
        </dependency>  
    </dependencies>
</project>
{% endhighlight %}

As you may have seen, there is already a dependency inside the `pom.xml` file – `JUnit`. This has been added automatically by the `archetype` we chose when the project was created.

And that's it! Maven will now know about that dependency when we compile our project, whereby the library will be downloaded and added to the classpath automatically. But before we compile, we first need some code to use the library in order to make sure everything has worked properly.

In the main `App.java` file, that currently has the Hello World example from the last tutorial, add the following code in order to use the `Guava` library:

{% highlight java %}
package net.ryanharrison.app;

import com.google.common.base.Joiner;

public class App {  
    public static void main(String[] args) {  
        String[] words = {"Hello", "World", "using", "the", "Guava", "library"};  
        String joined = Joiner.on(" ").join(words);  
        System.out.println(joined);  
    }  
}
{% endhighlight %}

In this example we make use of the `Joiner` class to join together an array of words with a space delimiter.

### Compiling and running the project –

Finally, in order to compile the application (including Maven downloading the dependencies), we run the command:

`mvn compile`

    > Downloading: http://repo.maven.apache.org/maven2/com/google/guava/guava/17.0/guava-17.0.pom  
    > Downloaded: http://repo.maven.apache.org/maven2/com/google/guava/guava/17.0/guava-17.0.pom (6 KB at 13.6 KB/sec)  
    > Downloading: http://repo.maven.apache.org/maven2/com/google/guava/guava-parent/17.0/guava-parent-17.0.pom  
    > Downloaded: http://repo.maven.apache.org/maven2/com/google/guava/guava-parent/17.0/guava-parent-17.0.pom (8 KB at 78.9  
    > Downloading: http://repo.maven.apache.org/maven2/com/google/guava/guava/17.0/guava-17.0.jar  
    > Downloaded: http://repo.maven.apache.org/maven2/com/google/guava/guava/17.0/guava-17.0.jar (2191 KB at 1622.6 KB/sec)

In the output you should see something like the above where Maven is downloading the dependency from the repository and placing it into your local repository (that way it doesn't have to be downloaded every time and can be shared across all your projects).

Hopefully you see the build succeeded message as output meaning that all the class file for the project have been created in the `target` folder. In order to run the program however, we first need to package it inside its own `.jar` file which contains within it the `.class` files of the dependencies (alternatively you could manually set the `classpath` when running the `java` command to point to to the `Guava` library in your local repository `.m2` folder). Although in reality this may not always happen as most of the time all of the needed `.jar` files will be deployed together, in this tutorial creating a single runnable `.jar` file will suffice.

In order to tell Maven to package the dependencies inside the same `.jar` file, we need to add the following to `pom.xml` after the closing `dependencies` tag (before the closing `project` tag):

{% highlight xml %}
<build>
    <plugins> 
        <plugin> 
            <artifactId>maven-assembly-plugin</artifactId>
            <configuration>  
                <archive>  
                    <manifest>  
                        <mainClass>net.ryanharrison.app</mainClass>  
                    </manifest>  
                </archive>  
                <descriptorRefs>  
                    <descriptorRef>jar-with-dependencies</descriptorRef>  
                </descriptorRefs>  
            </configuration> 
        </plugin>
    </plugins>
</build>
{% endhighlight %}

Now to package the project inside the one `.jar` file, run the command:

    mvn package assembly:single

A new `.jar` file should now have been created in the target folder called `MavenTutorial-1.0-SNAPSHOT-jar-with-dependencies.jar`. If you take a look inside the file, you will find all the class files for the `Guava` library.

Finally, we can run the `.jar` file and get our output:

    > C:\Projects\MavenTutorial>java -jar target/MavenTutorial-1.0-SNAPSHOT-jar-with-dependencies.jar  
    > Hello World using the Guava library

As you can see we get the joined output from our program. That's it for this tutorial, thanks for reading!

 [1]: {{ site.baseurl }}{% post_url 2014-05-05-maven-installation-getting-started %}