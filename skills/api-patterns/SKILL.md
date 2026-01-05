---
name: api-patterns
description: API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. Teaches thinking, not fixed patterns.
---

# API Patterns

> API design principles and decision-making for 2025.
> **Learn to THINK, not copy fixed patterns.**

---

## ⚠️ How to Use This Skill

This skill teaches **decision-making principles**, not fixed JSON to copy.

- ASK user for API style preference when unclear
- Choose pattern based on CONTEXT and clients
- Don't default to REST for everything

---

## 1. API Style Selection (2025)

### Decision Tree

```
Who are the API consumers?
│
├── Public API / Multiple platforms
│   └── REST + OpenAPI (widest compatibility)
│
├── Complex data needs / Multiple frontends
│   └── GraphQL (flexible queries)
│
├── TypeScript frontend + backend (monorepo)
│   └── tRPC (end-to-end type safety)
│
├── Real-time / Event-driven
│   └── WebSocket + AsyncAPI
│
└── Internal microservices
    └── gRPC (performance) or REST (simplicity)
```

### Comparison Principles

| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| **Best for** | Public APIs | Complex apps | TS monorepos |
| **Learning curve** | Low | Medium | Low (if TS) |
| **Over/under fetching** | Common | Solved | Solved |
| **Type safety** | Manual (OpenAPI) | Schema-based | Automatic |
| **Caching** | HTTP native | Complex | Client-based |
| **Tooling** | Extensive | Good | TS only |

### Selection Questions to Ask:
1. Who are the API consumers?
2. Is the frontend TypeScript?
3. How complex are the data relationships?
4. Is caching critical?
5. Public or internal API?

---

## 2. REST Principles (Not Fixed JSON)

### Resource Naming Rules

```
Principles:
├── Use NOUNS, not verbs (resources, not actions)
├── Use PLURAL forms (/users not /user)
├── Use lowercase with hyphens (/user-profiles)
├── Nest for relationships (/users/123/posts)
└── Keep shallow (max 3 levels deep)
```

### HTTP Method Selection

| Method | Purpose | Idempotent? | Body? |
|--------|---------|-------------|-------|
| **GET** | Read resource(s) | Yes | No |
| **POST** | Create new resource | No | Yes |
| **PUT** | Replace entire resource | Yes | Yes |
| **PATCH** | Partial update | No | Yes |
| **DELETE** | Remove resource | Yes | No |

### Status Code Selection Guide

| Situation | Code | Why |
|-----------|------|-----|
| Success (read) | 200 | Standard success |
| Created | 201 | New resource created |
| No content | 204 | Success, nothing to return |
| Bad request | 400 | Malformed request |
| Unauthorized | 401 | Missing/invalid auth |
| Forbidden | 403 | Valid auth, no permission |
| Not found | 404 | Resource doesn't exist |
| Conflict | 409 | State conflict (duplicate) |
| Validation error | 422 | Valid syntax, invalid data |
| Rate limited | 429 | Too many requests |
| Server error | 500 | Our fault |

---

## 3. Response Format Principles

### Consistency is Key

```
Choose a format and STICK TO IT across entire API.

Common patterns:
├── Envelope pattern ({ success, data, error })
├── Direct data (just return the resource)
└── HAL/JSON:API (hypermedia)
```

### Error Response Principles

```
Include:
├── Error code (for programmatic handling)
├── User message (for display)
├── Details (for debugging, field-level errors)
├── Request ID (for support)
└── NOT internal details (security!)
```

### Pagination Principles

| Type | Best For | Trade-offs |
|------|----------|------------|
| **Offset** | Simple, jumpable | Performance on large datasets |
| **Cursor** | Large datasets | Can't jump to page |
| **Keyset** | Performance critical | Requires sortable key |

### Selection Questions:
1. How large is the dataset?
2. Do users need to jump to specific pages?
3. Is data frequently changing?

---

## 4. GraphQL Principles

### When to Use GraphQL

```
✅ Good fit:
├── Complex, interconnected data
├── Multiple frontend platforms
├── Clients need flexible queries
├── Evolving data requirements
└── Reducing over-fetching matters

❌ Poor fit:
├── Simple CRUD operations
├── File upload heavy
├── HTTP caching important
└── Team unfamiliar with GraphQL
```

### Schema Design Principles

