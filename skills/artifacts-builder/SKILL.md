---
name: artifacts-builder
description: React/Tailwind component construction patterns for building reusable UI components.
---

# Artifacts Builder

> Source: travisvn/awesome-claude-skills

## Overview
Patterns for building high-quality React components with Tailwind CSS.

## Component Template (React 19 + Actions)

```tsx
'use client';

import { useActionState, useOptimistic } from 'react';
import { cn } from '@/lib/utils';

// Modern Action-based Button
export function SubmitButton({ action }: { action: (formData: FormData) => Promise<void> }) {
  const [error, submitAction, isPending] = useActionState(async (prev: any, formData: FormData) => {
    try {
      await action(formData);
      return null;
    } catch (e: any) {
      return e.message;
    }
  }, null);

  return (
    <form action={submitAction}>
      <button
        disabled={isPending}
        className={cn(
          'px-6 py-3 rounded-none border-2 border-black bg-black text-white hover:bg-white hover:text-black transition-all active:scale-95',
          isPending && 'animate-pulse cursor-wait'
        )}
      >
        {isPending ? 'Processing...' : 'Submit'}
      </button>
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </form>
  );
}
```

## Card Component

```tsx
interface CardProps {
  title: string;
  description?: string;
  children?: React.ReactNode;
}

export function Card({ title, description, children }: CardProps) {
  return (
    <div className="rounded-none border-2 border-black bg-white p-6 hover:shadow-[4px_4px_0_0_#000] transition-shadow">
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && (
        <p className="mt-1 text-sm text-gray-500">{description}</p>
      )}
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
}
```

## CN Utility

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Best Practices

1. **Type everything**: Use TypeScript interfaces
2. **Compose with cn**: Merge Tailwind classes properly
3. **Extend native props**: HTMLAttributes for full flexibility
4. **Default variants**: Provide sensible defaults
5. **Accessible**: Include proper ARIA attributes
