---
layout: post
title: Kotlin - Add Integration Test Module
tags:
    - kotlin
    - gradle
    - module
    - integration tests
typora-root-url: ../..
---

The default package structure for a new [Kotlin](https://kotlinlang.org/) project generated through [IntelliJ](https://www.jetbrains.com/idea/) looks like the following, whereby you have a main source folder with `source sets` (modules) for your `main` files and then `test` source files.

![Kotlin Default Project](/images/2018/kotlin-default-project.png)

Typically, you would place your unit tests within the auto-generated `test` module, and then run them all at once (within one JVM). IntelliJ is generally set up to support this use case and if that's all you need, requires minimal setup and effort.

However, if you also need to add integration tests (or end-to-end etc), then this project structure can start to cause issues. For example, consider a typical project setup for a server-side app:

-   `main` - business logic and main app files
-   `test` - unit tests,
    -   typically with [JUnit](https://junit.org/junit5/) or similar
    -   spin up in-memory [H2](http://www.h2database.com/html/main.html) database for easy DAO testing
-   `test-integration` - integration/e2e tests
    -   typically testing API endpoints with [Rest Assured](http://rest-assured.io/) or similar
    -   start up full version of the server and any dependencies

You can't merge all the tests into one module and run them all at once because you would need to start up multiple database instances etc. Conflicts arise and it's apparent that you need to run them separately in their own dedicated JVM.

To add the above mentioned `testIntegration` module, you can make some edits to your `build.gradle` file to define a new `source set` (IntelliJ module):

```groovy
sourceSets {
    testIntegration {
        java.srcDir 'src/testIntegration/java'
        kotlin.srcDir 'src/testIntegration/kotlin'
        resources.srcDir 'src/testIntegration/resources'
        compileClasspath += main.output
        runtimeClasspath += main.output
    }
}
```

Here, a new `source set` for integration tests is created. [Gradle](https://gradle.org/) is told where the Java and Kotlin source files live and we specify that the classpath inherits from the `main` source set. This allows you to reference classes of your `main` module within the integration tests (you might not need this).

Then, we provide a `configuration` and `task` for the new source set to ensure that the new module contains the same dependencies as within the main `test` module (defined using `testCompile` in your `dependencies`). Finally, define a new `Task` to run the integration tests, pointing it to the classes and classpath of the `testIntegration` source set instead of the inherited defaults from `test`:

```groovy
configurations {
    testIntegrationImplementation.extendsFrom testImplementation
    testIntegrationRuntime.extendsFrom testRuntime
}

task testIntegration(type: Test) {
    testClassesDirs = sourceSets.testIntegration.output.classesDirs
    classpath = sourceSets.testIntegration.runtimeClasspath
}
```

Similarly to how you might have previously set the target bytecode version for the `main` and `test` modules, you need to do the same for the new module:

```groovy
compileTestIntegrationKotlin {
    kotlinOptions.jvmTarget = "1.8"
}
```

If you run Gradle with the option to 'Create directories for empty content roots automatically', you should see a new module get created. You might notice one issue though, the new module is not marked as a test module within IntelliJ. You could do this manually, but it would get reset every time Gradle runs. To override this, you can apply the `idea` plugin and add the source directories of the new source set:

```groovy
idea {
    module {
        testSourceDirs += project.sourceSets.testIntegration.java.srcDirs
        testSourceDirs += project.sourceSets.testIntegration.kotlin.srcDirs
        testSourceDirs += project.sourceSets.testIntegration.resources.srcDirs
    }
}
```

Now you will see the desired output after Gradle runs:

![With Integration tests module](/images/2018/kotlin-integration-test-module.png)

**WARNING** - This approach is not without problems. If you look at the `Test Output Path` of the new module, it is defined as `\kotlin-scratchpad\out\test\classes` which is the same as the main `test` module. Therefore, all the compiled test classes will end up in the same directory - which causes issues if you try to `Run All` for example. To fix this, you have to manually update the path to `\kotlin-scratchpad\out\testIntegration\classes`. Alternatively, you might not apply the `idea` plugin and just mark the module for tests each time Gradle runs. Hopefully I will find a fix for this at some point.
{: .info-block}
