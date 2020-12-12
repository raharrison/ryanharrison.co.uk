---
layout: post
title: The Importance of Integration Testing Part 1 - HTTP Endpoints
tags:
  - integration testing
  - http
  - endpoint
  - spring
  - mockmvc
  - java
typora-root-url: ..
---

Bert is a new joiner within the team. As his first task he's been assigned to create a simple endpoint to expose some existing data onto one of the front-end screens. His manager says that this should give him a gentle introduction to the area whilst also giving opportunity to gain familiarity with the codebase and SDLC processes. She mentions that he should keep in regular contact with Brenda who will be handling the UI changes. Bert agrees, he's already quite familiar with `Spring Boot` from his previous position - creating a simple new endpoint in an existing service should be straightforward he thinks to himself. It should look good if he can get this finished and signed off within a couple days.

Bert clones the repo and notices that the service doesn't yet expose any API endpoints (Spring `@RestController`) so he quickly creates a new one, using the existing service pointed out to him by his teammate Ben (simplified below).

```java
@RestController 
@RequiredArgsConstructor 
public class SomeResultEndpoint { 

  private final SomeResultService someResultService; 

  @GetMapping(value = "/someResult") 
  public SomeResult getSomeResult() { 
    return someResultService.getSomeResult(); 
  } 
}
```
During a quick catch-up, Ben informs Bert about the team's core shared library, which includes various components that should automatically handle all the other key requirements for him. This includes things like authentication, object mapping and error handling. Bert starts up the service locally, pointing to the dev database, hits the endpoint and can see data returns successfully. Content that everything looks to be working ok, Bert moves on to writing tests for the change. He knows from reading the team's SDLC documentation that the pull request build will fail if it sees any drop in code coverage.

### The Bad

Generally the first thing done in these situations is the trusty unit test cases - and that's exactly what Bert does initially. In Java, tools like `JUnit` and `Mockito` (amongst many others) make this kind of change straightforward to unit test, just mock out the service dependency and ensure the controller behaves as expected. Bert comes up with the following simple test case:

```java
class SomeResultEndpointTest { 

  private SomeResultEndpoint someResultEndpoint; 

  private SomeResultService someResultService; 

  @BeforeEach 
  void setUp() { 
    someResultService = mock(SomeResultService.class); 
    someResultEndpoint = new SomeResultEndpoint(someResultService); 
  } 

  @Test 
  void getSomeResult() { 
    SomeResult expected = TestUtils.getSomeResultData(); 
    when(someResultService.getSomeResult()).thenReturn(expected); 
    SomeResult actual = someResultEndpoint.getSomeResult(); 
    assertThat(actual).isEqualTo(expected); 
    verify(someResultService, times(1)).getSomeResult(); 
  } 
}
```

Initially, Bert tried to construct some test `SomeResult` instances himself, but quickly realised that the data structure was complex and he was unfamiliar with what a real-world scenario would look like. Thankfully, Ben pointed him towards some existing helper methods, created alongside the original service, that looked to create some realistic data and populate most of the fields.

Bert ran the test suite, and as expected, everything passed successfully. But Bert had some issues - what about the negative scenarios? What about the `HTTP` status codes etc? All this was being handled by either Spring or the core shared library components. Bert created a simple negative test case, but then began to realise that there wasn't really much more that he could add here:

```java
@Test 
void getSomeResult_propagates_exception() { 
  when(someResultService.getSomeResult()).thenThrow(new RuntimeException("error"); 
  assertThrows(RuntimeException.class, () -> someResultEndpoint.getSomeResult()); 
}
```
Bert commits his change, pushes it and creates a pull request for the team to review. The build passes successfully and code coverage is 100% on Bert's changes - great! The pull request gets approved, merged and deployed into the dev/qa environments. Bert pings Brenda (who is doing the UI changes) that the change is ready to begin integrating with.

### The Ugly

