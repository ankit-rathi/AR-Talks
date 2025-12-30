## 8. Transactions

Based on the sources provided, the chapter "Safeguarding Data: The Mechanics of Database Transactions" offers several critical insights into how data systems manage faults and concurrency. Here are the key takeaways:

### 1. Transactions as a Safety Abstraction
Transactions are a programming model designed to **simplify error handling** by grouping multiple reads and writes into a single logical unit. Rather than forcing application developers to account for every possible partial failure—such as a crash halfway through a series of writes—the database provides an **"all-or-nothing" guarantee**. If a fault occurs, the transaction is simply aborted and can be safely retried.

### 2. The Nuances of ACID
While the ACID acronym (Atomicity, Consistency, Isolation, Durability) provides a high-level framework for reliability, its practical implementation varies significantly between databases.
*   **Atomicity:** Better understood as **"abortability,"** it ensures that all writes in a transaction are discarded if a failure occurs, preventing partially updated data.
*   **Consistency:** Unlike the other three, consistency is largely an **application responsibility**; the application must define its transactions correctly to preserve data invariants.
*   **Isolation:** This ensures that concurrent transactions do not interfere with one another. While formal isolation (serializability) means transactions appear to run one after another, many databases use weaker isolation levels for better performance.
*   **Durability:** No single technique provides an absolute guarantee against data loss; rather, it involves **risk-reduction techniques** such as writing to disk, replication, and backups.

### 3. Concurrency Control and Race Conditions
Concurrency issues, or race conditions, occur when multiple clients access the same records simultaneously. The sources identify several critical anomalies that occur under weak isolation:
*   **Dirty Reads/Writes:** A client seeing or overwriting uncommitted data.
*   **Read Skew (Nonrepeatable Reads):** A client seeing different parts of the database at different points in time. This is typically solved using **Snapshot Isolation** and Multi-Version Concurrency Control (MVCC).
*   **Lost Updates:** Occur during read-modify-write cycles where one client's changes are overwritten by another's. These can be prevented by atomic write operations, explicit locking, or automatic detection.
*   **Write Skew and Phantoms:** A subtler race condition where a transaction makes a decision based on a premise that is no longer true by the time the write is committed.

### 4. Implementing Serializability
To provide the strongest isolation guarantee—**Serializability**—databases generally use one of three methods:
*   **Actual Serial Execution:** Literally executing transactions one at a time on a single thread. This is efficient for in-memory data and short transactions but limited to the throughput of a single CPU core.
*   **Two-Phase Locking (2PL):** A pessimistic approach where writers block readers and readers block writers. While common for decades, it often suffers from poor performance and unstable latencies.
*   **Serializable Snapshot Isolation (SSI):** A modern, optimistic approach that allows transactions to proceed without blocking, only aborting them if a serialization conflict is detected at the commit point.

### 5. Distributed Transactions and Atomic Commit
When a transaction involves multiple nodes, the system faces the **"atomic commitment problem"**—ensuring that all nodes either commit or abort together. 
*   **Two-Phase Commit (2PC):** The classic algorithm for this, involving a **coordinator** that asks participants to "prepare" before issuing a final "commit". 
*   **The In-Doubt State:** If the coordinator fails after participants have voted "yes," those participants become "uncertain" or "in-doubt," holding onto locks indefinitely until the coordinator recovers.
*   **Heterogeneous vs. Internal:** While XA transactions (spanning different technologies) often cause operational "grief," database-internal distributed transactions can be highly optimized and reliable by using consensus protocols to replicate the coordinator.

***

**Analogy for Understanding 2PC:**
Think of Two-Phase Commit like a **wedding ceremony**. The "coordinator" (the officiant) asks the "participants" (the couple) if they consent. Once both say "I do" (the **prepare** phase), they have made a promise they cannot unilaterally take back. Even if someone faints before the officiant pronounces them married (the **commit** phase), they remain in a state of "doubt" until they can confirm the official decision was recorded.


### Chapter Summary

Transactions are an abstraction layer that allows an application to pretend that certain concurrency problems and certain kinds of hardware and software faults don’t exist. A large class of errors is reduced down to a simple transaction abort, and the application just needs to try again.

In this chapter we saw many examples of problems that transactions help prevent. Not all applications are susceptible to all those problems: an application with very simple access patterns, such as reading and writing only a single record, can probably manage without transactions. However, for more complex access patterns, transactions can hugely reduce the number of potential error cases you need to think about.

Without transactions, various error scenarios (processes crashing, network interruptions, power outages, disk full, unexpected concurrency, etc.) mean that data can become inconsistent in various ways. For example, denormalized data can easily go out of sync with the source data. Without transactions, it becomes very difficult to reason about the effects that complex interacting accesses can have on the database.

In this chapter, we went particularly deep into the topic of concurrency control. We discussed several widely used isolation levels, in particular read committed, snapshot isolation (sometimes called repeatable read), and serializable. We characterized those isolation levels by discussing various examples of race conditions, summarized in Table 8-1.

#### Dirty reads
One client reads another client’s writes before they have been committed. The read committed isolation level and stronger levels prevent dirty reads.

#### Dirty writes
One client overwrites data that another client has written, but not yet committed. Almost all transaction implementations prevent dirty writes.

#### Read skew
A client sees different parts of the database at different points in time. Some cases of read skew are also known as nonrepeatable reads. This issue is most commonly prevented with snapshot isolation, which allows a transaction to read from a consistent snapshot corresponding to one particular point in time. It is usually implemented with multi-version concurrency control (MVCC).

#### Lost updates
Two clients concurrently perform a read-modify-write cycle. One overwrites the other’s write without incorporating its changes, so data is lost. Some implementations of snapshot isolation prevent this anomaly automatically, while others require a manual lock (SELECT FOR UPDATE).

#### Write skew
A transaction reads something, makes a decision based on the value it saw, and writes the decision to the database. However, by the time the write is made, the premise of the decision is no longer true. Only serializable isolation prevents this anomaly.

#### Phantom reads
A transaction reads objects that match some search condition. Another client makes a write that affects the results of that search. Snapshot isolation prevents straightforward phantom reads, but phantoms in the context of write skew require special treatment, such as index-range locks.

Weak isolation levels protect against some of those anomalies but leave you, the application developer, to handle others manually (e.g., using explicit locking). Only serializable isolation protects against all of these issues. We discussed three different approaches to implementing serializable transactions:

#### Literally executing transactions in a serial order
If you can make each transaction very fast to execute (typically by using stored procedures), and the transaction throughput is low enough to process on a single CPU core or can be sharded, this is a simple and effective option.

#### Two-phase locking
For decades this has been the standard way of implementing serializability, but many applications avoid using it because of its poor performance.

#### Serializable snapshot isolation (SSI)
A comparatively new algorithm that avoids most of the downsides of the previous approaches. It uses an optimistic approach, allowing transactions to proceed without blocking. When a transaction wants to commit, it is checked, and it is aborted if the execution was not serializable.

Finally, we examined how to achieve atomicity when a transaction is distributed across multiple nodes, using two-phase commit. If those nodes are all running the same database software, distributed transactions can work quite well, but across different storage technologies (using XA transactions), 2PC is problematic: it is very sensitive to faults in the coordinator and the application code driving the transaction, and it interacts poorly with concurrency control mechanisms. Fortunately, idempotence can ensure exactly-once semantics without requiring atomic commit across different storage technologies, and we will see more on this in later chapters.

The examples in this chapter used a relational data model. However, as discussed in “The need for multi-object transactions”, transactions are a valuable database feature, no matter which data model is used.
