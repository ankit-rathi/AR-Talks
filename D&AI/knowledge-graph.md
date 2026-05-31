# Intelligence Loop Sketchbook — Master Asset Governance Table (42 Knowledge Nodes × 4 Sketch Types)

This is the **canonical reference table** that governs:

* Book Structure
* Knowledge Graph
* Dependency Chain
* Concept Ownership
* Topic Boundaries
* Sketchbook Flow
* Asset Creation Rules

Every future sketch should originate from **one row** of this table.

---

## PART I — WHY INTELLIGENCE EXISTS

| KG ID | Knowledge Node            | Depends On | Core Question                 | Owns                           | Out of Scope           | Concept Sketch                 | System Sketch                     | Decision Sketch                     | Evolution Sketch                 | Next |
| ----- | ------------------------- | ---------- | ----------------------------- | ------------------------------ | ---------------------- | ------------------------------ | --------------------------------- | ----------------------------------- | -------------------------------- | ---- |
| KG01  | Reality & Uncertainty     | None       | Why is intelligence needed?   | Uncertainty, risk, decisions   | Data, AI               | What is uncertainty?           | Decision making under uncertainty | Which decisions matter most?        | Human survival → Organizations   | KG02 |
| KG02  | Information               | KG01       | Why is information valuable?  | Signals, information advantage | Storage systems        | What is information?           | Information flow system           | What information creates advantage? | Signals → Information Economy    | KG03 |
| KG03  | Intelligence Loop         | KG01-02    | How does intelligence emerge? | Observation → Learning cycle   | AI implementation      | What is the Intelligence Loop? | End-to-end intelligence cycle     | Where is our loop broken?           | Feedback systems through history | KG04 |
| KG04  | Learning Organizations    | KG03       | How do organizations learn?   | Feedback loops, adaptation     | ML algorithms          | Organizational learning        | Learning architecture             | How can learning speed improve?     | Bureaucracy → Learning systems   | KG05 |
| KG05  | Evolution of Intelligence | KG01-04    | How has intelligence evolved? | Intelligence maturity          | Technical architecture | Organizational intelligence    | Intelligence maturity model       | What stage are we in?               | Intuition → AI → Autonomy        | KG06 |

---

## PART II — REALITY → MEMORY

| KG ID | Knowledge Node        | Depends On | Core Question                  | Owns                            | Out of Scope | Concept Sketch                   | System Sketch            | Decision Sketch               | Evolution Sketch            | Next |
| ----- | --------------------- | ---------- | ------------------------------ | ------------------------------- | ------------ | -------------------------------- | ------------------------ | ----------------------------- | --------------------------- | ---- |
| KG06  | Models & Abstractions | KG05       | How do we represent reality?   | Models, abstractions            | Databases    | What is a model?                 | Reality → Representation | What should be modeled?       | Maps → Digital Twins        | KG07 |
| KG07  | Observation Systems   | KG06       | How do organizations observe?  | Events, entities, relationships | Storage      | Events, entities & relationships | Observation architecture | What should we measure?       | Human observation → Sensors | KG08 |
| KG08  | Data                  | KG07       | What is organizational memory? | Recorded observations           | Warehouses   | What is data?                    | Data lifecycle           | What data should be retained? | Records → Data Products     | KG09 |
| KG09  | Data Platforms        | KG08       | How does memory scale?         | Databases, lakes, warehouses    | Pipelines    | Databases, warehouses, lakes     | Digital nervous system   | Centralized vs federated?     | Mainframes → Lakehouses     | KG10 |
| KG10  | Data Engineering      | KG09       | How does data move?            | Pipelines, integration          | Analytics    | What is data engineering?        | Information supply chain | Build vs buy platform?        | ETL → Data Products         | KG11 |

---

## PART III — MEMORY → UNDERSTANDING

| KG ID | Knowledge Node        | Depends On | Core Question                             | Owns                      | Out of Scope | Concept Sketch                 | System Sketch              | Decision Sketch            | Evolution Sketch              | Next |
| ----- | --------------------- | ---------- | ----------------------------------------- | ------------------------- | ------------ | ------------------------------ | -------------------------- | -------------------------- | ----------------------------- | ---- |
| KG11  | Analytics             | KG10       | What happened?                            | Descriptive understanding | Prediction   | What is analytics?             | Analytics lifecycle        | Which metrics matter?      | Reports → Augmented Analytics | KG12 |
| KG12  | Measurement           | KG11       | How do we quantify reality?               | KPIs, metrics             | Causality    | KPIs & Metrics                 | Measurement system         | What should be measured?   | Accounting → Telemetry        | KG13 |
| KG13  | Causality             | KG12       | Why did it happen?                        | Cause-effect reasoning    | ML           | Correlation vs causation       | Causal learning system     | Which levers matter?       | Observation → Experimentation | KG14 |
| KG14  | Decision Intelligence | KG13       | How does understanding improve decisions? | Decision systems          | Automation   | What is Decision Intelligence? | Decision Intelligence Loop | How can decisions improve? | Reporting → Decision Systems  | KG15 |
| KG15  | Feedback & Learning   | KG14       | How do systems improve?                   | Learning loops            | ML           | What is feedback?              | Learning engine            | How fast should we learn?  | PDCA → Continuous Learning    | KG16 |

