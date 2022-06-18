---
layout: post
title: Kafka Recommendations & Best Practices
tags:
  - kafka
  - command
  - cli
  - topic
  - producer
  - consumer
  - consumer group
  - zookeeper
typora-root-url: ../..
---

Most Kafka design and configuration choices are use case dependent and come with trade-offs, so it's hard to define any best usage rules. However, below are some points of interest and general recommendations based on previous experience that you may want to consider or look more into:

## Topics

- Ensure all topics have a consistent naming scheme. If using a shared cluster, prefix with the system name. Kafka can have issues when there are both underscores _ and periods . in the topic name, so choose one or the other as a common separator
- Determine the number of partitions the new topic should have, taking into account:
  - volume of data - more partitions increases the upper-bound on the number of concurrent consumers processing messages
  - it is easier to add new partitions to an existing topic in the future rather than remove partitions if there are too many already
  - during a rebalance, all consumers will stop and be reassigned new partitions. If there are too many partitions/consumers then this can be slower process to coordinate and redistribute and may cause additional stress on the cluster. Don't set the partition count too high as there are side effects
  - as a general rule of thumb, keep the number of partitions an easily and evenly divisible by your expected number of consumers e.g having 12 partitions will evenly spread load across 3 or 4 consumers subscribed to it and processing messages in parallel
- How long data on the topics should be kept in the cluster (retention) - as small as possible. For shared clusters this will be a max of 7 days in order to support the cluster being completely rebuilt over the weekend. Retention can be set on a per topic basis as needed
- The topic replication factor will be likely be determined by the existing cluster configuration to ensure message durability. Likly will be set to 3 or 4 to survive broker failure or complete data centre failover
- Don't set compression at the topic level, prefer at the producer level. Look into other topic level configuration properties such as compaction as needed depending on specific use case
- What the key of the topic will be depending on partitioning and source data - remember all messages with the same key will be sent to the same partition
- What the value POJO should be - see below for more details

## Messages

- When creating a key, take into account data skew on the broker and partitions - ideally there will be even distribution between them all. Otherwise you may see issues if one consumer is processing all the messages with the others sitting idle
  - if not key is provided, the cluster will use a round-robin approach to distribute messages - this is better than having a bad custom key
  - the key should contain data elements with high cardinality to increase the probability of good data distribution (based on hashes)
  - Do not include variable data elements in keys (e.g version numbers). The overall id is a good key property for example as it means all versions of that event will be sent to the same partition. There is no ordering guarantee across partitions so if you need one message to be processed after another, they must have the same key
- Use strongly typed keys and values on topic - don't use Strings as its harder to manage deserialization and versioning
- Consider using a message wrapper to add metadata fields to all messages (or use headers)
  - adds a number of fields to better support tracking across services source instance, cause, origin, run/batch UUID and unique message id's
- If the topic is to consume very high volumes of data, then try to avoid unnecessary duplication or large objects which are not needed to improve throughput and network traffic
- Consider changes to the format of the messages over time e.g adding or removing fields
  - this has to be synced between producers/consumers to ensure the messages can still be deserialized properly
  - it is also a reason to use short retention periods and consumers will not need to process very old messages
  - consider looking into Avro and schema registry to better manage this aspect

## Producers

- If your project is Spring based, use the provided KafkaTemplate classs which wraps the Apache producer and makes config/sending messages much easier
- Specify acks=all in the producer configuration to force the partition leader to replicate messages to a certain number of followers (depending on min-insync replias) before ack'ing the messages and received
  - this will increase latency between sending and receiving ack, but otherwise you may lose messages if a broker goes down and the message has not been replicated yet
  - KafkaTemplate operates in an sync manner by default, so call .get() on returned future to block until ack is complete
- Enable the idempotence property on the producer to esnure that the same message doesn't get sent twice under some error conditions (adds tracking ids to the message to prevent duplicates). Note that depending on use case and consumer behaviour this may not be needed. Be aware that this also overrides other producer configs such as retries (infinite) and max inflight requests
- Performance at the producer level is mainly driven by efficient micro-batching of messages
  - batch size and linger.ms can set to delay sending until the producer has more messages to include in the batch
  - this is a balancing act as increasing these will add higher latency to message delivery, but give more overall throughput
- Consider setting compression on the producer to improve throughout and reduce load on storage, but might not be suitable for very low latency apps as introduces a decompression cost on the consumer side. It is not recommended to add this to the topic level which will cause the cluster to perform compression on the broker instead of the producer

## Consumers

- If your project is Spring based, use the KafkaListener and KafkaListenerContainerFactory classes to greatly simplify the otherwise complicated setup of the core Apache consumer classes and adds inegrations with other aspects of Spring Boot
  - makes setting deserializers, concurrency, error handling etc easier
- Kafka only provides ordering guarantees for messages in the same partition, so if your consumer needs to see one message after another, they must have the same key
  - even then rebalancing *may* cause disturbances in this behaviour
- To scale consumption, place consumers into he same consumer group to evenly spread partitions between instances
- If the same listener is subscribed to multiple topics, it is recommended to place them in different consumer groups, otherwise rebalancing will impact processing in all when not necessary
- Improve throughput by configuring min bytes and max wait times for batching - again this is a balancing act of throughput vs latency
- Ensure all consumers are idempotent (able to consume the same message multiple times without any negative impact)
  - Kafka has a number of ways to try and combat duplication, but it is strongly recommended to place checks in all consumers as this is still never guaranteed from Kafka
  - Sending offset acknowledgements are a balancing act between at-least-once and at-most-once processing - the former being preferable in most cases
