# Frontend Security Protocols

> **Reference file for `@frontend-design`** - Load when building user-facing features.

---

## 🛡️ XSS Prevention (Critical)

| Attack Vector | Defense |
|---------------|---------|
| `innerHTML` injection | Use `textContent` or DOMPurify |
| `dangerouslySetInnerHTML` | NEVER without sanitization |
| `eval()`, `new Function()` | BANNED - use static code |
| Template literals in DOM | Escape user input |
| URL parameters in HTML | Validate and encode |

**Safe Pattern:**
```javascript
// ❌ DANGEROUS
element.innerHTML = userInput;

// ✅ SAFE
element.textContent = userInput;
// or
element.innerHTML = DOMPurify.sanitize(userInput);
```

---

## 🔐 Authentication & Session

**Token Storage:**
| Method | Security | Use Case |
|--------|----------|----------|
| `httpOnly` cookie | ✅ Best | Auth tokens |
| `localStorage` | ❌ XSS vulnerable | Non-sensitive only |
| `sessionStorage` | ⚠️ Tab-scoped | Temporary state |
| Memory (JS variable) | ✅ Good | Short-lived tokens |

**Cookie Flags:**
```
Set-Cookie: token=xxx; HttpOnly; Secure; SameSite=Strict; Path=/
```

---

## 🚫 CSRF Protection

**Required for:**
- Form submissions
- State-changing requests (POST, PUT, DELETE)
- Sensitive actions (payment, settings)

**Implementation:**
```javascript
// Include CSRF token in requests
fetch('/api/action', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
  }
});
```

---

## 📋 Content Security Policy (CSP)

**Minimum CSP Header:**
```
Content-Security-Policy: 
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.yoursite.com;
  frame-ancestors 'none';
```

**Rules:**
- NO `unsafe-eval` in script-src
- NO `*` wildcards for script/connect
- Use nonces for inline scripts if needed

---

## 📁 File Upload Security

**Client-side validation (defense in depth):**
```javascript
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateFile(file) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new Error('Invalid file type');
  }
  if (file.size > MAX_SIZE) {
    throw new Error('File too large');
  }
  return true;
}
```

**Note:** Server MUST re-validate. Client validation is UX only.

---

## 🔗 Cross-Skill References

- **@clean-code** - General security defaults
- **@backend-design** - API security, CORS config
- **@verification-mastery** - Test security controls
