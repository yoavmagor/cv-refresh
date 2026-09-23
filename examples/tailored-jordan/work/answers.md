# Interview answers (simulated user: evals/fixtures/simulated-user-jordan.md)

## Current role: Harborlight Logistics (planned 14, answered 13, skipped 1)
Q1. Are you still at Harborlight Logistics? → Yes
Q2. Is "Senior Data Engineer" still your title? Any promotions? → Promoted: Senior Data Engineer Apr 2022 – Dec 2023, Data Engineering Team Lead since Jan 2024
Q3. In one line, what does Harborlight do and for whom? → B2B SaaS for freight visibility; mid-size shippers and carriers track shipments and ETAs
Q4. Team size and your position? → Tech lead / manager: I lead a team of 4 data engineers
Q5. Which groups do you work with most? → Data science, product, backend team
Q6. What do you own? → The data platform: ingestion of carrier GPS/telematics and shipment events, the lakehouse, dbt models, internal analytics
Q7. The 2-3 things you're proudest of there? → (1) Built the lakehouse on Databricks + Delta Lake, replaced Redshift, migrated 30 pipelines. (2) Near-real-time ETA events pipeline with Kinesis and Spark Structured Streaming. (3) Introduced dbt with tests, and data contracts with the backend team so schema changes stop breaking pipelines
Q8. Any numbers you know for those? → Lakehouse cut monthly warehouse cost by about 35%. ETA latency went from about 1 hour (batch) to under 5 minutes
Q9. Tools you use there? → Python, SQL, PySpark, Databricks, Delta Lake, dbt, Airflow (MWAA), AWS (S3, Kinesis, Lambda, Glue), Terraform (some), GitHub Actions, Docker
Q10. Which apply: mentoring, hiring, design docs, on-call, stakeholder management? → Mentoring, hiring (interviewed and hired 2 engineers), design docs, on-call
Q11. Your CV says "6 years of experience". What should it say now? → 10 years
Q12. Any awards, talks or patents from this role? → (skipped)
Q13. The posting asks for streaming with Kafka. Have you used Kafka? → No (Kinesis only)
Q14. The posting lists Kubernetes as a nice-to-have. Used it? → No

## Follow-ups (planned 4)
F1. The ~35%: is that the monthly cost of the warehouse? → Yes, monthly warehouse cost
F2. How many engineers do you mentor? → 2 junior engineers
F3. The data contracts: with which team? → The backend team
F4. Which of these projects happened after your promotion to Team Lead? → (skipped)

## Previous roles
Offered: Data Engineer, Quillstone Retail (2019–2022) · BI Developer, Pinecrest Health Analytics (2016–2018) → Chosen: Quillstone Retail

### Quillstone Retail (planned 4)
P1. The posting asks for Apache Spark. Did you use it at Quillstone? → Yes, Spark on EMR for about a year to process clickstream data
P2. Did you use dbt there? → No
P3. Any streaming work there? → (skipped)
P4. Anything the CV undersells about Quillstone? → (skipped)
