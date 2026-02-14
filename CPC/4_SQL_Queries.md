They test:

1. Can you reason about large-scale data?
2. Can you write performant queries?
3. Do you understand query planning?
4. Can you handle edge cases?
5. Can you model business logic in SQL?
6. Can you debug production SQL problems?

Below is what you should realistically expect.

---

# 1️⃣ Advanced Aggregation & Window Functions

Very common.

### Example Question:

> Find the latest transaction per customer.

Strong answer:

```sql
SELECT *
FROM (
    SELECT 
        customer_id,
        transaction_id,
        transaction_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY transaction_date DESC
        ) AS rn
    FROM transactions
) t
WHERE rn = 1;
```

Principal-level explanation:

* Explain why `ROW_NUMBER()` over partition is better than correlated subqueries.
* Mention indexing on `(customer_id, transaction_date)` for performance.

---

# 2️⃣ Handling Slowly Changing Dimensions (SCD)

### Example:

> Retrieve customer attributes valid at transaction time.

```sql
SELECT t.*, d.customer_status
FROM transactions t
JOIN customer_dim d
  ON t.customer_id = d.customer_id
 AND t.transaction_date BETWEEN d.effective_date AND d.end_date;
```

Principal layer:

* Discuss SCD Type 2.
* Mention index on `(customer_id, effective_date)`.
* Explain why range joins can become expensive at scale.

---

# 3️⃣ De-duplication at Scale

### Example:

> Remove duplicate events keeping the most recent one.

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY event_id
               ORDER BY updated_at DESC
           ) AS rn
    FROM events
)
SELECT *
FROM ranked
WHERE rn = 1;
```

Principal insight:

* Discuss late-arriving data.
* Discuss idempotency.
* Mention partition pruning.

---

# 4️⃣ Complex Analytical Queries

### Example:

> Find customers whose 3-month rolling average spend increased continuously.

```sql
WITH monthly_spend AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', transaction_date) AS month,
        SUM(amount) AS total_spend
    FROM transactions
    GROUP BY 1,2
),
rolling AS (
    SELECT *,
        AVG(total_spend) OVER (
            PARTITION BY customer_id
            ORDER BY month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS rolling_avg
    FROM monthly_spend
)
SELECT *
FROM rolling;
```

Principal level:

* Discuss window frames.
* Talk about materialization strategy.
* Consider pre-aggregated tables.

---

# 5️⃣ Performance Debugging Question

They may show:

> This query is slow. Why?

```sql
SELECT *
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.country = 'UK';
```

Principal answer should mention:

* Missing index on `customer_id`
* Filter should be pushed before join
* Cardinality estimation
* Explain execution plan
* Data skew
* Join strategy (hash vs nested loop)

Not just “add index.”

---

# 6️⃣ Data Quality SQL

### Example:

> Identify customers with conflicting emails.

```sql
SELECT customer_id
FROM customers
GROUP BY customer_id
HAVING COUNT(DISTINCT email) > 1;
```

Principal layer:

* Discuss whether this is allowed business behavior.
* Mention need for canonical record.
* Consider normalization.

---

# 7️⃣ Partition Awareness Question

> Why is this query scanning entire table?

Principal answer:

* Partition key mismatch
* Predicate not aligned with partition
* Implicit casting preventing pruning
* OR conditions breaking optimization

This is where principal candidates shine.

---

# 8️⃣ Handling NULLs & Edge Cases

Example:

> Calculate retention rate.

Principal answer discusses:

* NULL semantics
* Division by zero
* Distinct vs non-distinct counts
* Time window correctness

---

# 9️⃣ Data Modeling Logic in SQL

Example:

> Flatten hierarchical data.

Using recursive CTE:

```sql
WITH RECURSIVE org_chart AS (
    SELECT id, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.id, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart;
```

Principal layer:

* Mention recursion depth limits
* Discuss alternatives in distributed engines

---

# 🔟 Query Design Trade-Off Question

They might ask:

> Would you compute this in SQL or Spark?

Strong answer:

* Depends on data size
* Depends on transformation complexity
* Depends on SLA
* Depends on cost

Principal answers are conditional, not absolute.

---

# What Makes Principal-Level SQL Answers Different?

Senior candidate:

* Writes correct query.

Principal candidate:

* Explains execution plan.
* Talks about performance.
* Mentions data distribution.
* Talks about cost.
* Discusses trade-offs.
* Mentions maintainability.

---

# ⚠️ Brutally Honest Reality

For Principal role:

They are not testing syntax.

They are testing:

* Do you understand how SQL runs under the hood?
* Can you reason about 10TB, not 10MB?
* Can you prevent production incidents?

---
