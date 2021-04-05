---
layout: post
title: Prometheus Monitoring Cheat Sheet
tags:
  - prometheus
  - monitoring
  - metrics
  - metric
  - time
  - series
  - labels
typora-root-url: ..
---

An open-source systems monitoring and alerting toolkit. Now a standalone open source project and maintained independently of any company. Analyse how your applications and infrastructure is performing based on the metrics they publish. Particularly suitable for large distributed systems with ephemeral instances.

- metrics are stored in a `multi-dimensional` data model instead of `hierarchical`, where each measurement consists of a name and a number of key/value pairs
  - `http.server.requests.count(uri="/endpoint", method="GET") 12` instead of `http.server.requests.GET.endpoint=12`
  - backed by it's own custom time-series database built specifically for metrics
- provides it's own query language `PromQL` as a read-only and flexible query language for aggregation on time series data
- no reliance on distributed storage; single server nodes are autonomous
- time series collection happens via a pull model over HTTP
- targets are discovered via service discovery or static configuration
- multiple modes of graphing and dashboarding support

- Alternative to `Graphite`, `InfluxDB`
- Ecosystem provides a number of pre-built `exporters` that expose metrics ready for Prometheus to scrape

## Architecture

![Prometheus Architecture](/images/2021/prometheus_architecture.png)

- main Prometheus server consists of a time series database storing each of the captured measurements
  - alongside a scraper which pulls samples from external applications, hosts, platforms
  - and an HTTP server which allows operations to be performed on the tsdb (e.g querying by PromQL)
- Prometheus is a single-instance component; all data is stored on local node storage
  - if you need to scale, recommendation is to spin up multiple separate Prometheus instances with different/replicated targets
- operates in a `pull` model, whereby Prometheus is setup to periodically scrape the metrics from all target application instances
  - therefore has to know about the location of all active instances via `service discovery`
  - more easily tell if a target is down, can manually go to a target and inspect its health with a web browser
  - application itself has no knowledge of Prometheus apart from an endpoint exposing the latest metrics snapshot (`/metrics`)
- the `pull` model can be problematic for short-lived/batch operations which may not be alive long enough to be scraped
  - `Pushgateway` component can be used as a middle-man - gets pushed metrics from jobs and forwards them to Prometheus
- service discovery integration into `Kubernetes`, `AWS`, `Azure` to understand current landscape of all target nodes
- after metrics are scraped and stored in tsdb, can be made available to users through web UI/Grafana/API
- `AlertManager` component can be used with a set of rules querying the metrics to generate system alerts
  - performs de-duplication of alerts, throttling, silences etc
  - forwards to email, `PagerDuty`, `Slack` etc

## Installation

- provided as a single Go binary from <https://prometheus.io/download/> so can be executed directly

  - `./prometheus`
  - by default looks for `prometheus.yml` config file in the same directory (by default will only scrape Prometheus itself)

- Prometheus Web UI available at `http://localhost:9090`

  - allows you to view current targets, configuration and run queries. For more complex visualizations use `Grafana`

- or can be executed through `Docker`

  - ```
    docker run -p 9090:9090 -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
    ```

## Configuration

- all Prometheus config provided in `prometheus.yml` file
  - docs at <https://prometheus.io/docs/prometheus/latest/configuration/configuration/>
- Prometheus can reload its configuration at runtime. If the new configuration is not well-formed, the changes will not be applied
  - reload is triggered by sending a `SIGHUP` to the Prometheus process (`kill -HUP <pid>`)
  - or sending an `HTTP POST` request to the `/-/reload` endpoint when the `--web.enable-lifecycle` flag is enabled

```yaml
global: # applied to all targets unless overridden
  scrape_interval: 15s # how often to scrape each target
  evaluation_interval: 15s # how often to evaluate predefined rules

scrape_configs: # a set of jobs denoting where to scrape metrics from
  - job_name: "prometheus" # a group of targets, also added as a label to each measurement
    metrics_path: '/metrics' # default
    static_configs: # a hardcoded host/port or could be service discovery
      - targets: ["localhost:9090"] # uses metrics path to pull metrics, by default http
```

