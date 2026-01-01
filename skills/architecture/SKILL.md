---
name: architecture
description: Architectural reasoning framework: requirements analysis, trade-off evaluation, and ADR-based decision documentation. NOT a pattern catalog, but a thinking framework. Use when designing system architecture, choosing patterns, or making structural decisions.
---

# Architecture Decision Framework

## Core Philosophy

**"Requirements drive architecture. Trade-offs inform decisions. ADRs capture rationale."**

Architecture is NOT about applying patterns. It's about solving problems within constraints.

---

## Phase 1: Context Discovery

### Question Hierarchy (Ask User FIRST)

Before suggesting any architecture, gather context:

1. **Scale**
   - How many users? (10, 1K, 100K, 1M+)
   - Data volume? (MB, GB, TB)
   - Transaction rate? (per second/minute)

2. **Team**
   - Solo developer or team?
   - Team size and expertise?
   - Distributed or co-located?

3. **Timeline**
   - MVP/Prototype or long-term product?
   - Time to market pressure?

4. **Domain**
   - CRUD-heavy or business logic complex?
   - Real-time requirements?
   - Compliance/regulations?

5. **Constraints**
   - Budget limitations?
   - Legacy systems to integrate?
   - Technology stack preferences?

### Project Classification Matrix

```
                    MVP              SaaS           Enterprise
┌─────────────────────────────────────────────────────────────┐
│ Scale        │ <1K           │ 1K-100K      │ 100K+        │
│ Team         │ Solo          │ 2-10         │ 10+          │
│ Timeline     │ Fast (weeks)  │ Medium (months)│ Long (years)│
│ Architecture │ Simple        │ Modular      │ Distributed  │
│ Patterns     │ Minimal       │ Selective    │ Comprehensive│
│ Example      │ Next.js API   │ NestJS       │ Microservices│
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Trade-off Analysis

### Decision Framework

For EACH architectural component, document:

```markdown
## Architecture Decision Record

### Context
- **Problem**: [What problem are we solving?]
- **Constraints**: [Team size, scale, timeline, budget]

### Options Considered

| Option | Pros | Cons | Complexity | When Valid |
|--------|------|------|------------|-----------|
| Option A | Benefit 1 | Cost 1 | Low | [Conditions] |
| Option B | Benefit 2 | Cost 2 | High | [Conditions] |
| Option C | Benefit 3 | Cost 3 | Medium | [Conditions] |

### Decision
**Chosen**: [Option B]

### Rationale
1. [Reason 1 - tied to constraints]
2. [Reason 2 - tied to requirements]
3. [Reason 3 - trade-off accepted]

