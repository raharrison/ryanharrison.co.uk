---
layout: post
title: Mocking Time in Java
tags:
  - java
  - testing
  - junit
  - mockito
  - time
  - clock
---

If your code calls `LocalDateTime.now()` or `Instant.now()` directly, you're stuck with whatever the system clock says. This makes
it nearly impossible to write deterministic tests for time-sensitive logic like expiration checks, scheduling, or time-based
calculations.

The solution is to inject time as a dependency rather than calling static `now()` methods directly. Java's `Clock` abstraction
provides a clean way to do this, and there are several approaches depending on your needs.

## The Problem with Static now() Calls

Consider a service that checks if a subscription has expired:

```java
public class SubscriptionService {
    public boolean isExpired(Subscription subscription) {
        return subscription.getExpiryDate().isBefore(LocalDateTime.now());
    }
}
```

This code is difficult to test because `LocalDateTime.now()` always returns the actual current time. You can't easily test the
boundary conditions around expiration without changing your system clock or waiting for time to pass.

<!--more-->

## Using Clock for Dependency Injection

The `java.time.Clock` class was designed to solve this problem. Instead of calling static `now()` methods, you pass a `Clock`
instance to the time API:

```java
LocalDateTime.now(clock);
Instant.now(clock);
ZonedDateTime.now(clock);
```

Refactor your code to accept a `Clock` parameter:

```java
public class SubscriptionService {
    private final Clock clock;

    public SubscriptionService(Clock clock) {
        this.clock = clock;
    }

    public boolean isExpired(Subscription subscription) {
        return subscription.getExpiryDate().isBefore(LocalDateTime.now(clock));
    }
}
```

In production, inject `Clock.systemDefaultZone()` or `Clock.systemUTC()`. In tests, use a fixed clock.

## Built-in Clock Implementations

Java provides several `Clock` implementations out of the box:

### Clock.fixed()

Creates a clock that always returns the same instant. Good for most unit tests:

```java

@Test
void testExpiredSubscription() {
    Clock clock = Clock.fixed(
            Instant.parse("2026-01-20T10:00:00Z"),
            ZoneId.of("UTC")
    );

    SubscriptionService service = new SubscriptionService(clock);

    Subscription subscription = new Subscription(
            LocalDateTime.parse("2026-01-20T09:00:00")
    );

    assertTrue(service.isExpired(subscription));
}
```

### Clock.offset()

Creates a clock that's offset from another clock by a duration. Useful when you need to test time progression:

```java

@Test
void testRenewalWindow() {
    Clock baseClock = Clock.fixed(
            Instant.parse("2026-01-20T10:00:00Z"),
            ZoneId.of("UTC")
    );

    // Create a clock 30 days in the future
    Clock futureClock = Clock.offset(baseClock, Duration.ofDays(30));

    RenewalService service = new RenewalService(futureClock);
    assertTrue(service.isInRenewalWindow(subscription));
}
```

### Clock.system()

The production clocks that return the actual system time:

```java
// Uses system default timezone
Clock.systemDefaultZone();

// Uses UTC timezone
Clock.systemUTC();

// Uses specific timezone
Clock.system(ZoneId.of("America/New_York"));
```

## MutableClock from ThreeTen-Extra

For tests that need to simulate time progression, the [MutableClock](https://www.threeten.org/threeten-extra/apidocs/org.threeten.extra/org/threeten/extra/MutableClock.html) from the threeten-extra library is useful. 
It allows you to advance time during a test.

Add the dependency:

```xml

<dependency>
    <groupId>org.threeten</groupId>
    <artifactId>threeten-extra</artifactId>
    <version>1.8.0</version>
    <scope>test</scope>
</dependency>
```

Use it to control time in your tests:

```java

@Test
void testTokenExpiration() {
    MutableClock clock = MutableClock.of(
            Instant.parse("2026-01-20T10:00:00Z"),
            ZoneId.of("UTC")
    );

    TokenService service = new TokenService(clock);
    String token = service.createToken("user123");

    assertTrue(service.isValid(token));

    // Advance time by 2 hours
    clock.add(Duration.ofHours(2));

    // Token should now be expired
    assertFalse(service.isValid(token));
}
```

This is cleaner than creating multiple fixed clocks or using offset clocks for complex time-based scenarios.

<!--more-->

## Using Mockito MockedStatic (Antipattern)

Mockito 3.4+ supports mocking static methods with `MockedStatic`. You might be tempted to use this for mocking
`LocalDateTime.now()`:

```java

@Test
void testWithMockedStatic() {
    try (MockedStatic<LocalDateTime> mock = mockStatic(LocalDateTime.class)) {
        LocalDateTime fixedTime = LocalDateTime.parse("2026-01-20T10:00:00");
        mock.when(LocalDateTime::now).thenReturn(fixedTime);

        SubscriptionService service = new SubscriptionService();
        // Test code here
    }
}
```

**This is generally an antipattern and should be avoided:**

- **Thread safety issues**: `MockedStatic` affects all threads, which can cause flaky tests in parallel test suites
- **Design smell**: If you need to mock static methods, it usually indicates your code isn't designed for testability
- **Performance**: Static mocking is slower than dependency injection
- **Scope**: Easy to accidentally leak mocks between tests if not careful with cleanup

The `Clock` abstraction exists specifically to avoid needing static mocking. Use it instead.

## More Reading

- [Java Clock Documentation](https://docs.oracle.com/javase/8/docs/api/java/time/Clock.html)
- [ThreeTen-Extra MutableClock](https://www.threeten.org/threeten-extra/apidocs/org.threeten.extra/org/threeten/extra/MutableClock.html)
- [Mockito MockedStatic Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html#static_mocks)
