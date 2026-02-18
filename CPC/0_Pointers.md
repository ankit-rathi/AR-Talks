
### Intro Pointers
- 20 years → multiple layers → data value chain
- writing SQL queries → building ETL pipelines → designing database/data warehouse → end-to-end data lifecycle management
- 2016 → data science → analytical outcomes → data quality and integrity
- Kaggle competitions → two books on data science
- Recent years → data engineering → leading data teams → reusable frameworks → ingestion standards
- Last year → SW → DMOP/Arago --> two major problems → data ownership → governance/quality controls
- Data marketplace → clear ownership with producuers → executable data governance controls → OBDQ framework
- My motivation → OBDQ framework → bank-wide impact → data foundations
- Personal initiative → Visual Notes on Data and AI Concepts → Engage Community → 300+ Members

---

### Motivation and Fitness Pointers
* **What I look in work environment**  → Problem Solving via Collaboration → Option analysis → Trade-offs discussions
* **What kind of work excites me** → Requirements → Design → Building scalable and resilient solution
* **When I feel Productive and Fulfilled** → Working on end-to-end problems → building scalable and resilient solution and frameworks
* **How this team contributes to Bank's Purpose and Values** → data management is foundational → data quality is critical → risk amangement, regulatory compliance and executive decision making
* **Why do I want to work in this team** → data management and data uqality is non-negotiable → want to build scalable and resilient solution/framework for pan-bank

---

### CPC Pointers
* **Connected** → HLSD rejected by Data Architecture Forum (DAF)
* **Improved Innovator** → Metadata-driven dynamic DAG orchestration (DSAR)
* **Critical Thinker** → Automated manual reconciliation in CBM ETL batch
* **Change Ready** → Operating model evolution + raising delivery standards
* **Trusted Advisor** → RAS Excel → Strategic metrics platform (Snowflake + QuickSight)

---

### CPC Skills and Questions with pointers

**Connected** - pointer: HLSD was rejected by DAF (Data Architecture Forum)
- When have you needed to work collaboratively with someone who approached work differently to you?
- When have you led a team that wasn't working as well as it could?
> - S - HLSD for CBM project was rejected by DAF team due to existing technical debt
> - T - I needed to get the approval from DAF on the HLSD to deploy the business critical app in prod
> - A - Connected with forum member to understand the concerns, collaborated with data source owners to understand the constraints, documented the story around the design
> - R - I was able to present the same design with current limitations and our future plan to address and got DAF approval

**Improved Innovator** - pointer: Used dynamic DAGs to keep the orchestration flexible
- When have you taken the opportunity to improve something for the customer or the colleagues? 
- When have you experimented with a new way of doing something?
> - S - As part of DSARs project, we were sourcing customer data from various data sources based on the subject access request. But different requests needed data from different source systems.
> - T - We needed an orchestration mechanism which could dynamically add tasks to a DAG
> - A - I suggested the team to try dynamic DAG creation and execution based on the request, dynamic DAG was built and stored in json format
> - R - We were able to handle the requirement by keeping the orchestration flexible based on incoming request without increasing the complexity of the system

**Critical Thinker** - pointer: Solved and automated Manual reconciliation in CBM ETL batch
- When have you considered multiple sources of information or data when solving a problem?
- When have you made a decision that had a significant positive impact on customer or colleague?
> - S - ETL batch in CBM application required manual reconciliation due to complexity in incoming data feeds, which required 2 FTEs for 4-5 days every month for last 3 years.
> - T - I needed to find a way if we could automate this part of the batch without any manual interventions.
> - A - We sat down we upstream data providers on how they were preparing the data, by looking at the patterns and relationship in those data sets we identified that there can be a logical way to automate this stuff.
> - R - We automated the whole ETL batch and saved 2 FTEs 4-5 days of involvement in manual reconciliation.

**Change Ready** - pointer: adjusting the individual contributors to handle shallow tasks effectively
- When has reflecting on your performance helped you achieve better results?
- Talk me through how you have raised the standard of work delivery by your team.
> - S - Technical resources are more inclined towards deep work, they needed to collaborate on large project intermittently and were struggling with context switching
> - T - I needed to device a way to collaborate without affecting their current work to make overall delivery effective.
> - A - I myself am a deep worker and have struggled in the past, I suggested them to keep an hour window during the day for shallow work and collboration, helping each other.
> - R - Team members liked this approach and could help each other on various issue without disrupting their work.

**Trusted Advisor** - pointer: RAS Excel dashboard converted to strategic solution with Metric platform, Snowflake and Quicksight
- When has your knowledge helped your colleague or a customer make a better decision?
- When has showing genuine care for customer or colleague really helped your relationship with them?
> - S - Business stakeholders built a RAS dashboard using tactical data in an excel sheet, they wanted a technical solution with forms and dashboards together.
> - T - I needed to make sure that they understand that strategic solutions are built differently while meeting all their business requirements.
> - A - I explained them how strategic solution works which may be a bit different than current tactical solution but would be more effective in longer run. We demoed them using Metric platform, Snowflake and Quicksight to make them comfortable.
> - R - They were convinced after the explanation and seeing our demo, we worked with them to deliver the strategic solution which met all the requirements by stakeholders.

---

**My Project**
- S
  * Needed to operationalize GDPR/CCPA DSAR compliance
  * Customer data was fragmented across structured and unstructured, on-prem and cloud, domain-owned platforms with heterogeneous latency
- T
  * Decouple orchestration from domain systems
  * Minimize blast radius of failures
  * Support hybrid cloud execution
  * Enforce strict auditability
  * Be extensible for onboarding future domains
- A
  * Event-driven architecture
  * Registration, Processing and Servicing layers
  * Identity Resolution, Failure Isolation & Resilience
  * Eventual consistency, Federated retrieval, Serverless compute
- R
  * Automated the majority of DSAR requests
  * Improved SLA adherence significantly
  * Reduced manual intervention
  * Enabled faster onboarding of new domain system
  * Increased auditability and compliance confidence

---

**Their Project**
- Definition
  * Define → Validate → Insert
- Execution
  * Read → Attach → Execute → Retrieve → Transform → Write
- Action
  * Visualize → Log → Remediate


- Domain team defines DQ rules
- OBDQ validates + registers rule metadata
- During ingestion / batch:
  * OBDQ fetches rules
  * Triggers Glue DQ execution
- Glue evaluates rules
- Results stored centrally
- OBDQ standardizes output
- QuickSight dashboards visualize health
- SMUS analyzes historical trends
- Failures logged for remediation