### Trade-offs Accepted
- [What we're giving up]
- [Why this is acceptable given constraints]

### Consequences
- **Positive**: [Benefits we gain]
- **Negative**: [Costs/risks we accept]
- **Mitigation**: [How we'll address negatives]

### Revisit Trigger
- [When to reconsider this decision]
```

---

## Phase 3: Pattern Selection Guidelines

### NOT a Checklist - But Decision Trees

```
START: What's your MAIN concern?

┌─ Data Access Complexity?
│  ├─ HIGH (complex queries, testing needed, multiple data sources)
│  │  → Repository Pattern + Unit of Work
│  │  VALIDATE: Will data source change frequently?
│  │     ├─ YES → Repository worth the indirection
│  │     └─ NO  → Consider simpler ORM direct access
│  └─ LOW (simple CRUD, single database)
│     → ORM directly (TypeORM, Prisma, Sequelize, etc.)
│     Simpler = Better, Faster
│
├─ Business Rules Complexity?
│  ├─ HIGH (domain logic, rules vary by context)
│  │  → Domain-Driven Design
│  │  VALIDATE: Do you have domain experts on team?
│  │     ├─ YES → Full DDD (Aggregates, Value Objects, Domain Events)
│  │     └─ NO  → Partial DDD (rich entities, clear boundaries)
│  └─ LOW (mostly CRUD, simple validation)
│     → Transaction Script pattern
│     Simpler = Better, Faster
│
├─ Independent Scaling Needed?
│  ├─ YES (different components scale differently)
│  │  → Microservices WORTH the complexity
│  │  REQUIREMENTS (ALL must be true):
│  │    - Clear domain boundaries (bounded contexts)
│  │    - Team > 10 developers (otherwise overhead too high)
│  │    - Different scaling/timeline needs per service
│  │  IF NOT ALL MET → Modular Monolith instead
│  └─ NO (everything scales together)
│     → Modular Monolith
│     Can extract services later when proven needed
│
└─ Real-time Requirements?
   ├─ HIGH (immediate updates, multi-user sync)
   │  → Event-Driven Architecture
   │  → Message Queue (RabbitMQ, Redis, Kafka)
   │  VALIDATE: Can you handle eventual consistency?
   │     ├─ YES → Event-driven valid
   │     └─ NO  → Consider synchronous with polling
   └─ LOW (eventual consistency acceptable)
      → Synchronous (REST/GraphQL)
      Simpler = Better, Faster
```

---

## Phase 4: Validation - The Simplicity Test

### The 3 Questions

Before applying ANY pattern, ask:

1. **Problem Solved**: What SPECIFIC problem does this pattern solve?
2. **Simpler Alternative**: Is there a simpler solution?
3. **Deferred Complexity**: Can we add this LATER when needed?

### Red Flags (Anti-patterns to Avoid)

| Pattern | Anti-pattern | Why Bad | Simpler Alternative |
|---------|-------------|---------|-------------------|
| Microservices | Premature splitting | Adds complexity before proving value | Start monolith, extract when needed |
| Clean/Hexagonal | Over-abstraction | Hard to understand, debug, onboard | Concrete first, extract interfaces later |
| Event Sourcing | Over-engineering | Complex debugging, temporal coupling | Append-only audit log |
| CQRS | Unnecessary complexity | Two models to maintain, sync issues | Single model until read/write diverge significantly |
| Repository | YAGNI for simple CRUD | Extra layer without benefit | ORM direct access |

### Simplicity Principle

**"Simplicity is the ultimate sophistication."**

- Start simple
- Add complexity ONLY when proven necessary
- You can always add patterns later
- Removing complexity is MUCH harder than adding it

---

## Phase 5: Document & Communicate

### ADR Template

Every architectural decision MUST be documented:

```markdown
# ADR-[XXX]: [Decision Title]

## Status
Proposed | Accepted | Deprecated | Superseded by [ADR-YYY]

## Context
[What problem are we solving? What constraints exist?]

## Decision
[What we chose - be specific]

## Rationale
[Why this decision - tie back to requirements and constraints]

## Trade-offs
[What we're giving up - be honest about costs]

## Consequences
- **Positive**: [Benefits we gain]
- **Negative**: [Costs/risks we accept]
- **Mitigation**: [How we'll address the negatives]
```

### ADR Storage

Create `docs/architecture/adr-*.md` files:

```
docs/
└── architecture/
    ├── adr-001-use-nextjs.md
    ├── adr-002-postgresql-over-mongodb.md
    ├── adr-003-adopt-repository-pattern.md
    └── adr-004-add-redis-caching.md
```

---

## Examples by Project Type

### Example 1: MVP E-commerce (Solo Developer)

```yaml
Requirements:
  - <1000 users initially
  - Solo developer
  - Fast to market (8 weeks)
  - Budget-conscious

Architecture Decisions:

┌────────────────────────────────────────────────────────────┐
│ Decision               │ Choice        │ Rationale          │
├────────────────────────────────────────────────────────────┤
│ App Structure          │ Monolith      │ Simpler for solo   │
│ Framework              │ Next.js       │ Full-stack, fast   │
│ Data Layer             │ Prisma direct │ No Repo over-abstr │
│ File Storage           │ Local/S3      │ Start local        │
│ Authentication         │ JWT           │ Simpler than OAuth │
│ Payment                │ Stripe        │ Hosted solution    │
│ Database               │ PostgreSQL    │ ACID for orders    │
└────────────────────────────────────────────────────────────┘

Trade-offs Accepted:
- Monolith → Can't scale components independently
  Why: Team size doesn't justify microservices overhead
- No Repository → Less testable data layer
  Why: Simple CRUD doesn't need indirection
- JWT → No social login initially
  Why: Faster implementation, can add OAuth later

Future Migration Path:
- When users > 10K → Extract payment service
- When team > 3 → Add Repository pattern
- When social login requested → Add OAuth provider
```

### Example 2: SaaS Product (5-10 Developers)

```yaml
Requirements:
  - 1K-100K users
  - 5-10 developers
  - Long-term product (12+ months)
  - Multiple domains (billing, users, core)

Architecture Decisions:

┌────────────────────────────────────────────────────────────┐
│ Decision               │ Choice          │ Rationale         │
├────────────────────────────────────────────────────────────┤
│ App Structure          │ Modular Monolith│ Team size optimal │
│ Framework              │ NestJS          │ Modular by design │
│ Data Layer             │ Repository      │ Testing, flex     │
│ Domain Model           │ Partial DDD     │ Rich entities     │
│ Authentication         │ OAuth + JWT     │ Social login      │
│ Caching                │ Redis           │ Performance       │
│ Database               │ PostgreSQL      │ ACID, reliable    │
│ Message Queue          │ RabbitMQ (later)│ When async needed │
└────────────────────────────────────────────────────────────┘

Trade-offs Accepted:
- Modular Monolith → Some coupling between modules
  Why: Microservices overhead not justified yet
- Partial DDD → Not full aggregates/domain events
  Why: No domain experts, rich entities sufficient
- RabbitMQ later → Initial synchronous calls
  Why: Add complexity when async proven needed

Migration Path:
- When team > 10 → Consider microservices
- When domains conflict → Extract bounded contexts
- When read performance issues → Add CQRS
```

### Example 3: Enterprise (100K+ Users)

```yaml
Requirements:
  - 100K+ users
  - 10+ developers
  - Multiple business domains
  - Different scaling needs per domain
  - 24/7 availability required

Architecture Decisions:

┌────────────────────────────────────────────────────────────┐
│ Decision               │ Choice          │ Rationale         │
├────────────────────────────────────────────────────────────┤
│ App Structure          │ Microservices   │ Independent scale │
│ API Gateway            │ Kong/AWS API GW │ Routing, auth     │
│ Domain Model           │ Full DDD        │ Complex business │
│ Data Consistency       │ Event-driven    │ Eventual OK       │
│ Message Bus            │ Kafka           │ High throughput   │
│ Authentication         │ OAuth + SAML    │ Enterprise SSO    │
│ Database              │ Polyglot        │ Right tool per job│
│ CQRS                  │ Selected services│ Read/write diverge│
│ Observability          │ Full stack      │ Debugging complex │
└────────────────────────────────────────────────────────────┘

Trade-offs Accepted:
- Microservices → High operational complexity
  Why: Different scaling needs justify cost
- Eventual Consistency → Complex debugging
  Why: Real-time not required everywhere
- Polyglot Persistence → More expertise needed
  Why: Different domains have different needs

Operational Requirements:
- Service mesh (Istio/Linkerd)
- Distributed tracing (Jaeger/Tempo)
- Centralized logging (ELK/Loki)
- Circuit breakers (Resilience4j)
- Deployment automation (Kubernetes/Helm)
```

---

## Common Architecture Patterns Reference

### Data Access Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Active Record** | Simple CRUD, rapid prototyping | Complex queries, multiple data sources | Low |
| **Repository** | Testing needed, multiple data sources | Simple CRUD, single database | Medium |
| **Unit of Work** | Complex transactions, consistency | Simple operations | High |
| **Data Mapper** | Complex domain logic, performance | Simple CRUD, rapid dev | High |

### Domain Logic Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Transaction Script** | Simple CRUD, procedural | Complex business rules | Low |
| **Table Module** | Record-based logic, simple domain | Rich behavior needed | Low |
| **Domain Model** | Complex business logic | Simple CRUD | Medium |
| **DDD (Full)** | Complex domain, domain experts | Simple domain, no experts | High |

### Distributed System Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **Modular Monolith** | Small teams, unclear boundaries | Clear bounded contexts, different scales | Medium |
| **Microservices** | Different scales, large teams | Small teams, simple domain | Very High |
| **Event-Driven** | Real-time, loose coupling | Simple workflows, strong consistency | High |
| **CQRS** | Read/write performance diverges | Simple CRUD, same model | High |
| **Saga** | Distributed transactions | Single database, simple ACID | High |

### API Patterns

| Pattern | When to Use | When NOT to Use | Complexity |
|---------|-------------|-----------------|------------|
| **REST** | Standard CRUD, resources | Real-time, complex queries | Low |
| **GraphQL** | Flexible queries, multiple clients | Simple CRUD, caching needs | Medium |
| **gRPC** | Internal services, performance | Public APIs, browser clients | Medium |
| **WebSocket** | Real-time updates | Simple request/response | Medium |

---

## Validation Checklist

Before finalizing architecture, verify:

- [ ] Requirements clearly understood and documented
- [ ] Constraints identified and accepted
- [ ] Each decision has trade-off analysis
- [ ] Simpler alternatives considered
- [ ] ADRs written for significant decisions
- [ ] Migration path documented (if needed)
- [ ] Team expertise matches chosen patterns
- [ ] Operational complexity is manageable

---

## Final Principle

**"Simplicity is the ultimate sophistication. Start simple, add complexity only when proven necessary."**

### When in Doubt

1. Choose the simpler option
2. Defer complexity until proven needed
3. Document the decision (ADR)
4. Set revisit triggers
5. Stay pragmatic over dogmatic

---

## Related Skills

- [database-design](../database-design/SKILL.md) - Database schema design
- [api-patterns](../api-patterns/SKILL.md) - API design patterns
- [deployment-procedures](../deployment-procedures/SKILL.md) - Deployment architecture
