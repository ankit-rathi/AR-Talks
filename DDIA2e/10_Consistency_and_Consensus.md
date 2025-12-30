This chapter, **"Consistency and Consensus,"** focuses on how distributed systems achieve strong guarantees—specifically linearizability—despite the physical unreliability and partial failures discussed in previous chapters.

The key takeaways from the sources are as follows:

### 1. Linearizability: The Illusion of a Single Copy
Linearizability is the strongest consistency model in common use, designed to make a replicated system behave as if there were only **one copy of the data** and all operations on it were **atomic**.
*   **Recency Guarantee:** It ensures that once a write is successful, all subsequent reads must see that new value.
*   **vs. Serializability:** While serializability is an *isolation* property for transactions (handling multiple objects), linearizability is a *consistency* property for individual objects (registers).
*   **The Cost of Speed:** Linearizability is expensive; its response time is inevitably high because it is proportional to the uncertainty of network delays.

### 2. Ordering and Distributed ID Generation
Maintaining order is a central challenge in distributed consistency.
*   **Logical Clocks:** Since physical clocks drift, systems use **logical clocks** (like Lamport timestamps) to count events rather than seconds.
*   **Causality vs. Linearizability:** Lamport clocks provide a total ordering consistent with **causality** (if A happened before B, A’s ID is lower), but they do not provide linearizability because they cannot ensure a value is the most up-to-date across nodes that haven't communicated.
*   **Hybrid Logical Clocks (HLCs):** These combine physical time-of-day clocks with Lamport ordering, allowing for a "best of both worlds" approach used in databases like CockroachDB.

### 3. Consensus: The Fundamental Distributed Problem
Consensus involves getting multiple nodes to agree on a single value, which is necessary for leader election, uniqueness constraints, and atomic transaction commits.
*   **Core Properties:** A valid consensus algorithm must satisfy **Uniform Agreement** (no two nodes decide differently), **Integrity** (no node decides twice), **Validity** (the decided value was proposed), and **Termination** (nodes eventually reach a decision).
*   **Equivalence:** Many distributed problems—such as Total Order Broadcast (shared logs), linearizable Compare-and-Set (CAS), and distributed locking—are formally equivalent to consensus; if you can solve one, you can solve them all.
*   **The FLP Result:** Theoretically, consensus cannot be guaranteed to terminate in an asynchronous system if a node might crash, but in practice, using timeouts and randomized numbers makes it solvable.

### 4. Implementing Fault-Tolerant Systems
Commonly used algorithms like **Raft, Paxos, and Zab** provide consensus-based replication.
*   **Epochs and Quorums:** These algorithms use **epoch numbers** (to ensure a unique leader per term) and **quorums** (requiring a majority of nodes for any decision) to prevent "split-brain" scenarios where two nodes believe they are the leader simultaneously.
*   **Coordination Services:** Tools like **ZooKeeper and etcd** outsource the complexity of consensus, providing higher-level features like **fencing tokens**, leases, and change notifications to help manage distributed configurations and work allocation.

### 5. The CAP Trade-off
The choice between consistency (linearizability) and availability is inevitable during a **network partition**.
*   **CP (Consistent):** The system returns an error or waits, choosing to be unavailable rather than serving stale/inconsistent data.
*   **AP (Available):** The system allows independent processing on replicas, but results are not linearizable.
*   The sources note that the CAP theorem is often misunderstood and limited in scope, as it only considers one consistency model and one type of fault.

***

**Analogy for Total Order Broadcast (Consensus):**
Think of a consensus-based shared log as a **court stenographer**. Even if multiple lawyers (nodes) are shouting arguments at the same time, the stenographer ensures that every word is recorded in a **single, definitive sequence**. Every person who reads the transcript later sees the exact same order of events, ensuring that the "truth" of the trial is consistent for everyone, regardless of when or where they read it.

### Chapter Summary

In this chapter we examined the topic of strong consistency in fault-tolerant systems: what it is, and how to achieve it. We looked in depth at linearizability, a popular formalization of strong consistency: it means that replicated data appears as though there were only a single copy, and all operations act on it atomically. We saw that linearizability is useful when you need some data to be up-to-date when you read it, or if you need to resolve a race condition (e.g. if multiple nodes are concurrently trying to do the same thing, such as creating files with the same name).

