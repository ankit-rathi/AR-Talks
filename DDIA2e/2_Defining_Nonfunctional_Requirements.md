The provided sources from Chapter 2, "Defining Nonfunctional Requirements," emphasize that while **functional requirements** define what an application does, **nonfunctional requirements**—such as reliability, scalability, and maintainability—determine if the application is actually usable and sustainable in the long term,.

The key takeaways from this chapter are:

### 1. Reliability and Fault Tolerance
Reliability is defined as a system’s ability to **continue working correctly even when things go wrong**,. 
*   **Faults vs. Failures:** A **fault** is a failure in a specific component (like a hard drive or a single machine), while a **failure** occurs when the system as a whole stops providing the required service to the user,.
*   **Managing Faults:** Systems achieve reliability through **fault tolerance**, which often involves **redundancy** (e.g., RAID disks or multi-node clusters) to ensure that a single point of failure (SPOF) does not bring down the entire system,. 
*   **Software and Human Error:** Software faults (like bugs or cascading failures) are often harder to manage than hardware faults because they tend to be **highly correlated** across nodes,. Furthermore, human configuration errors are a leading cause of outages, requiring technical measures like **rollback mechanisms** and cultural shifts like **blameless postmortems** to improve resilience,,.

### 2. Measuring Performance
Performance is not a single number but a **distribution** that must be measured and described accurately.
*   **Response Time vs. Throughput:** **Response time** is the total time a client sees for a request, while **throughput** is the volume of requests a system can handle per second,.
*   **The Importance of Percentiles:** Averages (means) are often misleading because they don't reflect the experience of typical users. Engineers should use **percentiles**, such as the **median (p50)** for typical performance and **high percentiles (p95, p99, p99.9)** to track **tail latencies**,. 
*   **Tail Latency Amplification:** In systems where one user request triggers multiple backend calls, a single slow backend call can delay the entire end-user request, making high-percentile performance critical for complex applications.

### 3. Scalability and Load
Scalability is the ability of a system to **cope with increased load** without a significant loss in performance,.
*   **Describing Load:** Load must be defined by specific **load parameters**, such as requests per second, read/write ratios, or the number of followers in a social network,.
*   **Scaling Strategies:** 
    *   **Vertical Scaling (Scaling Up):** Moving to a more powerful machine; however, this is expensive and has diminishing returns.
    *   **Horizontal Scaling (Scaling Out):** Using a **shared-nothing architecture** where many smaller machines coordinate via software. This approach is more complex but offers linear scalability and better fault tolerance,.
*   **Materialized Views:** As seen in the social network case study, precomputing data (like a home timeline) into a **materialized view** can significantly improve read performance at the cost of more complex and expensive write operations,.

### 4. Maintainability
Maintenance accounts for the majority of a software system's cost. The sources outline three pillars for making a system maintainable:
*   **Operability:** Making it easy for operations teams to keep the system running through **monitoring, automation, and predictable behavior**,.
*   **Simplicity:** Managing complexity by using **abstractions** (like SQL or database transactions) to hide implementation details and reduce the risk of bugs during changes,,.
*   **Evolvability:** Ensuring the system is flexible enough to adapt to **changing requirements** or new use cases over time,.

***

To visualize the relationship between **throughput** and **response time**, imagine a **grocery store checkout line**: when there are few customers (low throughput), the time it takes to check out (response time) is just the time it takes to scan items; however, as the store gets busier and more people enter the line, you spend more time waiting behind others (**queueing delay**), causing your total time in the store to increase dramatically even though the cashier is scanning at the same speed.