```
Principles:
├── Think in graphs, not endpoints
├── Design for evolvability (no versions)
├── Use connections for pagination
├── Be specific with types (not generic "data")
└── Handle nullability thoughtfully
```

### Security Considerations

```
Protect against:
├── Query depth attacks → Set max depth
├── Query complexity → Calculate cost
├── Batching abuse → Limit batch size
├── Introspection → Disable in production
```

---

## 5. tRPC Principles

### When to Use tRPC

```
✅ Perfect fit:
├── TypeScript on both ends
├── Monorepo structure
├── Internal tools
├── Rapid development
└── Type safety critical

❌ Poor fit:
├── Non-TypeScript clients
├── Public API
├── Need REST conventions
└── Multiple language backends
```

### Key Benefits

```
Why tRPC:
├── Zero schema maintenance
├── End-to-end type inference
├── IDE autocomplete across stack
├── Instant API changes reflected
└── No code generation step
```

### Integration Patterns

```
Common setups:
├── Next.js + tRPC (most common)
├── Monorepo with shared types
├── Remix + tRPC
└── Any TS frontend + backend
```

---

## 6. Versioning Strategies

### Decision Factors

| Strategy | Implementation | Trade-offs |
|----------|---------------|------------|
| **URI** | /v1/users | Clear, easy caching |
| **Header** | Accept-Version: 1 | Cleaner URLs, harder discovery |
| **Query** | ?version=1 | Easy to add, messy |
| **None** | Evolve carefully | Best for internal, risky for public |

### Versioning Philosophy

```
Consider:
├── Public API? → Version in URI
├── Internal only? → May not need versioning
├── GraphQL? → Typically no versions (evolve schema)
├── tRPC? → Types enforce compatibility
```

---

## 7. Authentication Patterns

### Selection Guide

| Pattern | Best For |
|---------|----------|
| **JWT** | Stateless, microservices |
| **Session** | Traditional web, simple |
| **OAuth 2.0** | Third-party integration |
| **API Keys** | Server-to-server, public APIs |
| **Passkey** | Modern passwordless (2025+) |

### JWT Principles

```
Important:
├── Always verify signature
├── Check expiration
├── Include minimal claims
├── Use short expiry + refresh tokens
└── Never store sensitive data in JWT
```

---

## 8. Rate Limiting Principles

### Why Rate Limit

```
Protect against:
├── Brute force attacks
├── Resource exhaustion
├── Cost overruns (if pay-per-use)
└── Unfair usage
```

### Strategy Selection

| Type | How | When |
|------|-----|------|
| **Token bucket** | Burst allowed, refills over time | Most APIs |
| **Sliding window** | Smooth distribution | Strict limits |
| **Fixed window** | Simple counters per window | Basic needs |

### Response Principles

```
Include in headers:
├── X-RateLimit-Limit (max requests)
├── X-RateLimit-Remaining (requests left)
├── X-RateLimit-Reset (when limit resets)
└── Return 429 when exceeded
```

---

## 9. Documentation Principles

### OpenAPI/Swagger

```
Include:
├── All endpoints with examples
├── Request/response schemas
├── Authentication requirements
├── Error response formats
└── Rate limiting info
```

### Good Documentation Has

```
Essentials:
├── Quick start / Getting started
├── Authentication guide
├── Complete API reference
├── Error handling guide
├── Code examples (multiple languages)
└── Changelog
```

---

## 10. Decision Checklist

Before designing an API:

- [ ] **Asked user about API consumers?**
- [ ] **Chosen API style for THIS context?** (REST/GraphQL/tRPC)
- [ ] **Defined consistent response format?**
- [ ] **Planned versioning strategy?**
- [ ] **Considered authentication needs?**
- [ ] **Planned rate limiting?**
- [ ] **Documentation approach defined?**

---

## 11. Anti-Patterns to Avoid

### ❌ DON'T:
- Default to REST for everything (consider tRPC/GraphQL)
- Use verbs in REST endpoints (/getUsers)
- Return inconsistent response formats
- Expose internal errors to clients
- Skip rate limiting
- Ignore pagination for lists
- Version without strategy

### ✅ DO:
- Choose API style based on context
- Ask about client requirements
- Document thoroughly
- Use appropriate status codes
- Plan for evolution

---

> **Remember**: API design is about decision-making for YOUR specific context. Don't copy patterns blindly—think about what serves your consumers best.