Although linearizability is appealing because it is easy to understand—it makes a database behave like a variable in a single-threaded program—it has the downside of being slow, especially in environments with large network delays. Many replication algorithms don’t guarantee linearizability, even though it superficially might seem like they might provide strong consistency.

Next, we applied the concept of linearizability in the context of ID generators. A single-node auto-incrementing counter is linearizable, but not fault-tolerant. Many distributed ID generation schemes don’t guarantee that the IDs are ordered consistently with the order in which the events actually happened. Logical clocks such as Lamport clocks and hybrid logical clocks provide ordering that is consistent with causality, but no linearizability.

This led us to consensus algorithms, which make it possible to implement fault-tolerant, linearizable replication. Linearizability means the system must behave as if there was only one copy of the data, and all operations happened one at a time to that single copy, in a well-defined order. Consensus provides this by making a group of nodes agree on a single sequence of operations, even if messages are delayed or some nodes fail. That sequence of operations makes a distributed system behave as if there was only one node processing operations in order, even though it is actually a group of nodes working together.

The classic formulation of consensus involves deciding on a single value in such a way that all nodes agree on what was decided, and such that they can’t change their mind. A wide range of problems are actually reducible to consensus and are equivalent to each other (i.e., if you have a solution for one of them, you can transform it into a solution for all of the others). Such equivalent problems include:

#### Linearizable compare-and-set operation
The register needs to atomically decide whether to set its value, based on whether its current value equals the parameter given in the operation.

#### Locks and leases
When several clients are concurrently trying to grab a lock or lease, the lock decides which one successfully acquired it.

#### Uniqueness constraints
When several transactions concurrently try to create conflicting records with the same key, the constraint must decide which one to allow and which should fail with a constraint violation.

#### Shared logs
When several nodes concurrently want to append entries to a log, the log decides in which order they are appended. Total order broadcast is also equivalent.

#### Atomic transaction commit
The database nodes involved in a distributed transaction must all decide the same way whether to commit or abort the transaction.

#### Linearizable fetch-and-add operation
This operation can be used to implement an ID generator. Several nodes can concurrently invoke the operation, and it decides the order in which they increment the counter. This case actually solves consensus only between two nodes, while the others work for any number of nodes.

All of these are straightforward if you only have a single node, or if you are willing to assign the decision-making capability to a single node. This is what happens in a single-leader database: all the power to make decisions is vested in the leader, which is why such databases are able to provide linearizable operations, uniqueness constraints, a replication log, and more.

However, if that single leader fails, or if a network interruption makes the leader unreachable, such a system becomes unable to make any progress until a human performs a manual failover. Widely-used consensus algorithms like Raft and Paxos are essentially single-leader replication with built-in automatic leader election and failover if the current leader fails.

Consensus algorithms are carefully designed to ensure that no committed writes are lost during a failover, and that the system cannot get into a split brain state in which multiple nodes are accepting writes. This requires that every write, and every linearizable read, is confirmed by a quorum (typically a majority) of nodes. This can be expensive, especially across geographic regions, but it is unavoidable if you want the strong consistency and fault tolerance that consensus provides.

Coordination services like ZooKeeper and etcd are also built on top of consensus algorithms. They provide locks, leases, failure detection, and change notification features that are useful for managing the state of distributed applications. If you find yourself wanting to do one of those things that is reducible to consensus, and you want it to be fault-tolerant, it is advisable to use a coordination service. It won’t guarantee that you will get it right, but it will probably help.

Consensus algorithms are complicated and subtle, but they are supported by a rich body of theory that has been developed since the 1980s. This theory makes it possible to build systems that can tolerate all the faults that we discussed in Chapter 9, and still ensure that your data is not corrupted. This is an amazing achievement, and the references at the end of this chapter feature some of the highlights of this work.

Nevertheless, consensus is not always the right tool: in some systems, the strong consistency properties it provides are not needed, and it is better to have weaker consistency with higher availability and better performance. In these cases, it is common to use leaderless or multi-leader replication, which we previously discussed in Chapter 6. The logical clocks that we discussed in this chapter are helpful in that context.
