---
name: backend-design
description: Elite Tier Backend standards, including Vertical Slice Architecture, Zero Trust Security, and High-Performance API protocols.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

<domain_overview>
# Backend Design System

> **Philosophy:** The Backend is the Fortress. Logic is Law. Latency is the Enemy.
> **Core Principle:** ISOLATE features. TRUST no one. SCALE linearly.

**ANTI-HAPPY PATH MANDATE (CRITICAL):** Never assume the ideal scenario. AI-generated code often fails by ignoring edge cases and failure modes. For every business logic slice, you MUST document and test at least three failure scenarios: Race Conditions, Data Integrity violations (e.g., unique constraint overlaps), and Boundary failures. Reject any implementation that only covers the 'Happy Path'. Engineering is the art of handling what shouldn't happen.
</domain_overview>

<architectural_protocols>
## 🚀 ELITE TIER KNOWLEDGE (ARCHITECTURAL PROTOCOLS)

### 0. The "Vertical Slice" Law (The Anti-Layer Mandate)
> **CRITICAL:** You are FORBIDDEN from creating "Horizontal Layers" (Controllers, Services, Repositories) as primary folders.

**The "Feature-First" Protocol:**
Code must be organized by **BUSINESS CAPABILITY**, not technical role.
1.  **The Slice:** A single directory (e.g., `features/create-order/`) contains EVERYTHING needed for that feature:
    *   `handler.ts` (Controller)
    *   `logic.ts` (Domain/Service)
    *   `schema.ts` (DTO/Validation)
    *   `db.ts` (Data Access)
2.  **The Benefit:** Changing a feature requires touching only ONE folder. No "Shotgun Surgery" across 5 layers.
3.  **Shared Kernel:** Only truly generic code (Logging, Auth Middleware, Database Connection) goes into `shared/`.

### 1. The "Modular Monolith" Mandate
*   **Microservices Ban:** Do NOT start with microservices. Start with a **Modular Monolith**.
*   **Modulith Rules:**
    *   Modules must be isolated (like internal microservices).
    *   Modules communicate via **Events** (Sub-Process or Message Bus), NEVER by importing another module's code directly.
    *   **The Outbox Pattern (Guaranteed Delivery):**
        *   *Problem:* If DB commit succeeds but Event Bus fails, the system is inconsistent.
        *   *Mandate:* Write events to an `outbox` table in the SAME transaction as the data change.
        *   *Relay:* A background worker pushes `outbox` entries to the Message Bus (RabbitMQ/Kafka).
    *   Data Sovereignty: Module A cannot query Module B's tables. It must ask Module B via API/Event.

### 2. The "Zero Trust" Security Protocol
> **Detailed protocols:** See [security-protocols.md](security-protocols.md)

**Quick Rules:**
1. **Strict Serialization:** NEVER return raw DB entities → Use ResponseDTO
2. **Validation at Gate:** Schema validation (Zod/Pydantic) BEFORE logic
3. **Token Sovereignty:** PASETO v4 > JWT (Ed25519 if JWT forced)
</architectural_protocols>

<reliability_contracts>
## 🏗️ Reliability & Performance Contracts

### 3. The "Sub-100ms" Performance Mandate
*   **The Latency Budget:** P50 < 100ms. P99 < 500ms.
*   **UUIDv7 (The Time-Lord Rule):**
    *   *Ban:* Never use `UUIDv4` (Random) for Primary Keys. It fragments B-Tree indexes.
    *   *Mandate:* Use **UUIDv7** (Time-ordered). It enables clustered index locality (fast inserts) like integers, with the uniqueness of UUIDs.
*   **N+1 Assassin:**
    *   *Check:* Always inspect ORM queries. Loops triggering DB calls are a "Level 0" error.
    *   *Fix:* Use `DataLoader` pattern or explicit `JOIN` loading.

### 4. API Reliability Contracts
*   **RFC 7807 (Problem Details):**
    *   *Ban:* returning `{ "error": "Something went wrong" }`.
    *   *Mandate:* Return standard Problem JSON:
        ```json
        {
          "type": "https://api.myapp.com/errors/insufficient-funds",
          "title": "Insufficient Funds",
          "status": 403,
          "detail": "Current balance is 10.00, required is 15.00",
          "instance": "/transactions/12345"
        }
        ```
*   **Idempotency Keys:**
    *   *Rule:* All critical `POST/PATCH` (Money, State Change) must accept an `Idempotency-Key` header.
    *   *Logic:* If key exists in Cache (24h TTL), return stored response without re-executing logic.
</reliability_contracts>