The next day Bert gets a message from Brenda - "the service isn't working properly", she explains. "Every time I call it in QA I get a `500` error returned". Bert quickly pulls up the logs and notices many exceptions being thrown from the endpoint - all of which seem to be related to `Jackson` when the response `SomeResult` is converted to JSON.

```plaintext
com.fasterxml.jackson.databind.JsonMappingException: Infinite recursion (StackOverflowError) (through reference chain: java.util.concurrent.ConcurrentHashMap[" "]->com.java.sample.OraganisationStructures$$EnhancerBySpringCGLIB$$99c7d84b["$$beanFactory"]->org.springframework.beans.factory.support.DefaultListableBeanFactory["forwardRef"]at com.fasterxml.jackson.databind.ser.std.BeanSerializerBase.serializeFields(BeanSerializerBase.java:706) 
at at com.fasterxml.jackson.databind.ser.BeanSerializer.serialize(BeanSerializer.java:155) 
at at com.fasterxml.jackson.databind.ser.BeanPropertyWriter.serializeAsField(BeanPropertyWriter.java:704) 
at at com.fasterxml.jackson.databind.ser.std.BeanSerializerBase.serializeFields(BeanSerializerBase.java:690) 
at at com.fasterxml.jackson.databind.ser.BeanSerializer.serialize(BeanSerializer.java:155) 
```

A quick search of the error indicated a circular reference issue when trying to serialize the `SomeResult` instance. Sure enough, the data structure contained self references. Ben explained that it was actually a linked-list type structure, useful for the existing processing but perhaps not ideal for an endpoint representation. "Why didn't this issue come up when you were testing?", asked Ben. Some investigation later, Bert found that the dev database had old data, preventing such instances from ever being created when he ran it locally. The test utility methods did create this scenario, but the tests themselves had failed to pick up the issue. Ben suggests, "I guess we have never tried converting that model to JSON before". Bert quickly resolved the issue, pushed his changes and informed Brenda about the fix - noting that he didn't have to change any of the tests as part of his change.

The next day Bert gets another message from Brenda - "I'm now seeing some strange behaviour when unauthorized users call the endpoint. I expect the response to conform to our standard error model, but I just get a wall of text and a `500` error instead of the `401` status code I expect". Again Bert checks the logs, he sees new `AuthorizationException` stack traces coming from the shared library component which performs the authorization checks. This looks like expected behaviour, Bert ponders, but why doesn't the response get mapped correctly? Ben points him towards the `AuthExceptionMapper` class in the shared library, which converts the exception to the common error model. After some debugging, Bert found that the mapper had not been correctly configured in the service. Ben explained, "that mapper is still quite new, I guess it never got added since that service hasn't exposed any endpoints before". Again, Bert quickly fixes the issue, pushes his changes and informs Brenda - again noting that he did not have to change any of his test cases as part of the fix.

### The Good

After these fixes, the new endpoint works as expected and Brenda is able to integrate successfully, but Bert is quite rightly less than satisfied. Not only did an otherwise straightforward change take much longer than it should, even now he could not be confident that it works as expected in all scenarios, let alone 6 months down the line. Bert brings up the issue in the sprint retrospective, highlighting a number of areas that are not covered by the current test suites - even though the code coverage metrics might suggest they are:

- JSON object marshalling - both in request and response bodies
- URL formatting and HTTP request methods
- usage of query and/or path parameters
- any exception scenario requiring use of separate exception mappers or handlers (response format and HTTP status codes)
- any additional functionality provided in controller advice, filters, converters etc.

The team agrees, clearly there is a need for automated integration tests for these endpoints in addition to the conventional unit tests. Thankfully, Spring comes with a number of built-in solutions - one being `MockMvc`, which the team end-up using. A typical problem for integration tests like this is the need to spin-up a full Spring container - for most apps that might mean queue listeners get created, calling out to other services during startup etc - not something that is ideal for a short-lived test suite. Bert suggests configuring the app in such a way that allows for a "test" instance to be started (without all the external dependencies etc.) - to make creation of a proper integration test suite much easier. But in the meantime, `MockMvc` has a nice way around it:

