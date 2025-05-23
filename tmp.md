# RAID Log – Dashboard Effort & Setup Plan

## Risks
| Risk | Description | Mitigation |
|------|-------------|------------|
| **Data unavailability** | Required raw data may not exist or be incomplete in source systems. | Early data discovery phase, escalate missing data to business owners. |
| **Underestimation of dashboard complexity** | Some dashboards may require more time due to complex logic or visuals. | Add buffer in timeline; prioritize MVP features first. |
| **Integration delays** | Snowflake + Airflow or Tableau setup might take longer than planned. | Start infra setup in parallel with planning; engage platform teams early. |
| **Limited resource availability** | Only 1 person each for Snowflake and Tableau may become a bottleneck. | Prioritize business areas; avoid parallel work on too many dashboards. |
| **Stakeholder feedback loop** | Late feedback or unclear requirements can delay progress. | Schedule interim demos, agree on acceptance criteria early. |

## Assumptions
| Assumption | Rationale |
|------------|-----------|
| Business stakeholders are available for requirement gathering and UAT. | Critical to shape dashboards correctly and validate. |
| Data access to all relevant sources will be granted timely. | Without this, development will be blocked. |
| Snowflake and Tableau infrastructure will be fully operational before dashboard development begins. | Prevents rework and avoids idle time for developers. |
| No major changes in business requirements once development starts. | Changing requirements could throw off the timeline. |
| Each dashboard can be built within 1–1.5 days on average. | Used for effort estimation; assumes moderate complexity. |

## Issues
| Issue | Impact | Resolution |
|-------|--------|------------|
| Tableau license provisioning may be delayed. | Tableau resource can't start building dashboards. | Coordinate with IT/license admin early to avoid delay. |
| Source system documentation may be outdated or missing. | Slows down data mapping and understanding. | Work closely with SMEs or data owners for clarity. |

## Dependencies
| Dependency | Description | Impact |
|------------|-------------|--------|
| **Business SME availability** | Needed during requirements, validation, and feedback. | Delays in their availability slow down entire project. |
| **IT/Infra team** | For provisioning Snowflake roles, Airflow pipelines, Tableau server access. | Any delays here affect dev start time. |
| **Access control setup** | Permissions for Snowflake, Tableau, and source systems. | Critical for both developers to start their work. |
| **JIRA board setup** | For tracking tasks and progress collaboratively. | Without it, project transparency and accountability suffer. |
