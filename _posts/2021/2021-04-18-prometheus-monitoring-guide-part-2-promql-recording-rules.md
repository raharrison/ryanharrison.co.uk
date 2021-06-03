---
layout: post
title: Prometheus Monitoring Guide Part 2 - PromQL and Recording Rules
tags:
    - prometheus
    - monitoring
    - promql
    - query
    - rule
    - metrics
    - metric
    - time
    - vector
    - series
    - labels
    - http
typora-root-url: ../..
---

-   [Part 1 - Installation and Instrumentation]({{ site.baseurl }}{% post_url 2021/2021-04-05-prometheus-monitoring-guide-part-1-install-instrumentation %})

## PromQL

Prometheus provides a functional query language called PromQL (Prometheus Query Language) that lets the user select and aggregate time series data in real time. The result of an expression can either be shown as a graph, viewed as tabular data in Prometheus's expression browser, or consumed by external systems via the HTTP API.

### Data Types

An expression or sub-expression can evaluate to one of four types:

-   **Instant vector** - a set of time series containing a single sample for each time series, all sharing the same timestamp (`prometheus_http_requests_total`)
-   **Range vector** - a set of time series containing a range of data points over time for each time series (`prometheus_http_requests_total[5m]`)
-   **Scalar** - a simple numeric floating point value

Depending on the use-case (e.g. when graphing vs. displaying the output of an expression), only some of these types are legal as the result from a user-specified expression. For example, an expression that returns an instant vector is the only type that can be directly graphed.

### Selectors and Matchers

In the simplest form, only a metric name is specified. This results in an instant vector containing elements for all time series that have this metric name:

```plain
http_requests_total
```

It is possible to filter these time series further by appending a comma separated list of label matchers in curly braces (`{}`).

This example selects only those time series with the `http_requests_total` metric name that also have the `job` label set to `prometheus` and their `group` label set to `canary`:

```plain
http_requests_total{job="prometheus",group="canary"}
```

-   `=` - select labels that are exactly equal to the provided string
-   `!=` - select labels that are not equal to the provided string
-   `=~` - select labels that regex-match the provided string
-   `!~` - select labels that do not regex-match the provided string

Range vector literals work like instant vector literals, except that they select a range of samples back from the current instant. A time duration is appended in square brackets (`[]`) at the end of a vector selector to specify how far back in time values should be fetched for each resulting range vector element.

In this example, we select all the values we have recorded within the last 5 minutes for all time series that have the metric name `http_requests_total` and a `job` label set to `prometheus`:

```plain
http_requests_total{job="prometheus"}[5m]
```

### Operators

Prometheus's query language supports basic logical and arithmetic operators. For operations between two instant vectors, the [matching behavior](https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching) can be modified.

-   binary arithmetic operators are defined between scalar/scalar, vector/scalar, and vector/vector value pairs. (`+, -, *, /, %, ^`)
-   comparison operators are defined between scalar/scalar, vector/scalar, and vector/vector value pairs. By default they filter. Their behaviour can be modified by providing `bool` after the operator, which will return `0` or `1` for the value rather than filtering (`==, !=, >, >=`)
-   operations between vectors attempt to find a matching element in the right-hand side vector for each entry in the left-hand side.
    -   when applying operators Prometheus attempts to find a matching element in both vectors by labels. Can ignore labels to get matches
    -   `method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m`
-   aggregation operators can be used to aggregate the elements of a single instant vector, resulting in a new vector of fewer elements with aggregated values: (`sum`, `min`, `max`, `avg`, `count`, `topk`, `quantile`)
    -   if the metric `http_requests_total` had time series that fan out by `application`, `instance`, and `group` labels, we could calculate the total number of seen HTTP requests per application and group over all instances via: `sum without (instance) (http_requests_total)`
-   `rate` calculates per second increment over a time-period (takes in a range vector and outputs an instant vector)
-   <https://prometheus.io/docs/prometheus/latest/querying/functions>

### Examples

**Return all time series with the metric `http_requests_total`:**

```plain
http_requests_total
```

**Return all time series with the metric `http_requests_total` and the given `job` and `handler` labels:**

```plain
http_requests_total{job="apiserver", handler="/api/comments"}
```

**Return a whole range of time (in this case 5 minutes) for the same vector, making it a range vector (not graphable):**

```plain
http_requests_total{job="apiserver", handler="/api/comments"}[5m]
```

**Return the 5-minute rate of the `http_requests_total` metric for the past 30 minutes, with a resolution of 1 minute:**

```plain
rate(http_requests_total[5m])[30m:1m]
```

**Return sum of 5-minute rate over all instances by job name:**

```plain
sum by (job) (
  rate(http_requests_total[5m])
)
```

**Return the unused memory in MiB for every instance:**

If we have two different metrics with the same dimensional labels, we can apply binary operators to them and elements on both sides with the same label set will get matched and propagated to the output:

```plain
(instance_memory_limit_bytes - instance_memory_usage_bytes) / 1024 / 1024
```

The same expression, but summed by application, could be written like this:

```plain
sum by (app, proc) (
  instance_memory_limit_bytes - instance_memory_usage_bytes
) / 1024 / 1024
```

**Return the top 3 CPU users grouped by application (`app`) and process type (`proc`):**

```plain
topk(3, sum by (app, proc) (rate(instance_cpu_time_ns[5m])))
```

**Return the count of the total number of running instances per application:**

```plain
count by (app) (instance_cpu_time_ns)
```

## Recording Rules

Prometheus supports two types of rules which may be configured and then evaluated at regular intervals: recording rules and alerting rules. To include rules in Prometheus, create a file containing the necessary rule statements and have Prometheus load the file via the `rule_files` field in the config.

-   recording rules allow you to precompute frequently needed or computationally expensive expressions and save their result as a new set of time series
-   querying the precomputed result will then often be much faster than executing the original expression every time it is needed
-   this is especially useful for dashboards which need to query the same expression repeatedly every time they refresh

Recording and alerting rules exist in a rule group. Rules within a group are run sequentially at a regular interval, with the same evaluation time. The names of recording rules must be valid metric names. The names of alerting rules must be valid label values.

### Rule Definitions

-   Recording rules should be of the general form `level:metric:operation`
    -   **level** = the aggregation level of the metric and labels of the rule output
    -   **metric** = the metric name under evaluation
    -   **operation** = list of operations applied to the metric under evaluation

```yaml
# rules/myrules.yml
groups:
    - name: example # The name of the group. Must be unique within a file.
      rules:
          - record: job:http_inprogress_requests:sum # The name of the time series to output to. Must be a valid metric name.
            # The PromQL expression to evaluate. Every evaluation cycle this is
            # evaluated at the current time, and the result recorded as a new set of
            # time series with the metric name as given by 'record'.
            expr: sum by (job) (http_inprogress_requests)
```

The rule file paths need to be added into the main Prometheus config to be executed periodically as defined by `evaluation_interval`

```yaml
rule_files:
    - "rules/myrules.yml"
```

### Checking Rule Syntax

To quickly check whether a rule file is syntactically correct without starting a Prometheus server, you can use Prometheus's `promtool` command-line utility tool:

`promtool check rules /path/to/example.rules.yml`

## HTTP API

Allows direct endpoints for querying instant/range queries, viewing targets, configuration etc

-   `localhost:9090/api/v1/query?query=up`
-   `localhost:9090/api/v1/query?query=http_requests_total[1m]`
-   `localhost:9090/api/v1/targets?state=active` / `localhost:9090/api/v1/rules?type=alert`

<https://prometheus.io/docs/prometheus/latest/querying/api/>
