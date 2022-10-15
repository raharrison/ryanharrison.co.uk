---
layout: post
title: RESTful Kotlin with Ktor and Exposed
tags:
  - kotlin
  - ktor
  - exposed
last_modified_at: 2022-10-15
---

**Updated for Ktor 2.1 and Kotlin 1.7.20+**

I've been writing a lot more Kotlin recently and have been really liking the language so far. I'll probably write another post pointing out some of my favourite features, but in short it's basically Java, but without all the annoying stuff. I think in terms of adoption it's still very early days for Kotlin, but due to the great interop with Java and being an official language for Android development, I wouldn't be surprised if it doesn't start to become extremely popular over the next few years.

Kotlin is pretty versatile, even though most people no doubt focus on the Android side of things. That doesn't mean however that server side development isn't also supported - in fact, quite the opposite. The Spring framework already has built-in support for Kotlin and many other libraries are also focusing attention on it. You *could* use such Java focused libraries, but instead you could use the dedicated Kotlin libraries - some of which are supported by [JetBrains](https://www.jetbrains.com/) themselves.

All the code for the following example is available in the GitHub project [kotlin-ktor-exposed-starter](https://github.com/raharrison/kotlin-ktor-exposed-starter).

## Create a Kotlin Project

First things first on our way to creating a barebones REST server in Kotlin. Open up IntelliJ and create a new Kotlin project. This will create the basic file structure and a `gradle` build file (in this example we will be using the Kotlin DSL). To make sure everything is working, you can run the basic Hello World:

```kotlin
fun main(args: Array<String>) {
    println("Hello World!")
}
```

## Setting up Ktor Async Web Framework

[Ktor](https://github.com/ktorio/ktor) is great library for creating simplistic and lightweight web services in Kotlin. It's completely asynchronous through the use of `coroutines` and as such should scale very well with load. It's still in active development so might have some rough edges, but on the whole it seems solid. The documentation is somewhat lacking, but has improved significantly since the `0.x` days. 

Add the following to `build.gradle.kts` to add ktor as a dependency and allow the use of kotlin coroutines (an experimental feature as of writing). We are also using the new `kotlinx.serialization` library instead of traditional libraries such as `Jackson` for slightly better performance

```groovy
plugins {
    kotlin("jvm") version "1.7.20"
    kotlin("plugin.serialization") version "1.7.20"
    application
}

repositories {
    mavenCentral()
}
val ktorVersion = "2.1.2"
dependencies {
    implementation("io.ktor:ktor-server-core:$ktorVersion")
    implementation("io.ktor:ktor-serialization:$ktorVersion")
    implementation("io.ktor:ktor-server-netty:$ktorVersion")
    implementation("io.ktor:ktor-server-call-logging:$ktorVersion")
    implementation("io.ktor:ktor-server-default-headers:$ktorVersion")
    implementation("io.ktor:ktor-server-websockets:$ktorVersion")
    implementation("io.ktor:ktor-server-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
    // ommitted test dependencies
}
```

The full example Gradle file is available [here](https://github.com/raharrison/kotlin-ktor-exposed-starter/blob/master/build.gradle.kts). In this case, we're making use of the [Netty](https://github.com/netty/netty) application server, although `servlet` based options are also  available (although not sure why you would want to sacrifice async).

## Create a Ktor application

The main configuration for a Ktor app (`module`) is very straightforward (`MainKt` file):

```kotlin
fun Application.module() {
    install(DefaultHeaders)
    install(CallLogging)
    install(WebSockets) {
        contentConverter = KotlinxWebsocketSerializationConverter(JsonMapper.defaultMapper)
    }

    install(ContentNegotiation) {
        json(JsonMapper.defaultMapper)
    }

    val widgetService = WidgetService()

    install(Routing) {
        index()
        widget(widgetService)
    }
}

fun main(args: Array<String>) {
    embeddedServer(Netty, commandLineEnvironment(args)).start(wait = true)
}
```

Here a new `Ktor` `module` is created. `Ktor` is configured around the concept of `plugins` which can be installed into the main request pipeline. In this example we add pluginsto add default headers to all our responses, log our calls for debugging and also configure processing of JSON requests and conversion to responses. Finally, the main `Routing` feature is used to designate which paths to handle in our app. We defer to another extension method defined elsewhere to define the routes for a `widget` RESTful service. To run the application, the `main` method starts a `Netty` server pointing to the `module` we just created.

Ktor is configuring using an `application.conf` similar to how Spring would use `application.properties`:

```
ktor {
    deployment {
        port = 8080
        watch = [ build ]
    }

    application {
        modules = [ MainKt.module ]
    }
}
```

Here we provide the port `Ktor` should bind to and the path to the main `module` path which will be used for our app.

Of course for anything to actually happen, we need to define the widget routes and service themselves.

## Defining Routes

Here is the definition of the `widget` extension method which defines the interface for our service:

```kotlin
fun Route.widget(widgetService: WidgetService) {

    route("/widgets") {

        get {
            call.respond(widgetService.getAllWidgets())
        }

        get("/{id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalStateException("Must provide id")
            val widget = widgetService.getWidget(id)
            if (widget == null) call.respond(HttpStatusCode.NotFound)
            else call.respond(widget)
        }

        post {
            val widget = call.receive<NewWidget>()
            call.respond(HttpStatusCode.Created, widgetService.addWidget(widget))
        }

        put {
            val widget = call.receive<NewWidget>()
            val updated = widgetService.updateWidget(widget)
            if (updated == null) call.respond(HttpStatusCode.NotFound)
            else call.respond(HttpStatusCode.OK, updated)
        }

        delete("/{id}") {
            val id = call.parameters["id"]?.toInt() ?: throw IllegalStateException("Must provide id")
            val removed = widgetService.deleteWidget(id)
            if (removed) call.respond(HttpStatusCode.OK)
            else call.respond(HttpStatusCode.NotFound)
        }
    }
}
```

As you can see the Ktor `DSL` is very intuitive thanks mainly to extension methods and lambda parameter syntax in Kotlin. The basic `HTTP` method are defined for dealing with widgets - each of which defer to our service which can do all the database access etc.

Note that the `post` and `put` methods expect an instance of the `NewWidget` class (as converted via JSON). This is defined as a Kotlin `data class` for a widget instance with an optional `id`:

```kotlin
@Serializable
data class NewWidget(
        val id: Int? = null,
        val name: String,
        val quantity: Int
)
@Serializable
data class Widget(
        val id: Int,
        val name: String,
        val quantity: Int,
        val dateUpdated: Long
)
```

Just like if we were using `Jackson`, simple data objects work well with `Ktor`. As we are using `kotlinx.serialization` we just need to add the `@Serializable` attribute to the compiler plugin knows to visit these classes and generate the full serializable classes.

## Setting up Exposed

[Exposed](https://github.com/JetBrains/Exposed) is another JetBrains sponsored library (though not officially) for database interactions in Kotlin. It is a kind of `ORM`, but unlike `Hibernate` it's very simple and lightweight. In this post we're going to use [H2](https://github.com/h2database/h2database) as a simple in-memory database and [HikariCP](https://github.com/brettwooldridge/HikariCP) for connection pooling. Add the following dependencies:

```groovy
implementation("com.h2database:h2:$h2Version")
implementation("org.jetbrains.exposed:exposed-core:$exposedVersion")
implementation("org.jetbrains.exposed:exposed-jdbc:$exposedVersion")
implementation("com.zaxxer:HikariCP:$hikariCpVersion")
implementation("org.flywaydb:flyway-core:$flywayVersion")
implementation("ch.qos.logback:logback-classic:$logbackVersion")
```

`Exposed` has two ways of interacting with databases - their `DSL` and `DAO`. In this post I focus only on the `DSL` (sql builder) as I think that's where the library excels. The `DAO` syntax is nice, but introduces complexity when dealing with web frameworks as you have to convert to your own model class manually. The following defines a `Table` for widgets:

```kotlin
object Widgets : Table() {
    val id = integer("id").autoIncrement()
    val name = varchar("name", 255)
    val quantity = integer("quantity")
    val dateUpdated = long("dateUpdated")
    override val primaryKey = PrimaryKey(id)
}
```

It's quite straightforward, we just define our columns as fields and use the fluent column builder to define attributes. We can then make use of the `Widgets` object application wide to query the table.

## Connection Pooling and Database Threads

Now we can setup a connection pool for database interaction. This example uses `HikariCP` as it's the most widely used library for this at the moment:

```kotlin
private fun hikari(): HikariDataSource {
    val config = HikariConfig().apply {
        driverClassName = "org.h2.Driver"
        jdbcUrl = "jdbc:h2:mem:test"
        maximumPoolSize = 3
        isAutoCommit = false
        transactionIsolation = "TRANSACTION_REPEATABLE_READ"
        validate()
    }
    return HikariDataSource(config)
}
```

Now we can tell `Exposed` to connect to our `H2` db and create the widgets table. **Note:** in the example project I use [Flyway](https://flywaydb.org/) to perform proper database migrations for table creation. Check out the repo for details as this is beyond the scope of this post.

```kotlin
Database.connect(hikari())
transaction {
    create(Widgets)
}
```

A key thing to note when dealing with the async world is that you really don't want to block any of the threads that are handling web requests. Unlike the standard servlet model where each request is tied to a thread, when you block in an async app you are essentially also blocking any other work from being done. If you do this a lot or have a spike in load, your app will grind to a halt.

This presents a problem when using standard `JDBC` to query our database because the framework is inherently blocking and so our threads will cease when waiting for results sets. To get around this, we must do our database queries on a dedicated thread pool. This is only really possible through coroutines which can `suspend` and `resume` as needed. The flow will be:

1. Coroutine `A` starts to handle main web request from user
2. Database query needed so another coroutine `B` is starting on another thread pool to perform this blocking operation
3. `A` suspends execution until `B` is finished. Due to the nature of coroutines, the underlying thread is then free to perform other work (handling other requests)
4. Background coroutine `B` finishes after database query. Thread is returned to the thread pool for other queries etc
5. `A` resumes execution by restoring the previous state it had before suspension. It now has access to the query results which can be passed back as the response. Note that the coroutine `A` may now be executing on a different thread than in step 1 (pretty cool right?)

This might sound like a lot of work (and it is), but thanks to the coroutines library in Kotlin, this is thankfully very easy to accomplish. The following helper method, which is used across all database interaction in our service class, runs a block of code inside a transaction in this new coroutine.  `Dispatchers.IO` references a thread pool managed by Kotlin coroutines that is meant for blocking IO operations like these. Once called, this function will suspend the current coroutine and launch a new one on the special `IO` thread pool - which will then block whilst the database transaction is performed. When the result is ready, the coroutine is resumed and returned to the initial caller.

```kotlin
suspend fun <T> dbExec(
    block: () -> T
): T = withContext(Dispatchers.IO) {
    transaction { block() }
}
```

The method is marked as suspend which will allow the suspension of `A` described in step 3.

## Database Queries with Exposed

Finally, we need to define the `WidgetService` which will be making use of the database we just set up. The whole code is available in the GitHub project, but here is the method to retrieve a specific widget:

```kotlin
suspend fun getWidget(id: Int): Widget? = dbExec {
    Widgets.select {
        (Widgets.id eq id)
    }.map { toWidget(it) }
    .singleOrNull()
}
```

As you can see we make use of the `dbExec` helper to perform our query. The Exposed DSL for queries is nice and easy to read. The result of the select is a `ResultRow`, so I define a helper to perform the mapping to our model class:

```kotlin
private fun toWidget(row: ResultRow): Widget =
    Widget(
        id = row[Widgets.id],
        name = row[Widgets.name],
        quantity = row[Widgets.quantity],
        dateUpdated = row[Widgets.dateUpdated]
)
```

Something like `Hibernate` (or the DAO in Exposed) would do this automatically, but Exposed is just a lightweight wrapper around the sql so we have full control of what's happening. Here is the method to add and delete a widget - again fairly intuitive to read:

```kotlin
suspend fun addWidget(widget: NewWidget): Widget {
    var key = 0
    dbExec {
        key = (Widgets.insert {
            it[name] = widget.name
            it[quantity] = widget.quantity
            it[dateUpdated] = System.currentTimeMillis()
        } get Widgets.id)
    }
    return getWidget(key)!!.also {
        onChange(ChangeType.CREATE, key, it)
    }
}

suspend fun deleteWidget(id: Int): Boolean {
    return dbExec {
        Widgets.deleteWhere { Widgets.id eq id } > 0
    }.also {
        if (it) onChange(ChangeType.DELETE, id)
    }
}
```

And that's it! Pretty straightforward in terms of lines of code to create a REST server with database interaction. Start the app as you would any other program (no need to deploy to any app server) and test out the widget routes.

The full example is available in the GitHub project [kotlin-ktor-exposed-starter](https://github.com/raharrison/kotlin-ktor-exposed-starter). This also contains some extra's:

- Database migrations using [Flyway](https://flywaydb.org/)
- Notifications with [Ktor](https://ktor.io/) websockets
- Unit and integration testing of our services using a fully running server and [Rest Assured](http://rest-assured.io/)
- Code coverage and reporting using [Kover](https://github.com/Kotlin/kotlinx-kover)