### Service Discovery

- `static_configs` does not scale to more dynamic environments where instances are added/removed frequently
- Prometheus can integrate with service discovery mechanisms to automatically update it's view of of running instances
  - when new instances are added Prometheus will begin scraping, when lost from discovery the time series will also be removed
  - built-in integrations with `Consul`, `Azure`, `AWS` or file based if custom mechanism required
- `JSON`/`YAML` file can be published by the platform specifying all targets to scrape from. Prometheus uses it to automatically update targets

![Prometheus Service Discovery](/images/2021/prometheus_service_discovery.png)

```yaml
- job_name: 'myapp'
  file_sd_configs:
    refresh_interval: 5m # default
    - files:
      - file_sd.yml
```

Where the published file `file_sd.json` contains all the current live targets and any attached labels:

```json
[
  {
    "targets": [
      "<host>"
    ],
    "labels": {
      "<labelname>": "<labelvalue>"
    }
  }
]
```

### Relabelling

Prometheus needs to know what to scrape, and that's where service discovery and `relabel_configs` come in. Relabel configs allow you to select [which targets you want scraped](https://www.robustperception.io/automatically-monitoring-ec2-instances/), and [what the target labels will be](https://www.robustperception.io/finding-consul-services-to-monitor-with-prometheus/). So if you want to say scrape this type of machine but not that one, use `relabel_configs`.

