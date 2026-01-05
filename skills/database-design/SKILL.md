---
name: database-design
description: Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. Teaches thinking, not fixed SQL.
---

# Database Design

> Database design principles and decision-making for 2025.
> **Learn to THINK, not copy SQL patterns.**

---

## ⚠️ How to Use This Skill

This skill teaches **decision-making principles**, not fixed SQL to copy.

- ASK user for database preferences when unclear
- Choose database/ORM based on CONTEXT
- Don't default to PostgreSQL for everything

---

## 1. Database Selection (2025)

### Decision Tree

```
What are your requirements?
│
├── Full relational features needed
│   ├── Self-hosted → PostgreSQL
│   └── Serverless → Neon, Supabase
│
├── Edge deployment / Ultra-low latency
│   └── Turso (edge SQLite)
│
├── AI / Vector search
│   └── PostgreSQL + pgvector
│
├── Simple / Embedded / Local
│   └── SQLite
│
└── Global distribution
    └── PlanetScale, CockroachDB, Turso
```

### Comparison Principles

| Database | Best For | Trade-offs |
|----------|----------|------------|
| **PostgreSQL** | Full features, complex queries | Needs hosting |
| **Neon** | Serverless PG, branching | PostgreSQL complexity |
| **Turso** | Edge, low latency | SQLite limitations |
| **SQLite** | Simple, embedded, local | Single-writer |
| **PlanetScale** | MySQL, global scale | No foreign keys |

### Selection Questions to Ask:
1. What's the deployment environment?
2. How complex are the queries?
3. Is edge/serverless important?
4. Vector search needed?
5. Global distribution required?

---

## 2. ORM Selection (2025)

### Decision Tree

```
What's the context?
│
├── Edge deployment / Bundle size matters
│   └── Drizzle (smallest, SQL-like)
│
├── Best DX / Schema-first
│   └── Prisma (migrations, studio)
│
├── Maximum control
│   └── Raw SQL with query builder
│
└── Python ecosystem
    └── SQLAlchemy 2.0 (async support)
```

### Comparison Principles

| ORM | Best For | Trade-offs |
|-----|----------|------------|
| **Drizzle** | Edge, TypeScript | Newer, less examples |
| **Prisma** | DX, schema management | Heavier, not edge-ready |
| **Kysely** | Type-safe SQL builder | Manual migrations |
| **Raw SQL** | Complex queries, control | Manual type safety |

---

## 3. Schema Design Principles

### Normalization Decision

```
When to normalize (separate tables):
├── Data is repeated across rows
├── Updates would need multiple changes
├── Relationships are clear
└── Query patterns benefit

When to denormalize (embed/duplicate):
├── Read performance critical
├── Data rarely changes
├── Always fetched together
└── Simpler queries needed
```

### Primary Key Selection

| Type | Use When |
|------|----------|
| **UUID** | Distributed systems, security (no guessing) |
| **ULID** | UUID + sortable by time |
| **Auto-increment** | Simple apps, single database |
| **Natural key** | Rarely (business meaning, careful!) |

### Timestamp Strategy

```
For every table, consider:
├── created_at → When record was created
├── updated_at → Last modification time
└── deleted_at → Soft delete (if needed)

Use TIMESTAMPTZ (with timezone) not TIMESTAMP
```

---

## 4. Indexing Principles

### When to Create Indexes

```
Index these:
├── Columns in WHERE clauses
├── Columns in JOIN conditions
├── Columns in ORDER BY
├── Foreign key columns
└── Unique constraints

Don't over-index:
├── Write-heavy tables (slower inserts)
├── Low-cardinality columns
├── Columns rarely queried
```

### Index Type Selection

| Type | Use For |
|------|---------|
| **B-tree** | General purpose, equality & range |
| **Hash** | Equality only, faster |
| **GIN** | JSONB, arrays, full-text |
| **GiST** | Geometric, range types |
| **HNSW/IVFFlat** | Vector similarity (pgvector) |

### Composite Index Principles

```
Order matters for composite indexes:
├── Equality columns first
├── Range columns last
├── Most selective first
└── Match query pattern
```

---

## 5. Query Optimization Principles

