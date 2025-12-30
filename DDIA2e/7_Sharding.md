This chapter focuses on **sharding** (also known as partitioning), the process of breaking a large dataset into smaller subsets and distributing them across multiple nodes. While the previous chapters in our conversation history covered how to copy data (replication) and how to encode it, this chapter addresses how to **scale** a system horizontally when data volume or write throughput exceeds the capacity of a single machine.

The following are the key takeaways regarding sharding strategies, rebalancing, and routing:

### 1. The Core Goal: Avoiding Skew
The primary objective of sharding is to spread data and query load **evenly** across nodes. If the distribution is unfair, the system suffers from **skew**, where some nodes (known as **hot spots**) handle disproportionately high load while others remain idle. To achieve this balance, systems typically use one of two main sharding schemes:
*   **Key Range Sharding:** Records are sorted and assigned to shards based on contiguous ranges of keys. This is ideal for **range queries**, but it carries a high risk of hot spots if the application frequently writes to nearby keys, such as sequential timestamps.
*   **Hash Sharding:** A hash function is applied to the key to determine its shard, which effectively distributes data more uniformly and relieves hot spots. The trade-off is that **range queries become inefficient**, as related keys are scattered across different shards.

### 2. Strategies for Rebalancing
As a cluster grows or shrinks, shards must be moved between nodes to maintain balance—a process called **rebalancing**. The sources highlight several approaches:
*   **Avoid "Hash Mod N":** Simply taking the hash of a key modulo the number of nodes is inefficient because adding or removing a single node forces nearly all data to be moved.
*   **Fixed Number of Shards:** The system creates many more shards than nodes (e.g., 1,000 shards for 10 nodes). When a node is added, entire shards are moved to it, which is simpler and cheaper than splitting them.
*   **Dynamic Partitioning:** Used in systems like HBase or MongoDB, shards are split into two when they reach a certain size and merged when they become too small. This allows the number of shards to **adapt to the actual volume of data**.

### 3. Challenges with Secondary Indexes
Secondary indexes do not map neatly to shards, leading to two distinct architectural choices:
*   **Local Secondary Indexes (Document-Partitioned):** Each shard maintains its own index for the data it stores. This makes writes fast and simple but makes reads expensive, as the system must perform a **"scatter-gather"** operation, querying every shard to find all matching results.
*   **Global Secondary Indexes (Term-Partitioned):** The index itself is sharded, potentially using a different key than the primary data. While this allows for **efficient reads** from a single shard, it makes writes more complex and slower because updating one record may require updating multiple index shards.

### 4. Request Routing and Coordination
Because data is distributed, the system needs a way to route client requests to the correct node. This is typically handled in one of three ways:
*   **Node Forwarding:** Clients contact any node, which then forwards the request to the correct owner.
*   **Routing Tier:** A specialized, shard-aware load balancer directs traffic.
*   **Client Awareness:** The client application is aware of the sharding scheme and connects directly to the correct node.
Many systems use a **coordination service** like **ZooKeeper** or **etcd** to maintain the authoritative mapping of which shards live on which nodes.

### 5. Sharding for Multitenancy
Sharding is often used in **Software as a Service (SaaS)** environments to isolate customer data. This provides **resource and permission isolation**, ensures regulatory compliance regarding data residency, and allows for **gradual schema rollouts** by updating one tenant's shard at a time.

An analogy for sharding is a **library's shelving system**. Key-range sharding is like an encyclopedia set where volume 1 covers "A-B" and volume 12 covers "T-Z"; it’s easy to find a range of topics, but the "S" volume might be much heavier than "X." Hash sharding is more like assigning books to shelves based on a random-looking ID number; the books are perfectly spread out, but if you want to find all books about "History," you’ll have to check every single shelf in the building.

### Chapter Summary

In this chapter we explored different ways of sharding a large dataset into smaller subsets. Sharding is necessary when you have so much data that storing and processing it on a single machine is no longer feasible.

The goal of sharding is to spread the data and query load evenly across multiple machines, avoiding hot spots (nodes with disproportionately high load). This requires choosing a sharding scheme that is appropriate to your data, and rebalancing the shards when nodes are added to or removed from the cluster.

We discussed two main approaches to sharding:

- Key range sharding, where keys are sorted, and a shard owns all the keys from some minimum up to some maximum. Sorting has the advantage that efficient range queries are possible, but there is a risk of hot spots if the application often accesses keys that are close together in the sorted order.

In this approach, shards are typically rebalanced by splitting the range into two subranges when a shard gets too big.

- Hash sharding, where a hash function is applied to each key, and a shard owns a range of hash values (or another consistent hashing algorithm may be used to map hashes to shards). This method destroys the ordering of keys, making range queries inefficient, but it may distribute load more evenly.

When sharding by hash, it is common to create a fixed number of shards in advance, to assign several shards to each node, and to move entire shards from one node to another when nodes are added or removed. Splitting shards, like with key ranges, is also possible.

It is common to use the first part of the key as the partition key (i.e., to identify the shard), and to sort records within that shard by the rest of the key. That way you can still have efficient range queries among the records with the same partition key.

We also discussed the interaction between sharding and secondary indexes. A secondary index also needs to be sharded, and there are two methods:

- Local secondary indexes, where the secondary indexes are stored in the same shard as the primary key and value. This means that only a single shard needs to be updated on write, but a lookup of the secondary index requires reading from all shards.

- Global secondary indexes, which are sharded separately based on the indexed values. An entry in the secondary index may refer to records from all shards of the primary key. When a record is written, several secondary index shards may need to be updated; however, a read of the postings list can be served from a single shard (fetching the actual records still requires reading from multiple shards).

Finally, we discussed techniques for routing queries to the appropriate shard, and how a coordination service is often used to keep track of the assigment of shards to nodes.

By design, every shard operates mostly independently—that’s what allows a sharded database to scale to multiple machines. However, operations that need to write to several shards can be problematic: for example, what happens if the write to one shard succeeds, but another fails? We will address that question in the following chapters.