<database_integrity>
## 🗄️ Database Integrity & Design

### 5. Database Integrity & Design
*   **Hard Constraints:** Application-level checks are "Suggestions". Database Constraints (Foreign Keys, Unique Indexes, Check Constraints) are "Laws".
*   **Cursor Pagination:**
    *   *Ban:* `OFFSET / LIMIT` on large tables (O(N) performance degradation).
    *   *Mandate:* Cursor-based pagination (`WHERE created_at < cursor LIMIT 20`).
*   **Migration Discipline:**
    *   Never alter a column in a way that locks the table for >1s.
    *   Use "Expand and Contract" pattern for breaking changes.
*   **Concurrency Control:**
    *   *Problem:* Two users update the same record. The last one wipes the first.
    *   *Mandate:* Use Optimistic Locking. Add a `version` (int) column.
    *   *Logic:* Update WHERE `id` = X AND `version` = Y. If 0 rows affected, throw `StaleObjectException`.

### 6. AI & Vector Readiness
*   **Semantic Storage:** Backend must be ready to store embeddings (Vector Types).
*   **Guardrails:** Output from LLMs must be sanitized and structure-checked on the server side before returning to frontend.
</database_integrity>

<observability>
## 👁️ Observability & Monitoring (The "Glass Box" Protocol)

### 7. Structured Logging Only
*   **Ban:** `console.log("User updated")`. String logs are useless for machines.
*   **Mandate:* JSON Logs with correlation IDs. `{ "level": "info", "event": "user_updated", "user_id": "u7-...", "trace_id": "..." }`.

### 8. Distributed Tracing (OpenTelemetry)
*   Every request MUST carry a `traceparent` header.
*   Spans must cover: DB Queries, External API Calls, and Redis operations.

### 9. Health Checks
*   Liveness (`/health/live`): "Am I running?" (Instant, no checks).
*   Readiness (`/health/ready`): "Can I take traffic?" (Check DB/Redis connection).
</observability>

<resilience>
## 🛡️ Resilience Patterns (The "Anti-Fragile" Mandate)

### 10. Circuit Breakers
*   Wrap ALL external calls (Payment Gateways, 3rd Party APIs) in a Circuit Breaker.
*   *Logic:* After 5 failures, fail fast for 30s. Don't drown the downstream service.

### 11. Rate Limiting
*   Protect *every* public endpoint with a Token Bucket rate limiter (Redis-backed).
*   Differentiate limits by User Role (Anon: 60/min, Pro: 1000/min).
</resilience>

<workflow_rules>
## 🔧 Workflow Rules

### 1. The Pre-Flight Checklist
0.  **Environment Hardening:**
    *   Verify all `process.env` variables at startup using a schema (e.g., `t3-env` or `envalid`). If a key is missing, crash immediately. Do not start the server in an undefined state.
Before writing a single handler:
1.  **Define the DTOs:** Request Schema (Zod) and Response Schema.
2.  **Define the Error States:** What can go wrong? (404, 409, 429).
3.  **Define the Data Access:** What is the most efficient SQL query?

### 2. The "No Magic" Rule
*   Avoid "Magical" ORM features (Lazy Loading, Auto-Saving context).
*   Prefer Explicit over Implicit. "Write the SQL (or Query Builder) if the ORM hides expensive logic."

### 3. Testing Pyramid
1.  **Unit:** Test Domain Logic in isolation (mock DB).
2.  **Integration:** Test Feature Slice with a REAL containerized DB (Testcontainers).
3.  **E2E:** Test critical flows from the "Outside".
</workflow_rules>

<audit_and_reference>
## 📂 Cognitive Audit Cycle
Before committing code:
1.  **Is the endpoint under a feature slice?** (Not in a generic controller folder).
2.  **Is Input Validated with a Schema?** (Zero Trust).
3.  **Are DB Indexes used?** (Run `EXPLAIN ANALYZE`).
4.  **Is the Primary Key UUIDv7?** (Index Perf).
5.  **Are secrets managed properly?** (No hardcoded strings).

---

## 🔗 CROSS-SKILL INTEGRATION

| Skill | Backend Adds... |
|-------|-----------------|
| `@frontend-design` | API contracts, CORS config, error responses |
| `@clean-code` | Input validation, no raw SQL, dependency security |
| `@tdd-mastery` | Integration tests with Testcontainers |
| `@planning-mastery` | API endpoint task breakdown |
| `@debug-mastery` | Structured logging, distributed tracing |

> **Command:** Use these skills to architect "Fortress-Level" backend systems.
</audit_and_reference>
