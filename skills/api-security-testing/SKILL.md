---
name: api-security-testing
description: API security testing principles. OWASP API Top 10, authentication, authorization testing.
---

# API Security Testing

> Principles for testing API security.

---

## 1. OWASP API Security Top 10

### Testing Focus by Category

| Vulnerability | Test Focus |
|---------------|------------|
| **API1: BOLA** | Access other users' resources |
| **API2: Broken Auth** | JWT, session, credentials |
| **API3: Property Auth** | Mass assignment, data exposure |
| **API4: Resource Consumption** | Rate limiting, DoS |
| **API5: Function Auth** | Admin endpoints, role bypass |
| **API6: Business Flow** | Logic abuse, automation |
| **API7: SSRF** | Internal network access |
| **API8: Misconfiguration** | Debug endpoints, CORS |
| **API9: Inventory** | Shadow APIs, old versions |
| **API10: Unsafe Consumption** | Third-party API trust |

---

## 2. Authentication Testing

### JWT Testing Principles

| Check | What to Test |
|-------|--------------|
| Algorithm | None, algorithm confusion |
| Secret | Weak secrets, brute force |
| Claims | Expiration, issuer, audience |
| Signature | Manipulation, key injection |

### Session Testing

| Check | What to Test |
|-------|--------------|
| Generation | Predictability |
| Storage | Client-side security |
| Expiration | Timeout enforcement |
| Invalidation | Logout effectiveness |

---

## 3. Authorization Testing

### Testing Patterns

| Test Type | Approach |
|-----------|----------|
| **Horizontal** | Access peer users' data |
| **Vertical** | Access higher privilege functions |
| **Context** | Access outside allowed scope |

### BOLA/IDOR Testing

1. Identify resource IDs in requests
2. Capture request with user A's session
3. Replay with user B's session
4. Check for unauthorized access

---

## 4. Input Validation Testing

### Injection Types

| Type | Test Focus |
|------|------------|
| SQL | Query manipulation |
| NoSQL | Document queries |
| Command | System commands |
| LDAP | Directory queries |

### Testing Approach

- Test all input parameters
- Try type coercion
- Test boundary values
- Check error messages

---

## 5. Rate Limiting Testing

### What to Test

| Aspect | Check |
|--------|-------|
| Existence | Is there any limit? |
| Bypass | Headers, IP rotation |
| Scope | Per-user, per-IP, global |
| Response | Clear indication |

### Bypass Techniques to Test

- X-Forwarded-For header
- Different HTTP methods
- Case variations in endpoints
- API versioning differences

---

## 6. GraphQL Security

### Specific Tests

| Test | Focus |
|------|-------|
| Introspection | Schema disclosure |
| Batching | Query DoS |
| Nesting | Depth-based DoS |
| Authorization | Field-level access |

---

## 7. API Discovery

### Finding Undocumented APIs

| Source | What to Check |
|--------|---------------|
| Documentation | Swagger, OpenAPI |
| JavaScript | Embedded endpoints |
| Mobile apps | Decompiled code |
| Fuzzing | Common patterns |

---

## 8. Testing Checklist

### Authentication
- [ ] Test for bypass
- [ ] Check credential strength
- [ ] Verify token security
- [ ] Test logout

### Authorization
- [ ] Test BOLA/IDOR
- [ ] Check privilege escalation
- [ ] Verify function access

### Input
- [ ] Test all parameters
- [ ] Check for injection
- [ ] Verify validation

### Security Config
- [ ] Check CORS
- [ ] Verify headers
- [ ] Test error handling

---

## 9. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Test only documented APIs | Discover hidden endpoints |
| Skip authentication testing | Test all auth mechanisms |
| Ignore rate limiting | Test for abuse potential |
| Trust error messages | Verify actual behavior |

---

> **Remember:** APIs are the backbone of modern apps. Test them like attackers will.
