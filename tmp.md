
# Dashboard Effort Estimation & Plan - Presentation Transcript

## Opening

Good [morning/afternoon], everyone. Thank you for taking the time to join this session.

Today, I’d like to walk you through our proposed plan and effort estimation for building business dashboards on Tableau, powered by Snowflake as our data warehouse.

This project spans three business areas, each with distinct data sources and dashboard needs. Our goal is to deliver a set of reliable, insightful dashboards that support data-driven decision-making across the organization.

## Project Scope and Objectives

We’re looking at roughly 4 to 5 dashboards per business area, which totals around 15 dashboards.

The core objectives of this project are:

1. Identifying and validating the right data sources.
2. Ensuring all required raw data is modeled and made available in Snowflake.
3. Building interactive, user-friendly Tableau dashboards.
4. Managing the project using industry-standard tools and governance frameworks.

## Key Resources

We’ll be working with two dedicated resources:

- One focused on Snowflake and data engineering.
- One focused on Tableau dashboard development.

In addition, there are a few enabling tasks such as Snowflake administration, Airflow orchestration, and user onboarding that are essential to kickstart the delivery efficiently.

## Effort Estimation

Let me now break down the effort in person-days across each major phase.

| Phase | Task | Snowflake Engineer | Tableau Developer | Additional Roles |
| --- | --- | --- | --- | --- |
| Discovery & Planning | Requirement gathering & dashboard scoping | 3 | 3 | - |
| Data Platform Setup | Snowflake admin & DWH setup | 3 | - | - |
| Orchestration Setup | Airflow setup & Snowflake integration | 3 | - | - |
| DevOps & Tooling | Tableau licenses & configuration | - | 2 | - |
| Project Management | JIRA board setup | 1 | 1 | - |
| User Enablement | Onboarding & access | 1 | 1 | - |
| Data Discovery | Source analysis & gap ID | 3 | - | - |
| Data Engineering | Ingestion/modeling | 6–9 | - | - |
| Data QA | Data validation | 3 | - | - |
| Dashboard Dev | Tableau design & build | - | 15–20 | - |
| UAT & Review | Feedback & iterations | 2 | 2 | - |
| Deployment | Final deploy & docs | 1 | 1 | - |
| Buffer | For rework or unknowns | 3 | 3 | - |

Total effort comes to approximately **25–28 days** for the Snowflake resource, and **27–32 days** for the Tableau resource.

## Delivery Timeline

With parallel execution, we’re looking at a timeline of about **5 weeks**, structured as follows:

| Week | Snowflake Person | Tableau Person |
|------|------------------|----------------|
| 1    | Platform setup + Area 1 modeling | Requirement gathering |
| 2    | Area 2 & 3 data prep | Area 1 dashboards |
| 3    | Validation & fixes | Continue dashboards |
| 4    | Support & deploy | Finish dashboards + review |
| 5    | UAT, onboarding, buffer | UAT, onboarding, buffer |

## Key Recommendations

I recommend we approach the delivery in agile waves—starting with business areas that already have structured data available. This lets us show progress early and adapt to feedback.

Additionally, setting up a dashboard tracker and establishing periodic validation checkpoints will help maintain data quality and development pace.

## Closing

That wraps up the plan. I’m happy to answer any questions or dive deeper into any of the phases or assumptions made in the estimation.
