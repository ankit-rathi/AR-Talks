
# Dashboard Effort Estimation & Setup Plan

A structured plan to estimate and execute the development of Tableau dashboards using Snowflake as the data warehouse across three business areas, with supporting platform setup and project infrastructure.

## Project Scope

- Business Areas: 3
- Dashboards per Area: 4–5
- Total Dashboards: ~15
- Core Team:
  - 1 Snowflake Admin/Data Engineer
  - 1 Tableau Developer

## Objectives

1. Identify key data sources per business area.
2. Ensure all raw data is available in Snowflake.
3. Build data models and pipelines (if needed).
4. Set up necessary infrastructure (Snowflake, Airflow, Tableau, JIRA).
5. Develop and deploy Tableau dashboards.
6. Support user onboarding and testing.

## Platform & Infra Setup Effort

| Setup Component            | Task Description                             | Owner               | Effort (Days) | Notes                        |
|---------------------------|----------------------------------------------|----------------------|---------------|------------------------------|
| Snowflake Admin Setup     | Roles, warehouses, RBAC setup, quota policies| Snowflake Engineer   | 2 days        | Initial platform prep        |
| Airflow Integration       | Airflow deployment, Snowflake connector setup| Snowflake Engineer   | 2–3 days      | Optional if pipeline needed  |
| Tableau Setup             | License provisioning, site/project setup     | Tableau Developer    | 1 day         | Includes access control      |
| JIRA Setup                | Project board, workflows, task templates     | Project Manager/Lead | 1 day         | Optional but useful          |
| User Onboarding           | Training on access, JIRA, Tableau usage      | Combined Effort      | 1 day         | Admin + basic training       |

## Development Effort (Person-Days)

| Phase                      | Task                                      | Snowflake Engineer | Tableau Developer | Notes                      |
|----------------------------|-------------------------------------------|---------------------|--------------------|----------------------------|
| Discovery & Planning       | Dashboard scoping + requirement gathering | 3 days              | 3 days             | 1 day per business area    |
| Data Readiness             | Source identification & gap analysis      | 3 days              | -                  | Review schema + fields     |
|                            | Ingestion/modeling (if needed)            | 6–9 days            | -                  | 2–3 days per data source   |
|                            | Data validation                           | 3 days              | -                  | Parallel with dev          |
| Dashboard Development      | Tableau development & design              | -                   | 15–20 days         | 1–1.5 days per dashboard   |
| UAT & Iteration            | Review + feedback loop                    | 2 days              | 2 days             | Combined effort            |
| Deployment & Docs          | Publish dashboards, documentation         | 1 day               | 1 day              | Include walkthroughs       |
| Buffer                     | Unknowns & rework                         | 3 days              | 3 days             | Always buffer              |

## Total Estimated Effort

| Role               | Effort (Person-Days) |
|--------------------|----------------------|
| Snowflake Engineer | ~24–28 days          |
| Tableau Developer  | ~24–29 days          |
| PM/User Onboarding | ~2–3 days            |

Estimated Timeline (Parallel Workstreams): ~5–6 weeks

## Suggested Weekly Workflow

| Week | Snowflake Engineer                  | Tableau Developer         | PM/Support             |
|------|-------------------------------------|----------------------------|------------------------|
| 1    | Snowflake & Airflow setup, data mapping| Requirement gathering  | JIRA + onboarding      |
| 2    | Ingestion & modeling (Area 1)       | Dashboards (Area 1)       |                        |
| 3    | Modeling (Areas 2 & 3), validation  | Dashboards (Areas 2 & 3)  |                        |
| 4    | Data fixes, support, deploy         | Final dashboards + review |                        |
| 5    | UAT, bugfixes, documentation        | UAT, polish, documentation|                        |
| 6    | Buffer + support                    | Buffer + support          |                        |

## Final Recommendations

- Sequence business areas by data readiness.
- Document field mappings, transformations, and dashboard logic from day one.
- Use agile sprints to demo dashboards early and often.
- Set up a dashboard tracker and task status board (JIRA).
- Include user onboarding and access setup early to avoid go-live delays.