> Using this annotation will disable full auto-configuration and instead apply only configuration relevant to MVC tests (i.e. `@Controller`, `@ControllerAdvice`, `@JsonComponent`, `Converter/GenericConverter`, `Filter`, `WebMvcConfigurer` and `HandlerMethodArgumentResolver` beans but not `@Component`, `@Service` or `@Repository` beans).
>

Bert explains that this in effect gives you a a cut-down Spring container which just creates the components required to support `MVC/REST` functionality. No need for the rest of your beans to be created, those can be mocked out as usual. Bert comes up with the following additional test cases for the original change:

```java
@WebMvcTest(SomeResultEndpoint.class) 
class SomeResultEndpointIntTest { 

  @Autowired 
  private MockMvc mockMvc; 

  @MockBean 
  private SomeResultService someResultService; 

  @MockBean 
  private AuthorizationService authorizationService; 

  @Test 
  void getSomeResult_succeeds() throws Exception { 
    when(authorizationService.isAuthorized(anyString())).thenReturn(true); 
    SomeResult expected = TestUtils.getSomeResultData();  
    when(someResultService.getSomeResult()).thenReturn(expected); 

    this.mockMvc.perform(get("/someResult")) 
      .andExpect(status().isOk()) 
      .andExpect(content().string(equalTo(marshalObject(expected)))); 
  } 

  @Test 
  void getSomeResult_notfound() throws Exception { 
    when(authorizationService.isAuthorized(anyString())).thenReturn(true); 
    when(someResultService.getSomeResult()).thenReturn(null); 

    mockMvc.perform(get("/someResult")) 
      .andExpect(status().isNotFound()); 
  } 

  @Test 
  void getSomeResult_unauthorized() throws Exception { 
    when(authorizationService.isAuthorized(anyString())).thenReturn(false); 
    SomeResult expected = TestUtils.getSomeResultData();  
    when(someResultService.getSomeResult()).thenReturn(expected); 

    mockMvc.perform(get("/someResult")) 
      .andExpect(status().isUnauthorized()); 
  } 
}
```

The above are three very simple test cases, but crucially provide coverage in a number of key areas:

- we have the correct URL and are able to respond to `GET` requests over `HTTP`
- the response can be successfully serialized to the required response format and matches the expected output (JSON in this case, but it could be anything)
- exceptions are handled as expected, the `HTTP` response status codes are correct

Bert highlights that Spring has a number of other methods of handling the above - `@SpringBootTest` if you want to really startup the full application (combine with `@ActiveProfiles`) alongside utils like `TestRestTemplate`, but the team agrees that even just the above is a vast improvement.

### Takeaways (TL;DR)

The example above is somewhat contrived, but really these scenarios are not unrealistic at all. There can easily be large areas of your application that your tests don't actually cover - likely parts that are deeply reliant on 'magic' from your framework of choice and/or rely on (at least part of) your application to be running in order to test. How does your code integrate with the framework or other libraries? Is your configuration correct? You need something more than unit tests for this kind of thing and you want to know about such issues as early as possible.

- Unit tests are great, but not enough on their own
- Code coverage metrics will lie to you
- Making any change/fix that doesn't require you to also modify a test is a red flag
- We rely more and more on the 'magic from the framework', but how do we test it? How do we know we've configured it correctly?
- Above the core business logic (unit cases), every HTTP endpoint should have automated tests covering URL descriptors, methods, object marshalling, exception handling etc.
- `Spring MockMvc` is a neat way of producing integration tests for your endpoints, but is not the only solution, see 
  - <https://spring.io/guides/gs/testing-web/>
  - <https://docs.github.com/en/github/administering-a-repository/configuration-options-for-dependency-updates>