---
layout: post
title: Kafka Command Cheat Sheet
tags:
  - kafka
  - command
  - cheat sheet
  - cli
  - topic
  - producer
  - consumer
  - consumer group
  - zookeeper
typora-root-url: ../..
---

## Environment Variables

**Set path to binaries**

`export JAVA_HOME=/path/to/jdk`

`export PATH=$PATH:/path/to/kafka/common/bin`

**Add Kerberos / SASL config options (if required)**

`export KAFKA_OPTS="-Djava.security.krb5.conf/etc/krb5.conf -Dzookeeper.sasl.client.username=myuser -Djava.security.auth.login.config=/var/tmp/jaas.conf"`

`export KCONFIG=/var/tmp/kafka-client.properties`

Where properties contains:

```properties
security.protocol=SASL_PLAINTEXT
sasl.mechanism=GSSAPI
sasl.kerberos.service.name=myuser
```

**Set common broker lists**

`export KBROKER=host:9092`

`export ZBROKER=host:2181`

---

## Topics

**Create a new topic**

`kafka-topics.sh --zookeeper $ZBROKER --create --replication-factor 3 --partitions 4 --topic topic1`

**Describe an existing topic**

`kafka-topics.sh --zookeeper $ZBROKER --describe --topic topic1`

**List all topics in the cluster**

`kafka-topics.sh --zookeeper $ZBROKER --list`

**Delete a topic**

`kafka-topics.sh --zookeeper $ZBROKER --delete --topic topic1.*`

**Alter topic configuration**

`kafka-configs.sh --zookeeper $ZBROKER --alter --entity-type topics --entity-name topic1 --add-config retention.ms=2592000000`

---

## Consumers

**Run a console consumer starting from the beginning of a topic**

`kafka-console-consumer.sh --bootstrap-server $KBROKER --topic topic1 --from-beginning --consumer-config $KCONFIG`

**Consumer which prints key and value for each message**

`kafka-console-consumer.sh --bootstrap-server $KBROKER --topic topic1 --from-beginning --property print.key=true --property key.separator="|" --consumer-config $KCONFIG`

**Create a consumer inside a specific group**

`kafka-console-consumer.sh --bootstrap-server $KBROKER --topic topic1 --group group1 --consumer-config $KCONFIG`

---

## Producers

**Run a console producer pushing to a specific topic**

`kafka-console-producer.sh --broker-list $KBROKER --topic topic1 --producer-config $KCONFIG`

**Include a specific key in each published message**

`kafka-console-producer.sh --broker-list $KBROKER --topic topic1 --property "parse.key=true" --property "key.separator=|" --producer-config $KCONFIG`

---

## Consumer Groups

**List all consumer groups in the cluster**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --list --command-config $KCONFIG`

**Describe offsets and status of a consumer group**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --describe --command-config $KCONFIG`

**Delete a consumer group**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --delete --command-config $KCONFIG`

**Reset offsets to the beginning for all topics**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --reset-offsets --to-earliest --all-topics --execute --command-config $KCONFIG`

**Reset offsets to beginning for a specific topic**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --reset-offsets --to-earliest --topic topic1 --execute --command-config $KCONFIG`

**Reset offsets to latest**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --reset-offsets --to-latest --all-topics --execute --command-config $KCONFIG`

**Reset offsets to specific value**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --reset-offsets --to-offset 10 --topic topic1:10 --execute --command-config $KCONFIG`

**Reset offsets by a specific shift amount**

`kafka-consumer-groups.sh --bootstrap-server $KBROKER --group group1 --reset-offsets --shift-by -10 --topic topic1 --execute --command-config $KCONFIG`

---

## ACL's

**Grant superuser access to all topics and groups**

`kafka-acls.sh --authorizer-properties zookeeper.connect=$ZBROKER --add --allow-principal User:myuser --operation ALL --topic '*' --group '*' --cluster`

---

## Zookeeper

**Connect to the Zookeeper cluster**

`zookeeper-shell.sh $ZHOST:$ZPORT`

**Set Zookeeper ACL for superuser**

```
ls /
setAcl / sasl:myuser:cdrqa,world:anyone:r
getAcl /
```

<https://medium.com/@TimvanBaarsen/apache-kafka-cli-commands-cheat-sheet-a6f06eac01b>

<https://docs.cloudera.com/documentation/enterprise/6/6.3/topics/kafka_admin_cli.html>

