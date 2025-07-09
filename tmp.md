This section outlines the key non-functional requirements for the DORA reporting automation solution to ensure it meets operational expectations and aligns with the bank's standards.

1. Performance & Timeliness
The monthly ingestion, validation, and report generation process must complete overnight within a few hours, ensuring availability of outputs by the next business day.

The system should be optimized for batch processing of large data volumes.

2. Availability
The system is expected to run in batch mode once a month, post business hours.

High availability is not a primary requirement; however, the solution should be reliable enough to ensure monthly processing without failure.

3. Security & Compliance
The system must comply with the bank's internal IT security policies, including:

Role-based access control (read-only consumer access)

Secure APIs for data ingestion and report export

Encryption at rest and in transit as per standard policies

No additional DORA-specific security constraints are currently mandated.

4. Auditability & Logging
Standard application logging must be implemented to capture key events related to:

Data ingestion success/failure

Validation checks and errors

File generation for reporting

Logs should be retained as per the bank’s retention policy and be accessible for internal audit and troubleshooting.

5. User Access & Roles
The system will support read-only consumer access to generated reports.

No complex role hierarchy is required; RBAC will be limited to data consumers.

Authentication and authorization will follow existing bank standards.

6. Scalability & Extensibility
The solution should be designed with extensibility in mind to allow future:

Inclusion of additional reporting use cases under DORA

Onboarding of new data sources and systems

Design should support modular enhancement with minimal rework.

7. Technical Stack & Integration
There are no strict technology constraints; the solution may leverage any tech stack suitable for meeting business and operational needs.

It must be capable of integrating with existing systems such as:

Operations Assets database

Internal Service Management (ISM) tools

APIs for report generation must be compatible with downstream reporting platforms.
