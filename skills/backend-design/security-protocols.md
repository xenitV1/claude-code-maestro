# Backend Security Protocols

> **Reference file for `@backend-design`** - Load when building APIs and services.

---

## 🛡️ Zero Trust Architecture

**Core Principle:** Trust nothing. Verify everything.

| Layer | Verification |
|-------|--------------|
| Input | Schema validation (Zod/Pydantic) |
| Auth | Token verification on EVERY request |
| Data | Row-level security checks |
| Output | DTO mapping (never raw entities) |

---

## 🔐 Input Validation (Gate)

**Mandatory for ALL endpoints:**
```typescript
// ✅ CORRECT - Validate at the gate
const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(72), // bcrypt limit
  name: z.string().min(1).max(100)
}).strict(); // Strip unknown keys

// Use in handler
const validated = CreateUserSchema.parse(req.body);
```

**Rules:**
- Validate BEFORE any logic executes
- Use `.strict()` to reject unknown fields
- Set reasonable length limits

---

## 🗄️ SQL Injection Prevention

| Pattern | Security |
|---------|----------|
| Raw string concatenation | ❌ BANNED |
| Parameterized queries | ✅ Required |
| ORM with bindings | ✅ Acceptable |

**Safe Patterns:**
```typescript
// ❌ DANGEROUS
db.query(`SELECT * FROM users WHERE id = '${userId}'`);

// ✅ SAFE - Parameterized
db.query('SELECT * FROM users WHERE id = $1', [userId]);

// ✅ SAFE - ORM
User.findOne({ where: { id: userId } });
```

---

## 🔑 Authentication Tokens

**PASETO > JWT (2025 Standard):**
```typescript
// PASETO v4 (recommended)
import { V4 } from 'paseto';

const token = await V4.sign(
  { sub: userId, exp: '1h' },
  privateKey
);
```

**If JWT forced (external provider):**
- Use `RS256` or `EdDSA` only
- NEVER `HS256` with weak secret
- NEVER allow `alg: none`

---

## 🚪 CORS Configuration

**Strict Configuration:**
```typescript
// ✅ CORRECT
const corsOptions = {
  origin: ['https://app.example.com', 'https://admin.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
  maxAge: 86400
};

// ❌ DANGEROUS
const corsOptions = {
  origin: '*' // NEVER in production
};
```

---

## 🚦 Rate Limiting

**Required on ALL public endpoints:**
```typescript
// Token bucket with Redis
const rateLimiter = rateLimit({
  store: new RedisStore({ client: redis }),
  windowMs: 60 * 1000, // 1 minute
  max: (req) => req.user ? 100 : 20, // Authenticated vs anon
  standardHeaders: true,
  legacyHeaders: false
});
```

**Limits by endpoint type:**
| Endpoint | Limit |
|----------|-------|
| Login | 5/min |
| API (anon) | 20/min |
| API (auth) | 100/min |
| Webhooks | 1000/min |

---

## 🔒 Secrets Management

**Rules:**
1. NEVER hardcode secrets
2. Validate env vars at startup
3. Use secret managers in production (Vault, AWS Secrets)

```typescript
// Validate at startup
import { z } from 'zod';

const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  API_KEY: z.string()
});

// Crash immediately if invalid
const env = EnvSchema.parse(process.env);
```

---

## 📊 Security Headers

**Required headers:**
```typescript
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '0'); // Modern browsers don't need
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});
```

---

## 🔗 Cross-Skill References

- **@clean-code** - General security defaults, dependency audit
- **@frontend-design** - CSP, CORS coordination
- **@debug-mastery** - Security incident logging
- **@verification-mastery** - Security test verification