### N+1 Problem

```
What is N+1?
├── 1 query to get parent records
├── N queries to get related records (for each parent)
└── Very slow!

Solutions:
├── JOIN → Single query with all data
├── Eager loading → ORM handles JOIN
├── DataLoader → Batch and cache (GraphQL)
└── Subquery → Fetch related in one query
```

### Query Analysis Mindset

```
Before optimizing:
├── EXPLAIN ANALYZE the query
├── Look for Seq Scan (full table scan)
├── Check actual vs estimated rows
└── Identify missing indexes
```

### Optimization Priorities

1. **Add missing indexes** (most common issue)
2. **Select only needed columns** (not SELECT *)
3. **Use proper JOINs** (avoid subqueries when possible)
4. **Limit early** (pagination at database level)
5. **Cache** (when appropriate)

---

## 6. Migration Principles

### Safe Migration Strategy

```
For zero-downtime changes:
│
├── Adding column
│   └── Add as nullable → backfill → add NOT NULL
│
├── Removing column
│   └── Stop using → deploy → remove column
│
├── Adding index
│   └── CREATE INDEX CONCURRENTLY (non-blocking)
│
└── Renaming column
    └── Add new → migrate data → deploy → drop old
```

### Migration Philosophy

- Never make breaking changes in one step
- Test migrations on data copy first
- Have rollback plan
- Run in transaction when possible

---

## 7. Vector Database (AI/Embeddings)

### When to Use pgvector

```
Use pgvector when:
├── Already using PostgreSQL
├── Moderate vector dataset (<1M vectors)
├── Need SQL + vector in same query
└── Don't want separate vector service
```

### Alternative Vector Solutions

| Solution | Best For |
|----------|----------|
| **pgvector** | Integrated with PostgreSQL |
| **Pinecone** | Fully managed, large scale |
| **Qdrant** | Self-hosted, performance |
| **Weaviate** | Semantic search, GraphQL |

---

## 8. Serverless Database Principles

### Neon (Serverless PostgreSQL)

```
Benefits:
├── Scale to zero (cost savings)
├── Instant branching (dev/preview)
├── Full PostgreSQL compatibility
└── Autoscaling

Best for:
├── Variable traffic
├── Development workflows
├── Preview environments
└── Cost-conscious deployments
```

### Turso (Edge SQLite)

```
Benefits:
├── Ultra-low latency (edge locations)
├── SQLite compatibility
├── Generous free tier
└── Simple setup

Best for:
├── Edge functions
├── Read-heavy workloads
├── Simple data needs
└── Global distribution
```

---

## 9. Relationship Design Principles

### Relationship Types

| Type | When | Implementation |
|------|------|---------------|
| **One-to-One** | Extension data | Separate table with FK |
| **One-to-Many** | Parent-children | FK on child table |
| **Many-to-Many** | Both sides have many | Junction table |

### Foreign Key Principles

```
ON DELETE options:
├── CASCADE → Delete children with parent
├── SET NULL → Children become orphans
├── RESTRICT → Prevent delete if children exist
└── SET DEFAULT → Children get default value

Choose based on business logic, not convenience
```

---

## 10. Decision Checklist

Before designing schema:

- [ ] **Asked user about database preference?**
- [ ] **Chosen database for THIS context?** (not just default)
- [ ] **Considered deployment environment?**
- [ ] **Planned index strategy?**
- [ ] **Defined relationship types?**
- [ ] **Considered migration strategy?**
- [ ] **Evaluated serverless options?**

---

## 11. Anti-Patterns to Avoid

### ❌ DON'T:
- Default to PostgreSQL for simple apps (SQLite may suffice)
- Skip indexing (then wonder why queries are slow)
- Use SELECT * in production
- Store JSON when structured data is better
- Create indexes on every column
- Ignore N+1 queries
- Hard-delete when soft-delete is better

### ✅ DO:
- Choose database based on context
- Ask about deployment requirements
- Plan indexes based on query patterns
- Use EXPLAIN ANALYZE before optimizing
- Design for evolution

---

> **Remember**: Database design is about making decisions for YOUR specific use case. Don't copy schemas—think about what serves your application best.
