# Dashboard Effort Estimation Plan

This document outlines the structured approach and effort estimation for building Tableau dashboards powered by Snowflake data warehouse, across three business areas.

---

## 📋 Project Overview

* **Total Business Areas:** 3
* **Dashboards per Area:** 4–5
* **Total Dashboards:** \~15
* **Resources Available:**

  * 1 Snowflake/Data Engineer
  * 1 Tableau Developer

---

## 🎯 Objective

1. Identify and analyze relevant data sources for each business area.
2. Ensure required raw data points are available in Snowflake.
3. Model and validate data as needed.
4. Design and build interactive Tableau dashboards.

---

## 🧮 Estimation Table (Effort in Person-Days)

| Phase                            | Task                                      | Snowflake Resource | Tableau Resource | Notes                    |
| -------------------------------- | ----------------------------------------- | ------------------ | ---------------- | ------------------------ |
| **1. Discovery & Planning**      | Requirement gathering + dashboard scoping | 3 days             | 3 days           | 1 day per business area  |
| **2. Data Discovery & Modeling** | Data source analysis + gap identification | 3 days             | -                | Identify tables, fields  |
|                                  | Data ingestion/modeling (if needed)       | 6–9 days           | -                | 2–3 days per data source |
|                                  | Data validation                           | 3 days             | -                | Parallel validation      |
| **3. Dashboard Development**     | Tableau design & development              | -                  | 15–20 days       | 1–1.5 days per dashboard |
| **4. UAT & Iteration**           | Review + feedback loop                    | 2 days             | 2 days           | Combined effort          |
| **5. Deployment & Docs**         | Publish, access control, documentation    | 1 day              | 1 day            | Include handoff          |
| **Buffer**                       | Unknowns & rework                         | 3 days             | 3 days           | Always include buffer    |

---

## 📊 Total Estimated Effort (Person-Days)

* **Snowflake Resource:** \~19–22 days
* **Tableau Resource:** \~24–29 days

> **Total Timeline (Parallel Execution):** \~4–5 weeks

---

## 🧠 Suggested Workflow by Week

| Week | Snowflake Person                        | Tableau Person             |
| ---- | --------------------------------------- | -------------------------- |
| 1    | Data source mapping & modeling (Area 1) | Requirement gathering      |
| 2    | Continue modeling (Areas 2 & 3)         | Start dashboards (Area 1)  |
| 3    | Data validation + fixes                 | Continue dashboards        |
| 4    | Support dev/debug + deploy              | Finish dashboards + review |
| 5    | UAT, doc, and buffer                    | UAT, doc, and buffer       |

---

## ✅ Recommendations

* **Prioritize** business areas with ready data sources.
* Build in **agile waves**: Release dashboards by business area.
* Maintain a **dashboard progress tracker**.
* Include **validation checkpoints** to ensure quality and consistency.

---

Would you like a Notion or Excel dashboard tracker template? Let me know!