`metric_relabel_configs` by contrast are applied after the scrape has happened, but before the data is ingested by the storage system. So if there are some [expensive metrics you want to drop](https://www.robustperception.io/dropping-metrics-at-scrape-time-with-prometheus/), or labels coming from the scrape itself (e.g. from the `/metrics` page) that you want to manipulate that's where  `metric_relabel_configs` applies.

So as a simple rule of thumb: `relabel_config` happens before the scrape, `metric_relabel_configs` happens after the scrape

```yaml
  relabel_configs:
  - source_labels: [__meta_kubernetes_service_label_app]
    regex: nginx
    action: keep
  - source_labels: [__meta_kubernetes_endpoint_port_name]
    regex: web
    action: keep
  - source_labels: [__meta_ec2_public_ip] # rewrite private ip to public from service discovery
    regex: '(.*)'
    replacement: '${1}:9100'
    target_label: __address__    
```

You can perform the following `action` operations:

- `keep`: Keep a matched target or series, drop all others
- `drop`: Drop a matched target or series, keep all others
- `replace`: Replace or rename a matched label with a new one defined by the `target_label` and `replacement` parameters
- `labelkeep`: Match the `regex` against all label names, drop all labels that don’t match (ignores `source_labels` and applies to all label names)
- `labeldrop`: Match the `regex` against all label names, drop all labels that match (ignores `source_labels` and applies to all label names)

``metric_relabel_configs`` can be used to drop unnecessary time-series before ingestion:

```yaml
- job_name: cadvisor
  metric_relabel_configs:
  - source_labels: [container_label_JenkinsId]
    regex: '.+'
    action: drop
  - source_labels: [__name__]
    regex: '(container_tasks_state|container_memory_failures_total)'
    action: drop
```

<https://grafana.com/docs/grafana-cloud/billing-and-usage/prometheus/usage-reduction/>

## Instrumentation

- there are two ways in which application metrics can be exposed for Prometheus
  - use a client library directly in the application to create and expose a Prometheus endpoint (usually `/metrics`)
  - use an intermediate proxy `exporter` instance instrumenting the target application and converting to the Prometheus metrics format

```
# HELP http_requests_total The total number of HTTP requests.
# TYPE http_requests_total counter
http_requests_total{method="post",code="200"} 1027 1395066363000
http_requests_total{method="post",code="400"}    3 1395066363000

# Minimalistic line:
metric_without_timestamp_and_labels 12.47

# A histogram, which has a pretty complex representation in the text format:
# HELP http_request_duration_seconds A histogram of the request duration.
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.05"} 24054
http_request_duration_seconds_bucket{le="0.1"} 33444
http_request_duration_seconds_bucket{le="0.2"} 100392
http_request_duration_seconds_bucket{le="0.5"} 129389
http_request_duration_seconds_bucket{le="1"} 133988
http_request_duration_seconds_bucket{le="+Inf"} 144320
http_request_duration_seconds_sum 53423
http_request_duration_seconds_count 144320

# Finally a summary, which has a complex representation, too:
# HELP rpc_duration_seconds A summary of the RPC duration in seconds.
# TYPE rpc_duration_seconds summary
rpc_duration_seconds{quantile="0.01"} 3102
rpc_duration_seconds{quantile="0.05"} 3272
rpc_duration_seconds{quantile="0.5"} 4773
rpc_duration_seconds{quantile="0.9"} 9001
rpc_duration_seconds{quantile="0.99"} 76656
rpc_duration_seconds_sum 1.7560473e+07
rpc_duration_seconds_count 2693
```

### Conventions and Practices

- metrics names should start with a letter can be followed with any number of letters, numbers and underscores
- metrics must have unique names, client libraries should report an error if you try to register the same one twice
- should have a suffix describing the unit, in plural form (e.g `_bytes` or `_total`)
- should represent the same logical thing-being-measured across all label dimensions
- every unique combination of key-value label pairs represents a new time series, which can dramatically increase the amount of data stored. Do not use labels to store dimensions with high cardinality (many different label values), such as user IDs, email addresses, or other unbounded sets of values

### Exporters

There are a number of libraries and servers which help in exporting existing metrics from third-party systems as Prometheus metrics. This is useful for cases where it is not feasible to instrument a given system with Prometheus metrics directly (Linux kernel) as cannot modify source etc

- <https://prometheus.io/docs/instrumenting/exporters/>
- an `exporter` is a separate process dedicated entirely to pulling metrics from a target system and exposing them as Prometheus metrics
  - "proxy service" converting the target interface into one that can be scraped by Prometheus
- Common exporters (some official):
  - [Node Exporter](https://prometheus.io/docs/instrumenting/exporters/) - hardware and OS metrics exposed by Unix kernels, CPU load, memory, I/O, network
  - [MySQL Expoter](https://github.com/prometheus/mysqld_exporter) - database metrics, queries ran, timings, pool sizes
  - [Blackbox Exporter](https://github.com/prometheus/blackbox_exporter) - probing of endpoints over HTTP, DNS, TCP, ICMP
  - Kafka, Kafka Lag, Nginx, Postgres, Jenkins, AWS, Graphite, JMX

- for cases which you have access to modify the application code, instrumentation must be added in order to add Prometheus metrics
  - can use existing application frameworks to expose default common metrics (`Spring Actuator`)
  - use the client libraries to add custom metrics to be exposed (Go, Java, Python, Ruby)
- other metrics libraries offer a facade over the definition of metrics and allow pluggable Prometheus exporter to be added instead (`Micrometer`)
  - don't have to use Prometheus client library directly for increased flexibility in overall monitoring solution

#### Blackbox Exporter

A probing exporter, allowing you to monitor network endpoints - upon probing it returns detailed metrics about the underlying requests.

- for use when you have no knowledge of system internals, to measure response times, DNS resolution timing, check availability of endpoints etc

![Prometheus Blackbox Exporter](/images/2021/prometheus_blackbox.png)

- provided as a single Go binary from <https://github.com/prometheus/blackbox_exporter> so can be executed directly
  - `./blackbox_exporter` - by default runs on port `9115`
  - or with Docker `docker run --rm -d -p 9115:9115 -v pwd:/config prom/blackbox-exporter:master --config.file=/config/blackbox.yml`
- to retrieve metrics in Prometheus, target the `probe` endpoint directly (which performs and measures the request)
- modules used to perform the network request (as defined in the probe URL) are defined in the `blackbox.yml` config file (HTTP, DNS, SSH)
  - <https://github.com/prometheus/blackbox_exporter/blob/master/example.yml>

**Perform HTTP Request and Find Content in Response Body**

```yaml
# blackbox.yml
http_find_prom:
  prober: http
  http:
    preferred_ip_protocol: ip4 # by default ipv6
    fail_if_body_not_matches_regexp:
    - "monitoring"
```

`http://localhost:9115/probe?target=prometheus.io&module=http_find_prom` -- `probe_success = 1`

**Perform TCP Probe**

`http://localhost:9115/probe?target=localhost:8000&module=tcp_connect`

**Perform DNS Probe**

```yaml
dns_google:
  prober: dns
  dns:
    transport_protocol: "tcp"
    preferred_ip_protocol: ip4
    query_name: "www.google.com"
```

`http://localhost:9115/probe?target=8.8.8.8&module=dns_google`

**Scraping to Prometheus**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]  # Look for a HTTP 200 response.
    static_configs:
      - targets:
        - http://prometheus.io    # Target to probe with http
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target # save current target address into temp param
      - source_labels: [__param_target]
        target_label: instance # move current address to instance label
      - target_label: __address__
        replacement: 127.0.0.1:9115 # redirect address
```

### Metric Types

The client libraries offer four core metric types. These are currently only differentiated in the client libraries (to enable APIs tailored to the usage of the specific types) and in the wire protocol. The Prometheus server does not yet make use of the type information and flattens all data into untyped time series.

#### Counter

- a cumulative metric that represents a single [monotonically increasing counter](https://en.wikipedia.org/wiki/Monotonic_function) whose value can only increase or be reset to zero on restart
- for example, you can use a counter to represent the number of requests served, tasks completed, or errors
- do not use a counter to expose a value that can decrease. For example, do not use a counter for the number of currently running processes; instead use a gauge

#### Gauge

- a metric that represents a single numerical value that can arbitrarily go up and down
- gauges are typically used for measured values like temperatures or current memory usage, but also "counts" that can go up and down, like the number of concurrent requests

#### Histogram

- samples observations (usually things like request durations or response sizes) and counts them in configurable buckets. It also provides a sum of all observed values
- a histogram with a base metric name of `<basename>` exposes multiple time series during a scrape:
  - cumulative counters for the observation buckets, exposed as `<basename>_bucket{le="<upper inclusive bound>"}`
  - the **total sum** of all observed values, exposed as `<basename>_sum`
  - the **count** of events that have been observed, exposed as `<basename>_count` (identical to `<basename>_bucket{le="+Inf"}` above)

- use the [`histogram_quantile()` function](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile) to calculate quantiles from histograms or even aggregations of histograms across instances
- when operating on buckets, remember that the histogram is [cumulative](https://en.wikipedia.org/wiki/Histogram#Cumulative_histogram)

#### Summary

- similar to a histogram, a summary samples observations (usually things like request durations and response sizes). While it also provides a total count of observations and a sum of all observed values, it calculates configurable quantiles over a sliding time window
- a summary with a base metric name of `<basename>` exposes multiple time series during a scrape:
  - streaming **φ-quantiles** (0 ≤ φ ≤ 1) of observed events, exposed as `<basename>{quantile="<φ>"}`
  - the **total sum** of all observed values, exposed as `<basename>_sum`
  - the **count** of events that have been observed, exposed as `<basename>_count`
- <https://prometheus.io/docs/practices/histograms/>
  - if you need to aggregate, choose histograms.
  - otherwise, choose a histogram if you have an idea of the range and distribution of values that will be observed. Choose a summary if you need an accurate quantile, no matter what the range and distribution of the values is.

## PromQL

Prometheus provides a functional query language called PromQL (Prometheus Query Language) that lets the user select and aggregate time series data in real time. The result of an expression can either be shown as a graph, viewed as tabular data in Prometheus's expression browser, or consumed by external systems via the HTTP API.

### Data Types

An expression or sub-expression can evaluate to one of four types:

- **Instant vector** - a set of time series containing a single sample for each time series, all sharing the same timestamp (`prometheus_http_requests_total`)
- **Range vector** - a set of time series containing a range of data points over time for each time series (`prometheus_http_requests_total[5m]`)
- **Scalar** - a simple numeric floating point value

Depending on the use-case (e.g. when graphing vs. displaying the output of an expression), only some of these types are legal as the result from a user-specified expression. For example, an expression that returns an instant vector is the only type that can be directly graphed.

### Selectors and Matchers

In the simplest form, only a metric name is specified. This results in an instant vector containing elements for all time series that have this metric name:

```
http_requests_total
```

It is possible to filter these time series further by appending a comma separated list of label matchers in curly braces (`{}`).

This example selects only those time series with the `http_requests_total` metric name that also have the `job` label set to `prometheus` and their `group` label set to `canary`:

```
http_requests_total{job="prometheus",group="canary"}
```

- `=` - select labels that are exactly equal to the provided string
- `!=` - select labels that are not equal to the provided string
- `=~` - select labels that regex-match the provided string
- `!~` - select labels that do not regex-match the provided string

Range vector literals work like instant vector literals, except that they select a range of samples back from the current instant. A time duration is appended in square brackets (`[]`) at the end of a vector selector to specify how far back in time values should be fetched for each resulting range vector element.

In this example, we select all the values we have recorded within the last 5 minutes for all time series that have the metric name `http_requests_total` and a `job` label set to `prometheus`:

```
http_requests_total{job="prometheus"}[5m]
```

### Operators

Prometheus's query language supports basic logical and arithmetic operators. For operations between two instant vectors, the [matching behavior](https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching) can be modified.

- binary arithmetic operators are defined between scalar/scalar, vector/scalar, and vector/vector value pairs. (`+, -, *, /, %, ^`)
- comparison operators are defined between scalar/scalar, vector/scalar, and vector/vector value pairs. By default they filter. Their behaviour can be modified by providing `bool` after the operator, which will return `0` or `1` for the value rather than filtering (`==, !=, >, >=`)

- operations between vectors attempt to find a matching element in the right-hand side vector for each entry in the left-hand side.
  - when applying operators Prometheus attempts to find a matching element in both vectors by labels. Can ignore labels to get matches
  - `method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m`
- aggregation operators can be used to aggregate the elements of a single instant vector, resulting in a new vector of fewer elements with aggregated values: (`sum`, `min`, `max`, `avg`, `count`, `topk`, `quantile`)
  - if the metric `http_requests_total` had time series that fan out by `application`, `instance`, and `group` labels, we could calculate the total number of seen HTTP requests per application and group over all instances via: `sum without (instance) (http_requests_total)`
- `rate` calculates per second increment over a time-period (takes in a range vector and outputs an instant vector)
- <https://prometheus.io/docs/prometheus/latest/querying/functions>

### Examples

**Return all time series with the metric `http_requests_total`:**

```
http_requests_total
```

**Return all time series with the metric `http_requests_total` and the given `job` and `handler` labels:**

```
http_requests_total{job="apiserver", handler="/api/comments"}
```

**Return a whole range of time (in this case 5 minutes) for the same vector, making it a range vector (not graphable):**

```
http_requests_total{job="apiserver", handler="/api/comments"}[5m]
```

**Return the 5-minute rate of the `http_requests_total` metric for the past 30 minutes, with a resolution of 1 minute:**

```
rate(http_requests_total[5m])[30m:1m]
```

**Return sum of 5-minute rate over all instances by job name:**

```
sum by (job) (
  rate(http_requests_total[5m])
)
```

**Return the unused memory in MiB for every instance:**

If we have two different metrics with the same dimensional labels, we can apply binary operators to them and elements on both sides with the same label set will get matched and propagated to the output:

```
(instance_memory_limit_bytes - instance_memory_usage_bytes) / 1024 / 1024
```

The same expression, but summed by application, could be written like this:

```
sum by (app, proc) (
  instance_memory_limit_bytes - instance_memory_usage_bytes
) / 1024 / 1024
```

**Return the top 3 CPU users grouped by application (`app`) and process type (`proc`):**

```
topk(3, sum by (app, proc) (rate(instance_cpu_time_ns[5m])))
```

**Return the count of the total number of running instances per application:**

```
count by (app) (instance_cpu_time_ns)
```

## Recording Rules

Prometheus supports two types of rules which may be configured and then evaluated at regular intervals: recording rules and alerting rules. To include rules in Prometheus, create a file containing the necessary rule statements and have Prometheus load the file via the `rule_files` field in the config.

- recording rules allow you to precompute frequently needed or computationally expensive expressions and save their result as a new set of time series
- querying the precomputed result will then often be much faster than executing the original expression every time it is needed
- this is especially useful for dashboards which need to query the same expression repeatedly every time they refresh

Recording and alerting rules exist in a rule group. Rules within a group are run sequentially at a regular interval, with the same evaluation time. The names of recording rules must be valid metric names. The names of alerting rules must be valid label values.

### Rule Definitions

- Recording rules should be of the general form `level:metric:operation`
  - **level** = the aggregation level of the metric and labels of the rule output
  - **metric** = the metric name under evaluation
  - **operation** = list of operations applied to the metric under evaluation

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

## Alerting

Alerting rules allow you to define alert conditions based on Prometheus expression language expressions and to send notifications about firing alerts to an external service. Whenever the alert expression results in one or more vector elements at a given point in time, the alert counts as active for these elements' label sets.

Alerting rules are configured in Prometheus in the same way as recording rules:

```yaml
# rules/alert_rules.yml
groups:
- name: example
  rules:
  # Alert for any instance that has a median request latency >1s.
  - alert: APIHighRequestLatency
    expr: api_http_request_latencies_second{quantile="0.5"} > 1
    for: 10m
    labels:
      severity: page
    annotations:
      summary: "High request latency on {{ $labels.instance }}"
      description: "{{ $labels.instance }} has a median request latency above 1s (current value: {{ $value }}s)"
```

- **for** - wait for a certain duration between first encountering a new expression output vector element and counting an alert as firing for this element
- **labels** - specifying a set of additional labels to be attached to the alert
- **annotations** = informational labels that can be used to store longer additional information such as alert descriptions or runbook links

```yaml
rule_files:
  - "rules/alert_rules.yml"
```

Alerts can be monitored through the "Alerts" tab in the Prometheus dashboard (which ones are active, pending, firing etc)

### AlertManager

- another layer is needed to add summarization, notification rate limiting, silencing and alert dependencies on top of the simple alert definitions 
- Prometheus is configured to periodically send information about alert states to an `Alertmanager` instance, which then takes care of dispatching the right notifications
  - takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, PagerDuty
- provided as a single Go binary from <https://prometheus.io/download/> so can be executed directly
  - `./alertmanager` - by default runs on port `9093`
  - or with Docker `docker run --name alertmanager -d -p 9093:9093 quay.io/prometheus/alertmanager`
  - takes configuration from `alertmanager.yml` file in same directory

```yaml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      - 'localhost:9093'
```

**Sending Email Notifications**

- `alertmanager.yml` file defines routing tree defining how an alert should be managed. If no labels are matching, default root is used

```yaml
route:
  receiver: admin

receivers:
- name: admin
  email_configs:
  - to: 'example@gmail.com'
    from: 'example@gmail.com'
    smarthost: smtp.gmail.com:587
    auth_username: 'example@gmail.com'
    auth_password: 'abcdefghijklmnop'
```

### Routing Tree

- Grouping categorizes alerts of similar nature into a single notification. This is especially useful during larger outages when many systems fail at once and hundreds to thousands of alerts may be firing simultaneously.
  -  configure Alertmanager to group alerts by their cluster and alertname so it sends a single compact notification.
- Inhibition is the concept of suppressing notifications for certain alerts if certain other alerts are already firing
- Silences are a way to simply mute alerts for a given time. A silence is configured based on matchers, just like the routing tree. Incoming alerts are checked whether they match all the equality or regular expression matchers of an active silence. If they do, no notifications will be sent out for that alert. Configured through the UI. If time based, add condition to the underlying rule instead
- By default each alert running through the routing tree will halt after matching against the first receiver at the same level - can use `continue` clause

```yaml
route:
  receiver: admin # root fallback
  group_wait: 2m # how long to wait for other alerts in a group to fire before notifying (after initial)
  group_interval: 10s # how long to wait before sending a notification about new alerts added to an already firing group
  repeat_interval: 30m # how long to wait before sending a notification again if it has already been sent
  routes:
  - match_re:
      app_type: (linux|windows) # custom label specified in the rule definition file
    receiver: ss-admin # fallback receiver
    group_by: [severity] # group all alerts on a label to send compact notification
    routes:
    - match:
        app_type: linux # match on more specific label
      receiver: linux-teamlead # target more specific receiver
      routes: # nested routes on different labels
      - match:
          severity: critical
        receiver: delivery-manager
        continue: true
      - match:
          severity: warning
        receiver: linux-teamlead

  - match_re:
      app_type: (python|go)
    receiver: pec-admin # fallback receiver
    routes:
    - match:
        app_type: python
      receiver: python-team-admin # fallback receiver
      routes:
      - match:
          severity: critical
        receiver: python-team-manager
      - match:
          severity: warning
        receiver: python-team-lead

inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning' # mute warning alert if critical alert already raised in same app and category
  equal: ['app_type', 'category']

receivers:
- name: linux-team-lead
  email_configs:
  - to: 'example@gmail.com'
```

### Checking Tree Syntax

To quickly check whether an alerting route treefile is syntactically correct without starting the AlertManager instance, you can use the `amtool` utility:

`amtool check-config alertmanager.yml`

Or <https://prometheus.io/webtools/alerting/routing-tree-editor/> can be used to visualize a routing tree

## HTTP API

Allows direct endpoints for querying instant/range queries, viewing targets, configuration etc

- `localhost:9090/api/v1/query?query=up`
- `localhost:9090/api/v1/query?query=http_requests_total[1m]`
- `localhost:9090/api/v1/targets?state=active` / `localhost:9090/api/v1/rules?type=alert` 

<https://prometheus.io/docs/prometheus/latest/querying/api/>

## Pushgateway

The `pull` approach doesn't work for ephemeral jobs which don't run for long enough for Prometheus to scrape them. `Pushgateway` is a metrics cache for service-level batch jobs. Used to handle the exposition of metrics that have ben pushed from batch/cron jobs. If a `Pushgateway` instance collecting metrics from many targets goes down, all metrics will be lost.

![Prometheus Pushgateway](/images/2021/prometheus_pushgateway.png)

- provided as a single Go binary from <https://prometheus.io/download/> so can be executed directly
  - `./pushgateway` - by default runs on port `9091`
  - or with Docker `docker run -d -p 9091:9091 prom/pushgateway`
- need to add `Pushgateway` as scrape target in Prometheus

```yaml
- job_name: "pushgateway"
  honor_labels: true # instrumentation labels to override target labels
  static_configs:
    - targets: ["localhost:9091"]
```

- metrics can sent from the job instance to `Pushgateway` by sending an HTTP `POST` request
  - `echo "some_metric 3.14" | curl --data-binary @- http://pushgateway.example.org:9091/metrics/job/some_job`
- or Prometheus client libraries should have a feature to push the registered metrics to a `Pushgateway`
  - <https://prometheus.github.io/client_java/io/prometheus/client/exporter/PushGateway.html>

