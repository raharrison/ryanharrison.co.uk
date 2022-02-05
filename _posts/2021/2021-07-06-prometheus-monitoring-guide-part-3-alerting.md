---
layout: post
title: Prometheus Monitoring Guide Part 3 - Alerting
tags:
    - prometheus
    - monitoring
    - alert
    - receiver
    - rule
    - alertmanager
    - routing
    - metrics
    - metric
    - labels
typora-root-url: ../..
---

-   [Part 1 - Installation and Instrumentation]({{ site.baseurl }}{% post_url 2021/2021-04-05-prometheus-monitoring-guide-part-1-install-instrumentation %})
-   [Part 2 - PromQL and Recording Rules]({{ site.baseurl }}{% post_url 2021/2021-04-18-prometheus-monitoring-guide-part-2-promql-recording-rules %})
-   [Part 4 - Pushgateway and Blackbox Exporter]({{ site.baseurl }}{% post_url 2022/2022-02-05-prometheus-monitoring-guide-part-4-pushgateway-blackbox-exporter %})

## Alerting

Alerting rules allow you to define alert conditions based on Prometheus expression language expressions and to send notifications about firing alerts to an external service. Whenever the alert expression results in one or more vector elements at a given point in time, the alert counts as active for these elements' label sets.

Alerting rules are configured in Prometheus in the same way as recording rules:

{% raw %}

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

{% endraw %}

-   **for** - wait for a certain duration between first encountering a new expression output vector element and counting an alert as firing for this element
-   **labels** - specifying a set of additional labels to be attached to the alert
-   **annotations** = informational labels that can be used to store longer additional information such as alert descriptions or runbook links

```yaml
rule_files:
    - "rules/alert_rules.yml"
```

Alerts can be monitored through the "Alerts" tab in the Prometheus dashboard (which ones are active, pending, firing etc)

### AlertManager

-   another layer is needed to add summarization, notification rate limiting, silencing and alert dependencies on top of the simple alert definitions
-   Prometheus is configured to periodically send information about alert states to an `Alertmanager` instance, which then takes care of dispatching the right notifications
    -   takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, PagerDuty
-   provided as a single Go binary from <https://prometheus.io/download/> so can be executed directly
    -   `./alertmanager` - by default runs on port `9093`
    -   or with Docker `docker run --name alertmanager -d -p 9093:9093 quay.io/prometheus/alertmanager`
    -   takes configuration from `alertmanager.yml` file in same directory

```yaml
alerting:
    alertmanagers:
        - static_configs:
              - targets:
                    - "localhost:9093"
```

#### Sending Email Notifications

-   `alertmanager.yml` file defines routing tree defining how an alert should be managed. If no labels are matching, default root is used

```yaml
route:
    receiver: admin

receivers:
    - name: admin
      email_configs:
          - to: "example@gmail.com"
            from: "example@gmail.com"
            smarthost: smtp.gmail.com:587
            auth_username: "example@gmail.com"
            auth_password: "abcdefghijklmnop"
```

### Routing Tree

-   Grouping categorizes alerts of similar nature into a single notification. This is especially useful during larger outages when many systems fail at once and hundreds to thousands of alerts may be firing simultaneously.
    -   configure Alertmanager to group alerts by their cluster and alertname so it sends a single compact notification.
-   Inhibition is the concept of suppressing notifications for certain alerts if certain other alerts are already firing
-   Silences are a way to simply mute alerts for a given time. A silence is configured based on matchers, just like the routing tree. Incoming alerts are checked whether they match all the equality or regular expression matchers of an active silence. If they do, no notifications will be sent out for that alert. Configured through the UI. If time based, add condition to the underlying rule instead
-   By default each alert running through the routing tree will halt after matching against the first receiver at the same level - can use `continue` clause

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
          severity: "critical"
      target_match:
          severity: "warning" # mute warning alert if critical alert already raised in same app and category
      equal: ["app_type", "category"]

receivers:
    - name: linux-team-lead
      email_configs:
          - to: "example@gmail.com"
```

### Checking Tree Syntax

To quickly check whether an alerting route treefile is syntactically correct without starting the AlertManager instance, you can use the `amtool` utility:

`amtool check-config alertmanager.yml`

Or <https://prometheus.io/webtools/alerting/routing-tree-editor/> can be used to visualize a routing tree
