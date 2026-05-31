I would move from a **generic image-generation prompt** to a **governed sketch-generation prompt**.

The biggest lesson from our iteration is:

```text
The Knowledge Graph controls WHAT to teach.
The Sketch Type controls HOW to teach it.
The Prompt controls visual consistency.
```

So the prompt should only contain those three things.

---

# MASTER INTELLIGENCE LOOP SKETCHBOOK PROMPT (v2.0)

Use this prompt for generating **one sketch page at a time**.

```text
Act as a professional educational sketchnote illustrator, systems-thinking visual storyteller, and infographic designer.

You are creating one page for the Intelligence Loop Sketchbook.

KNOWLEDGE GRAPH ROW

[PASTE SINGLE KG ROW]

SKETCH TYPE

[Concept | System | Decision | Evolution]

--------------------------------------------------
GLOBAL SKETCHBOOK STANDARDS
--------------------------------------------------

• STRICT 4:5 aspect ratio
• Single standalone page
• Educational sketchnote infographic
• Hand-drawn visual language
• White background
• Pastel highlights
• Clean black outlines
• Consistent typography hierarchy
• Consistent icon system
• Consistent spacing
• Book-quality layout
• High readability
• High information density
• No photorealistic elements
• No decorative clutter

This sketch must feel like one page from a coherent 168-page sketchbook.

--------------------------------------------------
KNOWLEDGE GRAPH GOVERNANCE
--------------------------------------------------

Use ONLY the ownership defined in the KG row.

Respect:
• Depends On
• Core Question
• Ownership
• Explicitly Out of Scope
• Next Node

Do not introduce concepts owned by future nodes.

Do not duplicate concepts owned by previous nodes.

Keep boundaries clean.

--------------------------------------------------
VISUAL STORYTELLING RULE
--------------------------------------------------

The sketch must tell one coherent story.

Avoid disconnected boxes.

Every section should naturally lead to the next section.

The reader should be able to understand the topic by reading from top-left to bottom-right.

--------------------------------------------------
SKETCH TEMPLATE
--------------------------------------------------
```

---

# CONCEPT SKETCH TEMPLATE

Use when:

```text
Question:
"What is it?"
```

Prompt Add-on:

```text
Create a Concept Sketch.

Use this structure:

1. Everyday Observation
2. Hidden Problem
3. Simple Idea
4. Core Mechanism
5. Real-World Example
6. Why It Matters
7. Big Insight

Goal:

Build intuition.

The reader should understand the concept without prior technical knowledge.

Focus on understanding rather than implementation.

End with a memorable insight.

Output should be a complete 4:5 sketchnote infographic.
```

---

# SYSTEM SKETCH TEMPLATE

Use when:

```text
Question:
"How does it work?"
```

Prompt Add-on:

```text
Create a System Sketch.

Use this structure:

1. Goal
2. Inputs
3. Core Components
4. End-to-End Flow
5. Outputs
6. Feedback Loop
7. Failure Modes
8. System Insight

Goal:

Reveal the architecture.

Show how components interact.

Include one central system diagram.

Emphasize flows, dependencies, and feedback loops.

Output should be a complete 4:5 sketchnote infographic.
```

---

# DECISION SKETCH TEMPLATE

Use when:

```text
Question:
"What should we do?"
```

Prompt Add-on:

```text
Create a Decision Sketch.

Use this structure:

1. Decision Context
2. Available Options
3. Tradeoffs
4. Decision Framework
5. Evaluation Criteria
6. Rules of Thumb
7. Strategic Insight

Goal:

Help leaders, architects, engineers, and advisors make better decisions.

Focus on choices rather than implementation details.

Include one central decision framework.

Output should be a complete 4:5 sketchnote infographic.
```

---

# EVOLUTION SKETCH TEMPLATE

Use when:

```text
Question:
"How did we get here?"
```

Prompt Add-on:

```text
Create an Evolution Sketch.

Use this structure:

1. Starting Point
2. Limitation
3. Innovation
4. Next Stage
5. Current State
6. Future State
7. Evolution Insight

Goal:

Show the historical progression of ideas.

Emphasize why each stage emerged.

Use a timeline or evolutionary flow.

Output should be a complete 4:5 sketchnote infographic.
```

---

# Example Usage

For KG24 (Vector Databases):

```text
KG24 – Vector Databases

Depends On:
Embeddings

Core Question:
How is meaning stored and retrieved?

Ownership:
Similarity Search

Out of Scope:
RAG orchestration

Next Node:
RAG

Sketch Type:
System
```

Then append the **System Sketch Template**.

That will produce a much more coherent result than asking for all four sketches together because:

```text
KG24 Concept Sketch  = What is a Vector Database?
KG24 System Sketch   = How Semantic Retrieval Works
KG24 Decision Sketch = When Should You Use Vector Search?
KG24 Evolution Sketch = Keyword Search → Semantic Search
```

Each page has a unique job, a unique narrative, and a full 4:5 canvas dedicated to that job. That is the structure most likely to stay consistent across all 168 sketch assets.