- Ensure that consumer lag (difference in rate of production vs consumption) is properly traced via monitoring tools to detect general issues or slow consumers
- By default Kafka will auto-commit offsets as a specific interval, but this alone introduces risk of data loss (commits ofsset before fully processed vs processed before committing offset and then crashing)
  - Is is strongly recommended to disable auto commit and manage offset commits at the application level
  - You can process on message at a time and then sync commit the offset after processing is complete -safest approach but more network traffic as less offset batching
  - Process the messages as a batch in your service code and then sync commit all the offsets at the end - more throughput but more chance of duplicated effort
  - By making all consumers idempotent, these concerns are removed entirely as long as the offsets are committed after processing is completed

## Error Handling

- Ensure that all exception scenarios are thought about and handled (deserialization, delivery failure, listener failure, broker down, timeouts, transient issues, error topic publish etc) and alerts are raised when necessary (but ideally the system should be able to recover itself from many of these problems)
- Avoid creating configuration/consumers/producers manually, use factory methods in a core lib which should come setup already for error handling in a a consistent manner

### Kafka Spring Consumer

- There are a number of techniques to handle errors when consuming topics depending on use case - pausing the consumer, raise alerts and continue, error topics etc
- A common approach is for each topic to have associated error topics (suffix .error app exceptions and .deserr for deserialization exceptions). Messages are automatically forwarded to these error topics when corresponding exceptions are thrown
  - Error topics always have just one topic to maintain message order over time
  - If the deserializer fails to convert your JSON to the corresponding POJO, the message will be placed immediately on the .deserr error topic and an alert raised (no point in retries)
  - Key and value will be String versions of the original record to cover format issues
  - Headers of the message include specific exception details including the origin offset and partition and a stacktrace - very useful for debugging
  - If error topic publication fails, the record is not acknowledged and the container paused + an alert is generated - signals the cluster is likely having issues
  - Take into account the multiple consumer groups may be processing messages from the same topic - include the consumer group name in the error topic name
- If message fails during processing within a listener (general app exception)
  - Can retry processing multiple times to cover transient issues - be careful about duplicating work
  - If an exception is still thrown when processing the same message (app level issue such as db connection) then the message(s) are placed on the .error topic and the offsets are committed to continue consuming the next messages
  - Headers of the message include exception details and stacktrace just like deserialization errors
- Ensure monitoring is in place to detach any depth on error topics
  - Likely resolution will be to reflow the messages after the underlying issue resolved - making consumer idempotent is very important here
- Ensure transactionality is setup to rollback other changes (db) if the consumer fails

### Kafka Spring Producer

- All producers require ack from all broker replicas before committing. By default this is set to 'all' meaning that before proceeding a number of brokers need to ack all the messages - as defined by the min-insync-replicas config property at the broker level
- If using KafkaTemplate make sure to call .get() on the future to block until the ack is received (by default it will continue immediately and you may not know about the issue). With this behaviour an exception will be thrown as you would expect if the production fails
- Ensure transactionality is setup to rollback changes if errors occur - pullback messages sent to other topics etc

### Kafka Streams

- Similarly to general consumer error handling, but as Kafka streams spolits work into a number of parallel stream tasks, is a lot harder to manage centrally
- Specify a deserialization exception handler - similar to Spring consumers, to publish messages onto error topic automatically if a record cannot be deserialized. Stream will move onto the next record
  - Create all Serde's using builders to setup deserializers consistently and ensure handlers are included by default
- All potential exceptions must be handled within each stream task (map/filter etc) - if an exception is not caught it will crash the streams thread and force a rebalancing
  - default exception handlers will just log the error and continue
  - could wrap all operations in try/catch and handle accordingly
  - or could wrap the base KStream/KTable etc to give consistent error handling and avoid duplicated code - 'protected' versions
- If streams thread does do for some reason, an uncaught exception handler should be provided to generate a critiical alert. If all the streams threads die (potentially by all trying to process the same message), nothing will be consumed at all and the app will be stalled
- Ensure monitoring is in place to ensure that the streams app as a whole is live and healthy

## Misc

- Although during local development you could directly connect to the main dev cluster, it is recommended for devs to instead create and use their own local clusters
  - this gives a lot more control during dev for debugging/modifying properties without impacting others
  - any new topic can be created or invalid messages sent without also being seent/consumed by the main services and causing unnecessary exceptions and alerts
- Maintain clear documentation behind the reasons behind each topic and the config behind them - volume expectations etc
- Create a Kafka topology diagram showing clearly the path(s) taken by messages between components - this is especially important the more services and topics are created
- Create documentation showing exactly what keys/values are put onto each topic - useful for debugging and new joiners
- Ensure all Kafka configuration for new producers/consumers is done in a single central place (likely a shared lib) to avoid duplication and chance of issues if placed everywhere
  - list of broker hosts per environment, properties for Kerberos and auth etc
  - maintain consistency in configuration for all producers/consumers regardless of where they are used - serialization, error handling, transactions etc
- Ensure you have the appropriate disaster recovery plans in place to either recover from the cluster being down or failover
  - Kafka is not meant as a data store, although unlikely plan for all the data to be lost at any point
  - Determine how the application should react if the cluster is not available - brokers being down or transient network issues

