---
layout: post
title: Testing RESTful Ktor Services in Kotlin with Rest Assured
tags:
    - restful service
    - ktor
    - assert
    - test
    - kotlin
    - rest assured
    - junit
    - endpoint
last_modified_at: 2022-10-15
typora-root-url: ../..
---

If you're not writing a Spring application, creating good integration tests for RESTful endpoints (or any other web service) isn't always the easiest - especially when you aren't working in a dynamically typed language. [Rest Assured](http://rest-assured.io/) is a great library which makes the process a lot easier - it's designed around use in Java, but of course we can use it just fine in Kotlin as well (such as with the `Ktor` web framework).

In the following examples, a simple Kotlin web service written with [Ktor](https://ktor.io/) and [Exposed](https://github.com/JetBrains/Exposed) is tested using `Rest Assured` and `JUnit`. Note that this isn't a simple unit test of the endpoint, an actual instance of the server is started up and tested via requests to `localhost`.

**Full sample application available at** [kotlin-ktor-exposed-starter]()

## Add Test Dependencies

The first step is to add some test dependencies to our project. Just open up your `build.gradle.kts` file and add the following to the `dependencies` section (5.2.0 is the latest version of `Rest Assured` as of writing):

```kotlin
testImplementation("org.assertj:assertj-core:$assertjVersion")
testImplementation("io.rest-assured:rest-assured:$restAssuredVersion")
testImplementation("org.junit.jupiter:junit-jupiter-api:$junitVersion")
testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:$junitVersion")
```

Alongside `Rest Assured` we are also using a couple other test libraries:

- `AssertJ` - an amazing assertion library
- `JUnit5` - the test runner (shouldn't need too much explanation)

## Create Kotlin aliases

Before we start getting into using Rest Assured, because Kotlin is being used, a couple function aliases need to be created because of some methods overlapping with Kotlin keywords. In this case `when` (which is pretty vital in Rest Assured) and a helper function taking advantage of reified generics in Kotlin to convert a response object to the type we expect for further assertions.

```kotlin
protected fun RequestSpecification.When(): RequestSpecification {
    return this.`when`()
}

protected inline fun <reified T> ResponseBodyExtractionOptions.to(): T {
    return defaultMapper.decodeFromString(this.asString())
}

protected inline fun <reified T> RequestSpecification.bodyJson(obj: T): RequestSpecification {
    return this.body(defaultMapper.encodeToString(obj))
}
```

## Define a base Integration Test

In this example, all the concrete test cases which test our server endpoints will inherit from this base class. Because `Ktor` is being used, it's very straightforward to start the server up at the start of the test run and close it down at the end.

At this point we can also pass configuration options to Rest Assured (there are [plenty to check out](https://github.com/rest-assured/rest-assured/wiki/Usage)). In this case we just set the `base url` and `port` so that in our test cases we can use relative URLs which are easier to read - `/widget` instead of `http://localhost:8080/widget`.

Because we also have access to any other source files in this base class, you can also define logic to setup the database as you would like in between tests - in this case, before each test we wipe the main `Widget` table in `H2` to make sure every test starts from a blank slate.

```kotlin
open class ServerTest {
	companion object {

        private var serverStarted = false
        private lateinit var server: ApplicationEngine

        @BeforeAll
        @JvmStatic
        fun startServer() {
            if (!serverStarted) {
                server = embeddedServer(Netty, 8081, module = Application::module)
                server.start()
                serverStarted = true

                RestAssured.baseURI = "http://localhost"
                RestAssured.port = 8081
                Runtime.getRuntime().addShutdownHook(Thread { server.stop(0, 0, TimeUnit.SECONDS) })
            }
        }
    }

    @BeforeEach
    fun before() = runBlocking {
        newSuspendedTransaction {
            Widgets.deleteAll()
            Unit
        }
    }
}
```

## Create tests using Rest Assured

Now you can start using Rest Assured to test your RESTful endpoints (or any other web service really). Each test case is just a simple JUnit test so you get all the integration you would expect from using any another library. The base format is a `given --> when --> then` flow whereby first you define any entity you wish to use (in a `POST` for example), and then define your actual request with URL, followed finally by assertions on the response object.

Rest Assured includes a lot of support for making assertions on the output JSON using JSON paths etc. However I much prefer using the `to` helper we defined above to marshal the response back to our `DTO` objects. Some might frown at this approach as you shouldn't be reusing your domain classes in tests - but the response objects should take the same format anyway and I think we can agree that the test cases look a lot more readable this way. Plus as an added benefit, you get to use your good and faithful assertion libraries - my favourite being [AssertJ](http://joel-costigliola.github.io/assertj/).

### GET Requests

The below example shows testing out a `GET` request to our RESTful resource. The syntax is easy to follow, just create a `GET` request to the URL in question, make an assertion on the output status code and then extract the response body, converting it to a `List` of our model `Widget` class. Finally, just run assertions on the list to make sure it contains only the data you expect.

```kotlin
@Test
fun testGetWidgets() {
    val widget1 = NewWidget(null, "widget1", 10)
    val widget2 = NewWidget(null, "widget2", 5)
    addWidget(widget1)
    addWidget(widget2)

    val widgets = get("/widgets")
        .then()
        .statusCode(200)
        .extract().to<List<Widget>>()

    assertThat(widgets).hasSize(2)
    assertThat(widgets).extracting("name").containsExactlyInAnyOrder(widget1.name, widget2.name)
    assertThat(widgets).extracting("quantity").containsExactlyInAnyOrder(widget1.quantity, widget2.quantity)
}
```

### POST Requests

Testing out `POST` requests mainly follows the same format, however in this case you start off with a `given` expression where the `body` entity is defined, alongside the content type (JSON in this case). After that, the only difference is the request method. In the exact same manner as before, the output is extracted and similar assertions are run.

```kotlin
@Test
fun testUpdateWidget() {
    // when
    val widget1 = NewWidget(null, "widget1", 10)
    val saved = addWidget(widget1)

    // then
    val update = NewWidget(saved.id, "updated", 46)
    val updated = given()
        .contentType(ContentType.JSON)
        .bodyJson(update)
        .When()
            .put("/widgets")
            .then()
            .statusCode(200)
            .extract().to<Widget>()

    assertThat(updated).isNotNull
    assertThat(updated.id).isEqualTo(update.id)
    assertThat(updated.name).isEqualTo(update.name)
    assertThat(updated.quantity).isEqualTo(update.quantity)
}
```

### Error Cases

As good testers we of course want to test the negative cases as well, for typical RESTful services this will involve looking at the response status code and maybe checking that the response contains the correct error message etc:

```kotlin
@Test
fun testDeleteInvalidWidget() {
    delete("/widget/{id}", "-1")
        .then()
        .statusCode(404)
}
```

## Docs

The Rest Assured [usage guide](https://github.com/rest-assured/rest-assured/wiki/Usage) is very comprehensive and gives a good overview of what Rest Assured can accomplish. In the examples above I have showed only the basic functionality - but to be honest for a lot of cases this is all your really need.

The main differences you will see in other examples is that in a typical Rest Assured test, the `body` method is used to run `Hamcrest` matchers against certain JSON elements. You can also test forms, run JSON schema validations, test against XML and use `JSONPath` to access specific nodes.

Find a lot more real-world use cases in the following two projects. This also includes testing Ktor websockets:

<https://github.com/raharrison/kotlin-ktor-exposed-starter/tree/master/src/test/kotlin>

<https://github.com/raharrison/lynks-server/tree/master/src/test-integration/kotlin>
