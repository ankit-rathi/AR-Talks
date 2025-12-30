The primary theme of this chapter is that **there are no perfect solutions in data systems architecture, only trade-offs**. To build an effective system, one must navigate various competing requirements, such as performance, cost, and complexity, to find the best possible balance for a specific application.

Key takeaways from the sources include:

### 1. Operational Versus Analytical Systems
Data systems are generally categorized into two distinct types based on their usage patterns:
*   **Operational Systems (OLTP):** These systems handle **online transaction processing**, serving interactive applications where users read and modify individual records (point queries). They focus on the **latest state of data** at low latency.
*   **Analytical Systems (OLAP):** These systems handle **online analytic processing**, used by analysts and data scientists to run aggregate queries over huge datasets for decision support. They often store a **history of events** rather than just the current state.
*   **Data Integration:** Data is moved from operational databases to **data warehouses** or **data lakes** via **Extract-Transform-Load (ETL)** processes. While data warehouses use structured relational models, data lakes offer a "sushi principle" approach, storing **raw data** in various formats for maximum flexibility.

### 2. Systems of Record and Derived Data
The sources distinguish between how data is managed and updated:
*   **Systems of Record:** Also known as the **source of truth**, these hold the authoritative version of data.
*   **Derived Data Systems:** These systems take information from a system of record and transform it for specific purposes, such as **caches, search indexes, or machine learning models**. While technically redundant, they are essential for query performance.

### 3. Cloud Services and Cloud-Native Architecture
The decision to use cloud services or self-host involves balancing business priorities and technical control.
*   **Trade-offs:** Cloud services allow organizations to **move faster** and handle **variable loads** more efficiently, but they result in **less control** over the infrastructure and potential vendor lock-in.
*   **Cloud-Native Design:** Modern cloud-native systems often feature the **separation of storage and compute**, where storage is handled by specialized services like Amazon S3 while computation is scaled independently. This allows for **multitenancy**, better hardware utilization, and easier scalability.

### 4. Distributed Versus Single-Node Systems
While distributing a system across multiple machines (nodes) can provide **fault tolerance, scalability, and lower latency** for global users, it introduces significant complexity.
*   **Complexity:** Distributed systems must deal with **network failures, timeouts, and consistency challenges** that do not exist on a single machine.
*   **Single-Node Efficiency:** If a workload can fit on a single node, it is often **much simpler and cheaper** to manage, as modern single-node databases have become increasingly powerful.

### 5. Law, Ethics, and Data Minimization
Data system design is increasingly influenced by legal regulations like **GDPR and CCPA**, which grant users rights such as the "right to be forgotten".
*   **Responsibility:** Engineers must consider the **ethical impact** of their systems, particularly regarding automated decision-making and privacy.
*   **Data Minimization:** Contrary to the "big data" philosophy of keeping everything, the principle of **data minimization** suggests only collecting data for a specified purpose and deleting it when it is no longer necessary to reduce legal and security risks.

To understand these trade-offs, you might think of a data system like a **custom-built home**: you can choose to have a massive open floor plan (scalability) or a highly reinforced foundation (fault tolerance), but every design choice you make to prioritize one feature will inevitably influence the cost, maintenance, and utility of the others.

### Chapter Summary

The theme of this chapter has been to understand trade-offs: that is, to recognize that for many questions there is not one right answer, but several different approaches that each have various pros and cons. We explored some of the most important choices that affect the architecture of data systems, and introduced terminology that will be needed throughout the rest of this book.

We started by making a distinction between operational (transaction-processing, OLTP) and analytical (OLAP) systems, and saw their different characteristics: not only managing different types of data with different access patterns, but also serving different audiences. We encountered the concept of a data warehouse and data lake, which receive data feeds from operational systems via ETL. In Chapter 4 we will see that operational and analytical systems often use very different internal data layouts because of the different types of queries they need to serve.

We then compared cloud services, a comparatively recent development, to the traditional paradigm of self-hosted software that has previously dominated data systems architecture. Which of these approaches is more cost-effective depends a lot on your particular situation, but it’s undeniable that cloud-native approaches are bringing big changes to the way data systems are architected, for example in the way they separate storage and compute.

Cloud systems are intrinsically distributed, and we briefly examined some of the trade-offs of distributed systems compared to using a single machine. There are situations in which you can’t avoid going distributed, but it’s advisable not to rush into making a system distributed if it’s possible to keep it on a single machine. In Chapter 9 we will cover the challenges with distributed systems in more detail.

Finally, we saw that data systems architecture is determined not only by the needs of the business deploying the system, but also by privacy regulation that protects the rights of the people whose data is being processed—an aspect that many engineers are prone to ignoring. How we translate legal requirements into technical implementations is not yet well understood, but it’s important to keep this question in mind as we move through the rest of this book.