---

## PART IV — MACHINE INTELLIGENCE

| KG ID | Knowledge Node          | Depends On | Core Question                   | Owns                            | Out of Scope          | Concept Sketch    | System Sketch            | Decision Sketch                | Evolution Sketch             | Next |
| ----- | ----------------------- | ---------- | ------------------------------- | ------------------------------- | --------------------- | ----------------- | ------------------------ | ------------------------------ | ---------------------------- | ---- |
| KG16  | Machine Learning        | KG15       | How do machines learn patterns? | ML fundamentals                 | Deep learning         | What is ML?       | Pattern learning system  | Should we use ML?              | Rules → Learning Systems     | KG17 |
| KG17  | Deep Learning           | KG16       | Why neural networks?            | Neural networks                 | LLMs                  | Neural networks   | Representation learning  | Classical ML vs DL             | Features → Representations   | KG18 |
| KG18  | Foundation Models       | KG17       | Why universal models?           | Pretraining paradigm            | Transformer internals | Foundation models | Pretraining architecture | Build vs consume?              | Specialized → General Models | KG19 |
| KG19  | Large Language Models   | KG18       | Why language intelligence?      | Tokens, attention, transformers | RAG                   | What is an LLM?   | Transformer system       | Open vs Closed models          | NLP → Language Platforms     | KG20 |
| KG20  | Generative Intelligence | KG19       | Why generation?                 | Text/image/code generation      | Agents                | What is GenAI?    | Generative architecture  | Where does GenAI create value? | Prediction → Creation        | KG21 |

---

## PART V — OPERATIONALIZING INTELLIGENCE

| KG ID | Knowledge Node      | Depends On | Core Question                 | Owns                     | Out of Scope   | Concept Sketch             | System Sketch                   | Decision Sketch                         | Evolution Sketch                  | Next |
| ----- | ------------------- | ---------- | ----------------------------- | ------------------------ | -------------- | -------------------------- | ------------------------------- | --------------------------------------- | --------------------------------- | ---- |
| KG21  | AI Engineering      | KG20       | How does AI become a product? | AI application lifecycle | Agents         | What is AI Engineering?    | AI application architecture     | When do we need AI Engineering?         | Models → Products                 | KG22 |
| KG22  | Context Engineering | KG21       | Why context matters?          | Context assembly         | Embeddings     | What is context?           | Context assembly system         | What context should be provided?        | Prompts → Context Systems         | KG23 |
| KG23  | Embeddings          | KG22       | How is meaning represented?   | Semantic vectors         | Vector DBs     | What are embeddings?       | Semantic representation system  | When do we need semantic understanding? | Keywords → Meaning                | KG24 |
| KG24  | Vector Databases    | KG23       | How is meaning stored?        | Similarity search        | RAG            | What is a vector database? | Semantic retrieval architecture | When should vector search be used?      | Search → Semantic Search          | KG25 |
| KG25  | RAG                 | KG24       | How does AI use memory?       | Retrieval architecture   | Agent planning | What is RAG?               | End-to-end RAG architecture     | RAG vs Fine-tuning                      | Static Models → Dynamic Knowledge | KG26 |
| KG26  | AI Memory           | KG25       | What should AI remember?      | Short & long-term memory | Agent autonomy | AI memory                  | Memory architecture             | What memory is worth storing?           | Stateless → Persistent AI         | KG27 |
| KG27  | AI Evaluation       | KG21-26    | How do we measure AI quality? | Evaluation systems       | Governance     | AI evaluation              | Evaluation framework            | What metrics matter?                    | Accuracy → Outcome Evaluation     | KG28 |

---

## PART VI — TRUST, CONTROL & COORDINATION

