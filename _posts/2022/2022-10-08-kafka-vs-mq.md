---
layout: post
title: Kafka vs MQ
tags:
  - kafka
  - mq
  - rabbitmq
  - differences
  - usages
typora-root-url: ../..
---

Some quick high levels notes on Kafka vs MQ. This is a question that often gets asked by folks already who are familiar with traditional queues (IBM MQ/RabbitMQ etc) when they are introduced to the world of Kafka:

### Kafka High Level Uses

- Event input buffer for data analytics/ML
- Event driven microservices
- Bridge to cloud-native apps

### ActiveMQ

- Consumer gets pushed certain number of message by broker depending on prefetch
- Consumer chunks through them, on each ack, broker deletes from data store
- Produce pushes single message, consumer acks, deletes, gone 1to1
- Conforms to standard `JMS` based messaging

#### Topics in MQ

- Subscribers only receive messages published while it is connected
- Or durable where client can disconnect and still receive messages after
- In MQ can block brokers, fill data stores
- Each consumer gets copy of the message unless composite destinations/message groups
- Hard to create dynamic consumers or change the topology

### Kafka

- each group gets message, but in group only one consumer
- consumers defines the interaction (pull)
	- partitions assignment, offset resets, consumer group
- consumer can apply backpressure or rebalance


- Can't go back through the log
- Difficult to load balance effectively
- Completing consumers vs one partition still processing whilst other is blocked
- Hard to change topology or increase number of queues
- Hard to handle slow/failing consumers
- not predefining functionality to behave like a queue or topic, defined by consumers
	- introduce new consumer groups adhoc to change how destination functions
	- single consumer group = queue
	- multi consumer groups = topic
	- what offset to start from
- one consumer group can fail and replay whilst another succeeds
- MQ always queue one out at a time - not depending on consumers, Kafka behaviour changes on number of partitions/consumers

### Useful Video Links

- <https://www.youtube.com/watch?v=6yG2myKcMQE>
- <https://www.youtube.com/watch?v=sjDnqrnnYNM>
- <https://www.youtube.com/watch?v=Sa3Csx6zFcs>
- <https://www.youtube.com/watch?v=7Faly8jORIw>
