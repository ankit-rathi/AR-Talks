## 3. Data Models and Query Languages

The primary takeaway from this chapter is that **data models determine not only how software is written, but how we think about the problems we are solving**. Because no single model is perfect for every use case, developers must navigate trade-offs between different structures, such as relational, document-based, and graph-oriented models.

Key insights from the sources include:

### 1. The Relational vs. Document Model Debate
The choice between these models often centers on the structure of the data and the frequency of relationships.
*   **The Document Model:** This model is best suited for **tree-structured data** where one-to-many relationships predominate and the entire "document" is typically loaded at once. It offers **schema flexibility** (schema-on-read), allowing for heterogeneous data where not all records share the same structure.
*   **The Relational Model:** This remains the dominant choice for applications involving **many-to-one and many-to-many relationships**. It provides superior support for **joins**, which reduce data redundancy through normalization.
*   **Impedance Mismatch:** A common challenge in relational databases is the "awkward translation" required between object-oriented application code and table-based storage. While **Object-Relational Mapping (ORM)** frameworks reduce boilerplate code, they can introduce complexities like the **N+1 query problem**.

### 2. Normalization and Performance Trade-offs
Deciding whether to normalize data involves a fundamental trade-off between read and write efficiency.
*   **Normalization:** By using IDs to reference information stored in a single place, normalized data is typically **faster to write** and ensures consistency. However, it is **slower to query** because it requires multiple joins.
*   **Denormalization:** Storing redundant copies of data makes it **faster to read** by avoiding joins, but it is **more expensive to write** and risks data inconsistency if updates are not handled carefully. 
*   **Data Locality:** Document databases provide a performance advantage when an application needs to access an entire record at once, as the data is stored in one continuous string rather than split across multiple tables.

### 3. Graph-Like Data Models
When connections between data points become so complex that "anything is potentially related to everything," graph models become more natural.
*   **Vertices and Edges:** Graphs consist of **vertices** (entities) and **edges** (relationships). This model is highly flexible, allowing any vertex to connect to any other without a restrictive schema.
*   **Recursive Queries:** Graph languages like **Cypher** or **SPARQL** are significantly more concise than SQL for traversing variable-length paths. For example, a 4-line Cypher query to find migration patterns might require over 30 lines of clumsy recursive SQL.

### 4. Specialized Models: Event Sourcing and DataFrames
Beyond traditional databases, specialized models serve unique architectural and analytical needs:
*   **Event Sourcing:** This approach uses an **append-only log of immutable events** as the source of truth. It employs **Command Query Responsibility Segregation (CQRS)** to derive read-optimized "materialized views" from the write-optimized event log.
*   **DataFrames:** Popular in scientific and machine learning contexts, DataFrames generalize relational tables into large numbers of columns and **multidimensional arrays**. They allow data scientists to "wrangle" data through a series of commands rather than a single declarative query.

### 5. Declarative Query Languages
A major advantage of languages like SQL or Cypher is that they are **declarative**—you specify *what* data you want, not *how* the computer should retrieve it. This allows the database's **query optimizer** to introduce performance improvements, such as parallel execution, without requiring changes to the application code.

***

To understand the difference between these models, imagine organizing a **personal library**: a **document model** is like keeping each author's work in a single, dedicated box (everything is together, but hard to cross-reference); a **relational model** is like a traditional library shelf where books are categorized by genre and tracked by a central index (organized for searching, but requires walking to different aisles to find everything by one author); and a **graph model** is like a web of strings connecting every book to every other book that shares a similar theme, character, or historical setting (perfect for following complex connections, but messy for a simple inventory).

### Chapter Summary

Data models are a huge subject, and in this chapter we have taken a quick look at a broad variety of different models. We didn’t have space to go into all the details of each model, but hopefully the overview has been enough to whet your appetite to find out more about the model that best fits your application’s requirements.

The relational model, despite being more than half a century old, remains an important data model for many applications—especially in data warehousing and business analytics, where relational star or snowflake schemas and SQL queries are ubiquitous. However, several alternatives to relational data have also become popular in other domains:

- The document model targets use cases where data comes in self-contained JSON documents, and where relationships between one document and another are rare.

- Graph data models go in the opposite direction, targeting use cases where anything is potentially related to everything, and where queries potentially need to traverse multiple hops to find the data of interest (which can be expressed using recursive queries in Cypher, SPARQL, or Datalog).

- DataFrames generalize relational data to large numbers of columns, and thereby provide a bridge between databases and the multidimensional arrays that form the basis of much machine learning, statistical data analysis, and scientific computing.

To some degree, one model can be emulated in terms of another model—for example, graph data can be represented in a relational database—but the result can be awkward, as we saw with the support for recursive queries in SQL.

Various specialist databases have therefore been developed for each data model, providing query languages and storage engines that are optimized for a particular model. However, there is also a trend for databases to expand into neighboring niches by adding support for other data models: for example, relational databases have added support for document data in the form of JSON columns, document databases have added relational-like joins, and support for graph data within SQL is gradually improving.

Another model we discussed is event sourcing, which represents data as an append-only log of immutable events, and which can be advantageous for modeling activities in complex business domains. An append-only log is good for writing data (as we shall see in Chapter 4); in order to support efficient queries, the event log is translated into read-optimized materialized views through CQRS.

One thing that non-relational data models have in common is that they typically don’t enforce a schema for the data they store, which can make it easier to adapt applications to changing requirements. However, your application most likely still assumes that data has a certain structure; it’s just a question of whether the schema is explicit (enforced on write) or implicit (assumed on read).

Although we have covered a lot of ground, there are still data models left unmentioned. To give just a few brief examples:

- Researchers working with genome data often need to perform sequence-similarity searches, which means taking one very long string (representing a DNA molecule) and matching it against a large database of strings that are similar, but not identical. None of the databases described here can handle this kind of usage, which is why researchers have written specialized genome database software like GenBank [73].

- Many financial systems use ledgers with double-entry accounting as their data model. This type of data can be represented in relational databases, but there are also databases such as TigerBeetle that specialize in this data model. Cryptocurrencies and blockchains are typically based on distributed ledgers, which also have value transfer built into their data model.

- Full-text search is arguably a kind of data model that is frequently used alongside databases. Information retrieval is a large specialist subject that we won’t cover in great detail in this book, but we’ll touch on search indexes and vector search in “Full-Text Search”.

We have to leave it there for now. In the next chapter we will discuss some of the trade-offs that come into play when implementing the data models described in this chapter.
