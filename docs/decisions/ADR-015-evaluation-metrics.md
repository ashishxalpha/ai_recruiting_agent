# ADR 015: Evaluation Metrics and Analytics Abstraction

## Context
We need to generate analytics (e.g., recruiter agreement rate, approval rate, interview rate) to evaluate the system. The data exists across Match, Feedback, and Ground Truth tables. As data grows, calculating this synchronously on every HTTP request will cause timeouts.

## Decision
1. Introduce an `AnalyticsProvider` abstraction.
2. Implement a `RealtimeAnalyticsProvider` that queries the relational tables dynamically for immediate use.
3. Prepare the interface to support a future `MaterializedAnalyticsProvider` that reads from pre-computed OLAP tables or materialized views.
4. Add robust metrics (Agreement Rate, Approval Rate, Interview Rate, Hire Rate, Average Processing Time, Average Latency).

## Consequences
- **Pros**: Clear abstraction protects the API layer from knowing how analytics are computed. Easy migration path to a data warehouse or materialized views later.
- **Cons**: Slight overhead in defining provider abstractions initially.
