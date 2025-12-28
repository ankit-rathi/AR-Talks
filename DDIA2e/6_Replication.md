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
