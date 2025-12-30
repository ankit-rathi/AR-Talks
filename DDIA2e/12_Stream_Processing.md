This chapter, **"Stream Processing,"** explores the transition from processing fixed, finite datasets (batch processing) to managing **unbounded data** that arrives incrementally over time. 

The key takeaways from the sources are as follows:

### 1. From Batch to Stream Processing
While batch processing assumes data is "complete" and finite, real-world data is often **unbounded**, as users and machines continue to produce events indefinitely. Stream processing abandons fixed time slices to process every event as it happens, reducing the delay between an event's occurrence and its reflection in the output. An **event** is the fundamental unit of a stream: a small, self-contained, and **immutable object** detailing something that happened at a specific point in time.

### 2. Evolution of Messaging Systems
Messaging systems notify consumers about new events, evolving from direct communication to centralized brokers.
*   **AMQP/JMS-style Brokers:** These treat messages as transient; once a message is acknowledged, it is deleted. This is ideal for task queues where order is less critical and old messages don't need to be reread.
*   **Log-based Brokers:** Systems like Apache Kafka treat a stream as an **append-only log on disk**. This allows multiple consumers to read the same stream independently without deleting data, enabling the **replaying of old messages** to recover from errors or build new views.

### 3. The Duality of State and Streams
A core insight of the chapter is that **mutable state and append-only logs are two sides of the same coin**. 
*   **State as an Integral:** The current application state can be viewed as the "integration" of an event stream over time.
*   **Stream as a Derivative:** A change stream is the "derivative" of the state over time.
*   **Change Data Capture (CDC):** This process observes changes in a database and extracts them as a stream, allowing you to keep derived systems like caches or search indexes in sync with the "system of record".

### 4. Reasoning About Time
Stream processing introduces significant complexity regarding time, specifically the distinction between **event time** (when the event actually occurred) and **processing time** (when the event was handled by the system). 
*   **Lags and Artifacts:** Network delays or system restarts can cause a backlog of events, leading to inaccurate spikes if windowing is based solely on processing time.
*   **Window Types:** Analytics are often computed over time windows, such as **tumbling** (fixed length, non-overlapping), **hopping** (fixed length, overlapping), **sliding** (interval between events), or **session** (defined by periods of activity).

### 5. Stream Joins
Joins in a streaming context are challenging because new data arrives continuously. The sources identify three types:
*   **Stream-stream joins:** Matching related events from two streams within a specific time window (e.g., matching a "search" event with a "click" event).
*   **Stream-table joins:** Enriching an activity stream with data from a database (e.g., adding user profile info to a click event).
*   **Table-table joins:** Joining two database changelogs to maintain a materialized view (e.g., a social media timeline updated by both "posts" and "follows" streams).

### 6. Fault Tolerance and Exactly-Once Semantics
Because streams are infinite, you cannot simply restart a job from the beginning if it fails. Stream processors use several techniques to achieve **exactly-once semantics** (the effect is as if every message was processed exactly once):
*   **Microbatching and Checkpointing:** Breaking the stream into small blocks or taking periodic state snapshots to allow for recovery.
*   **Idempotence:** Ensuring that performing an operation multiple times has the same effect as performing it once (e.g., using Kafka offsets to ignore duplicate writes).
*   **Atomic Commits:** Internal transactions that ensure state changes and outgoing messages happen together or not at all.

***

**Analogy for Time in Stream Processing:**
The sources suggest thinking of the **Star Wars movies**. If you watch them in the order they were released (processing time), you see Episode IV before Episode I. However, if you want to understand the narrative chronology (event time), you must reorder them. Stream processors must be specifically designed to handle this "narrative" order, even when events arrive out of sequence.

### Chapter Summary
In this chapter we have discussed event streams, what purposes they serve, and how to process them. In some ways, stream processing is very much like the batch processing we discussed in Chapter 11, but done continuously on unbounded (never-ending) streams rather than on a fixed-size input [84]. From this perspective, message brokers and event logs serve as the streaming equivalent of a filesystem.

We spent some time comparing two types of message brokers:

#### AMQP/JMS-style message broker
The broker assigns individual messages to consumers, and consumers acknowledge individual messages when they have been successfully processed. Messages are deleted from the broker once they have been acknowledged. This approach is appropriate as an asynchronous form of RPC (see also “Event-Driven Architectures”), for example in a task queue, where the exact order of message processing is not important and where there is no need to go back and read old messages again after they have been processed.

#### Log-based message broker
The broker assigns all messages in a shard to the same consumer node, and always delivers messages in the same order. Parallelism is achieved through sharding, and consumers track their progress by checkpointing the offset of the last message they have processed. The broker retains messages on disk, so it is possible to jump back and reread old messages if necessary.

The log-based approach has similarities to the replication logs found in databases (see Chapter 6) and log-structured storage engines (see Chapter 4). It is also a form of consensus, as we saw in Chapter 10. We saw that this approach is especially appropriate for stream processing systems that consume input streams and generate derived state or derived output streams.

In terms of where streams come from, we discussed several possibilities: user activity events, sensors providing periodic readings, and data feeds (e.g., market data in finance) are naturally represented as streams. We saw that it can also be useful to think of the writes to a database as a stream: we can capture the changelog—i.e., the history of all changes made to a database—either implicitly through change data capture or explicitly through event sourcing. Log compaction allows the stream to retain a full copy of the contents of a database.

Representing databases as streams opens up powerful opportunities for integrating systems. You can keep derived data systems such as search indexes, caches, and analytics systems continually up to date by consuming the log of changes and applying them to the derived system. You can even build fresh views onto existing data by starting from scratch and consuming the log of changes from the beginning all the way to the present.

The facilities for maintaining state as streams and replaying messages are also the basis for the techniques that enable stream joins and fault tolerance in various stream processing frameworks. We discussed several purposes of stream processing, including searching for event patterns (complex event processing), computing windowed aggregations (stream analytics), and keeping derived data systems up to date (materialized views).

We then discussed the difficulties of reasoning about time in a stream processor, including the distinction between processing time and event timestamps, and the problem of dealing with straggler events that arrive after you thought your window was complete.

We distinguished three types of joins that may appear in stream processes:

#### Stream-stream joins
Both input streams consist of activity events, and the join operator searches for related events that occur within some window of time. For example, it may match two actions taken by the same user within 30 minutes of each other. The two join inputs may in fact be the same stream (a self-join) if you want to find related events within that one stream.

#### Stream-table joins
One input stream consists of activity events, while the other is a database changelog. The changelog keeps a local copy of the database up to date. For each activity event, the join operator queries the database and outputs an enriched activity event.

#### Table-table joins
Both input streams are database changelogs. In this case, every change on one side is joined with the latest state of the other side. The result is a stream of changes to the materialized view of the join between the two tables.

Finally, we discussed techniques for achieving fault tolerance and exactly-once semantics in a stream processor. As with batch processing, we need to discard the partial output of any failed tasks. However, since a stream process is long-running and produces output continuously, we can’t simply discard all output. Instead, a finer-grained recovery mechanism can be used, based on microbatching, checkpointing, transactions, or idempotent writes.