| KG ID | Knowledge Node           | Depends On | Core Question                              | Owns                          | Out of Scope  | Concept Sketch           | System Sketch             | Decision Sketch             | Evolution Sketch                  | Next |
| ----- | ------------------------ | ---------- | ------------------------------------------ | ----------------------------- | ------------- | ------------------------ | ------------------------- | --------------------------- | --------------------------------- | ---- |
| KG28  | Metadata                 | KG10       | How do systems understand systems?         | Data about data               | Quality rules | What is metadata?        | Metadata control plane    | What metadata is strategic? | Labels → Knowledge Assets         | KG29 |
| KG29  | Data Quality             | KG28       | Why trust matters?                         | Accuracy, completeness, trust | Governance    | What is data quality?    | Trust architecture        | How much quality is enough? | Validation → Trust Systems        | KG30 |
| KG30  | Explainability & Lineage | KG29       | Why trace decisions?                       | Traceability                  | Policies      | Explainability & lineage | Traceability architecture | How explainable must we be? | Reports → Transparent Systems     | KG31 |
| KG31  | Governance               | KG30       | How do organizations control intelligence? | Policies & accountability     | Monitoring    | What is governance?      | Governance framework      | Governance vs agility       | Policies → Adaptive Governance    | KG32 |
| KG32  | Observability            | KG31       | How do we monitor intelligence?            | Monitoring systems            | Agents        | What is observability?   | Monitoring architecture   | What should be monitored?   | Logs → Intelligence Observability | KG33 |

---

## PART VII — AUTONOMOUS ORGANIZATIONS

| KG ID | Knowledge Node                        | Depends On | Core Question                        | Owns                          | Out of Scope             | Concept Sketch                 | System Sketch                         | Decision Sketch                   | Evolution Sketch                   | Next |
| ----- | ------------------------------------- | ---------- | ------------------------------------ | ----------------------------- | ------------------------ | ------------------------------ | ------------------------------------- | --------------------------------- | ---------------------------------- | ---- |
| KG33  | AI Agents                             | KG27, KG32 | What is an agent?                    | Reasoning + Tools + Action    | Multi-agent systems      | Agent fundamentals             | Agent architecture                    | Should this task become agentic?  | Automation → Agency                | KG34 |
| KG34  | Tool Use & MCP                        | KG33       | How do agents interact with systems? | MCP, tools, protocols         | Multi-agent coordination | Tool calling & MCP             | Tool ecosystem architecture           | Which tools should agents access? | APIs → Standardized AI Interfaces  | KG35 |
| KG35  | Planning & Reasoning                  | KG33-34    | How do agents think?                 | Planning & decomposition      | Agent teams              | Planning systems               | Goal → Plan → Action                  | Reactive vs planning agents       | Scripts → Autonomous Planning      | KG36 |
| KG36  | Multi-Agent Systems                   | KG35       | Why multiple agents?                 | Coordination patterns         | Workflow automation      | Multi-agent systems            | Distributed intelligence architecture | Single vs multi-agent?            | Teams → Agent Teams                | KG37 |
| KG37  | Autonomous Workflows                  | KG36       | How does work become autonomous?     | End-to-end execution          | Org design               | Agentic workflows              | Closed-loop execution system          | What should be automated?         | Workflow Automation → Autonomy     | KG38 |
| KG38  | Intelligence Products                 | KG37       | What is an intelligence product?     | Data & AI products            | Operating model          | Data vs intelligence products  | Intelligence marketplace              | What should become a product?     | Reports → Intelligence Services    | KG39 |
| KG39  | AI-Native Organizations               | KG38       | What changes in organizations?       | AI operating model            | Human role               | AI-native enterprise           | AI operating model                    | How should organizations evolve?  | Digital → AI-Native                | KG40 |
| KG40  | Human-AI Collaboration                | KG39       | What remains human?                  | Human-agent teaming           | Forecasting              | Augmented intelligence         | Human-agent teaming                   | What should humans keep doing?    | Tools → Teammates                  | KG41 |
| KG41  | Intelligence Infrastructure           | KG40       | Does intelligence become a utility?  | Enterprise intelligence layer | Future predictions       | Intelligence as infrastructure | Enterprise intelligence platform      | Where is advantage created?       | Electricity → Intelligence Utility | KG42 |
| KG42  | Future of Organizational Intelligence | KG01-KG41  | Where are we heading?                | Entire framework synthesis    | None                     | Future intelligence systems    | Evolutionary intelligence model       | How should we prepare?            | Human → Collective Intelligence    | END  |

---

## Asset Count

| Sketch Type        |   Count |
| ------------------ | ------: |
| Concept Sketches   |      42 |
| System Sketches    |      42 |
| Decision Sketches  |      42 |
| Evolution Sketches |      42 |
| **Total Assets**   | **168** |

This table is now your master reference for the entire *Intelligence Loop Sketchbook* and can be used as the source row for generating any individual sketch asset while maintaining dependency flow, scope boundaries, and zero redundancy.
