The primary focus of this chapter is **replication**: keeping a copy of the same data on multiple machines connected via a network. While simple in theory, replication is challenging because it requires managing data changes across nodes while navigating trade-offs between **availability, latency, and consistency**.

The following are the key takeaways regarding strategies and trade-offs in data replication:

### 1. Core Motivations for Replication
Replication serves four main purposes in distributed systems:
*   **High Availability:** Keeping the system running even if individual machines, zones, or entire regions fail.
*   **Latency Reduction:** Placing data geographically closer to users to speed up interactions.
*   **Scalability:** Increasing read throughput by distributing queries across multiple replicas.
*   **Disconnected Operation:** Allowing applications to function during network interruptions (common in mobile or local-first apps).

### 2. Three Major Replication Architectures
The sources identify three families of algorithms used to propagate changes between nodes:
*   **Single-Leader Replication:** The most common approach where all writes are sent to one designated leader. The leader sends a stream of changes to followers, who apply them in the same order.
*   **Multi-Leader Replication:** Multiple nodes can accept writes, which they then replicate to each other. This is ideal for **multi-region deployments** or **offline-first applications**, as it allows writes to happen locally even during network partitions.
*   **Leaderless Replication:** No node acts as a leader; clients (or coordinators) send writes and reads to several replicas in parallel. This architecture, popularized by **Dynamo-style** databases, is highly resilient to "gray failures" where a node is slow but not completely down.

### 3. Synchronous vs. Asynchronous Replication
A critical design choice is whether the leader waits for replicas to confirm a write before reporting success to the client:
*   **Synchronous:** Guarantees the follower is up-to-date, but the system blocks if that follower becomes unavailable.
*   **Asynchronous:** Offers better performance and availability, but introduces **replication lag** and the risk that a write may be lost if the leader fails before the change is propagated.

### 4. Handling Replication Lag Anomalies
In eventually consistent systems (where followers may be behind the leader), three specific guarantees are necessary to prevent user confusion:
*   **Read-after-write consistency:** Users must always see updates they submitted themselves, even if they are read from a replica.
*   **Monotonic reads:** Ensures that if a user makes several reads in sequence, they will not see time "go backward" by hitting a stale replica after seeing a fresh one.
*   **Consistent prefix reads:** Guarantees that if a sequence of writes happens in a certain order, followers see them in that same causal order (e.g., a question must appear before its answer).

### 5. Conflict Resolution
In multi-leader and leaderless systems, concurrent writes to the same record can cause conflicts. Strategies for resolution include:
*   **Last Write Wins (LWW):** Forcing an order based on timestamps and discarding "older" writes, which risks data loss.
*   **Automatic Merging:** Using data structures like **CRDTs** (Conflict-free Replicated Data Types) or **Operational Transformation** (OT) to converge concurrent changes into a consistent state without manual intervention.
*   **Version Vectors:** Using per-replica version numbers to distinguish between overwrites and truly concurrent writes.

### 6. Quorum Consistency in Leaderless Systems
Leaderless systems use **quorums** to ensure data reliability. If there are $n$ replicas, a write must be confirmed by $w$ nodes and a read must query $r$ nodes. As long as **$w + r > n$**, the system expects to find at least one up-to-date node during a read.

Managing replication is like **maintaining a shared team notebook across different offices**. Single-leader replication is like having one person take all the notes and photocoping them for everyone else. Multi-leader is like every office having their own notebook and trying to merge the handwritten edits at the end of the week—inevitably, you'll need a clear set of rules to decide what to do when two people have scribbled over the same line.


### Chapter Summary

In this chapter we looked at the issue of replication. Replication can serve several purposes:

#### High availability
Keeping the system running, even when one machine (or several machines, a zone, or even an entire region) goes down

#### Durability
Ensuring you don’t lose data, even if a whole machine (or even an entire region) fails permanently

#### Disconnected operation
Allowing an application to continue working when there is a network interruption

#### Latency
Placing data geographically close to users, so that users can interact with it faster

#### Scalability
Being able to handle a higher volume of reads than a single machine could handle, by performing reads on replicas

Despite being a simple goal—keeping a copy of the same data on several machines—replication turns out to be a remarkably tricky problem. It requires carefully thinking about concurrency, all the things that can go wrong, and how to deal with the consequences of those faults. At a minimum, we need to deal with unavailable nodes and network interruptions (and that’s not even considering the more insidious kinds of fault, such as silent data corruption due to software bugs or hardware errors).

We discussed three main approaches to replication:

#### Single-leader replication
Clients send all writes to a single node (the leader), which sends a stream of data change events to the other replicas (followers). Reads can be performed on any replica, but reads from followers might be stale.

#### Multi-leader replication
Clients send each write to one of several leader nodes, any of which can accept writes. The leaders send streams of data change events to each other and to any follower nodes.

#### Leaderless replication
Clients send each write to several nodes, and read from several nodes in parallel in order to detect and correct nodes with stale data.

Each approach has advantages and disadvantages. Single-leader replication is popular because it is fairly easy to understand and it offers strong consistency. Multi-leader and leaderless replication can be more robust in the presence of faulty nodes, network interruptions, and latency spikes—at the cost of requiring conflict resolution and providing weaker consistency guarantees.

Replication can be synchronous or asynchronous, which has a profound effect on the system behavior when there is a fault. Although asynchronous replication can be fast when the system is running smoothly, it’s important to figure out what happens when replication lag increases and servers fail. If a leader fails and you promote an asynchronously updated follower to be the new leader, recently committed data may be lost.

We looked at some strange effects that can be caused by replication lag, and we discussed a few consistency models which are helpful for deciding how an application should behave under replication lag:

#### Read-after-write consistency
Users should always see data that they submitted themselves.

#### Monotonic reads
After users have seen the data at one point in time, they shouldn’t later see the data from some earlier point in time.

#### Consistent prefix reads
Users should see the data in a state that makes causal sense: for example, seeing a question and its reply in the correct order.

Finally, we discussed how multi-leader and leaderless replication ensure that all replicas eventually converge to a consistent state: by using a version vector or similar algorithm to detect which writes are concurrent, and by using a conflict resolution algorithm such as a CRDT to merge the concurrently written values. Last-write-wins and manual conflict resolution are also possible.

This chapter has assumed that every replica stores a full copy of the whole database, which is unrealistic for large datasets. In the next chapter we will look at sharding, which allows each machine to store only a subset of the data.
