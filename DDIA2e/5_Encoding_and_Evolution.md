The primary theme of this chapter is **evolvability**: the ability to modify applications easily as requirements change. Because large-scale changes to code and data formats cannot happen instantaneously, systems must be designed to handle the coexistence of old and new versions.

The following are the key takeaways regarding data encoding and flow:

### 1. The Crucial Role of Compatibility
To ensure a system continues running smoothly during upgrades, it must maintain two types of compatibility:
*   **Backward Compatibility:** Newer code can read data that was written by older code. This is generally easy to achieve as the new code can be programmed to handle old formats.
*   **Forward Compatibility:** Older code can read data that was written by newer code. This is more challenging because it requires the old code to ignore additions it does not yet understand without losing or corrupting data.

### 2. Comparison of Encoding Formats
The sources distinguish between several ways to represent data for storage or transmission:
*   **Language-Specific Formats:** Built-in tools like Java’s `Serializable` or Python’s `pickle` are convenient but dangerous; they are often tied to one language, pose **security risks** by allowing arbitrary class instantiation, and frequently neglect compatibility.
*   **Textual Formats (JSON, XML, CSV):** These are human-readable and widely supported but have significant flaws, such as **ambiguity in number encoding** (e.g., integers vs. floats) and lack of native support for **binary strings**.
*   **Binary Schema-Driven Formats:** Tools like **Protocol Buffers** and **Avro** are more compact and efficient. They use schemas to define data structures, which serves as documentation and allows for type-checking in statically typed languages.

### 3. Schema Evolution Strategies
Different binary formats handle changes (evolution) differently:
*   **Protocol Buffers:** Uses **field tags** (numbers) to identify fields. You can add fields by assigning new tags; old code will simply skip tags it doesn't recognize, maintaining forward compatibility.
*   **Avro:** Does not use tags. Instead, it uses a **writer’s schema** and a **reader’s schema**. Differences are resolved by matching field names, and compatibility is maintained by only adding or removing fields that have **default values**.

### 4. Modes of Dataflow
The sources identify several ways data moves between processes, each with unique compatibility needs:
*   **Databases:** Data in a database often "outlives" the code. A value written years ago must still be readable today, and during rolling upgrades, old code may need to read values recently written by new code.
*   **Services (REST and RPC):** Clients and servers communicate via APIs. While **REST** is popular for its simplicity and use of HTTP, **RPC** (Remote Procedure Call) can be problematic because it attempts to make a network request look like a local function call, ignoring the unpredictability of networks and latency.
*   **Asynchronous Message Passing:** Using **message brokers** (like Kafka or RabbitMQ) or the **actor model** decouples senders and recipients. This provides better reliability and allows a single message to be sent to multiple consumers.

### 5. Durable Execution and Workflows
For complex, multi-step operations like payment processing, **workflow engines** (e.g., Temporal) provide **durable execution**. These frameworks ensure that even if a process fails, it can resume exactly where it left off by logging all state changes and RPC calls to durable storage.

Managing data evolution is like **sending a message to your future self** through a database. You must ensure that your "future self" understands the context of the message, but also that your "past self" (older code) doesn't get confused by new information it isn't ready to process yet.
