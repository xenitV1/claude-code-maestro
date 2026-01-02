---
name: webapp-testing
description: Web application testing with Playwright including E2E tests, visual testing, and CI integration.
---

# Web App Testing & Deep Audit

> **Maestro Quality Standard:** AI should pro-actively discover and test everything, including routes, APIs, and hidden components.

## 🗺️ Deep Audit & Discovery
When asked to "test everything" or performing a full audit:

### 1. Route & Page Discovery
Scan for all available routes:
- **Next.js:** Scan `app/` (folders with `page.tsx`) and `pages/`.
- **Vite/React:** Look for `Route` components in `App.tsx` or `main.tsx`.
- **Express:** Grep for `.get(`, `.post(`, `.use(`.

**Discovery Command:**
```bash
grep -rE "\.get\(|\.post\(|path:|router\.|@app\." .
```

### 2. API Inventory
List all backend endpoints and cross-reference with frontend service calls to ensure 100% coverage.

### 3. Systematic Testing Loop
1. **Map:** Create a mental or temporary list of all discovered pages/APIs.
2. **Scan:** Use Playwright or HTTP requests to check if they respond (200 OK).
3. **Assert:** Add tests for any uncovered business logic or critical paths.

## Playwright Setup

```bash
npm init playwright@latest
```

## Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }
}

// Usage in test
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'pass');
  await expect(page).toHaveURL('/dashboard');
});

## Playwright Component Testing (2025)
Test UI components in isolation with real browser access:
```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('click event works', async ({ mount }) => {
  let clicked = false;
  const component = await mount(<Button onClick={() => clicked = true}>Click Me</Button>);
  await component.click();
  expect(clicked).toBe(true);
});
```

## Trace Viewer & CI Debugging
Enable tracing to record everything (actions, snapshots, console):
```typescript
// playwright.config.ts
use: {
  trace: 'on-first-retry', // or 'retain-on-failure'
},
```
Access traces: `npx playwright show-trace path/to/trace.zip`
```

## Visual Testing

```typescript
test('homepage screenshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});
```

## Running Tests

```bash
# Run all tests
npx playwright test

# Run specific test
npx playwright test tests/login.spec.ts

# Run with UI
npx playwright test --ui

# Generate report
npx playwright show-report
```

## CI Configuration

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
```
