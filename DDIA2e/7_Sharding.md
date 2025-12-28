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
