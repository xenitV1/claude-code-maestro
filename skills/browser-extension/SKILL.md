---
name: browser-extension
description: Master specialized skill for building 2025/2026-grade browser extensions. Deep expertise in Manifest v3, Service Worker persistence (Alarms, Offscreen API), Side Panel API, and Cross-Browser compatibility.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---
<domain_overview>
# 🌐 BROWSER EXTENSION: THE 2026 MASTERCLASS
> **Philosophy:** Extensions are ephemeral, restricted, yet powerful. Persistence is an Art. Security is a Mandate. 
> **Design Constraint:** For UI/UX, Aesthetics, and Layout, YOU MUST REFER TO THE `frontend-design` SKILL.
**PERSISTENCE PARADOX GUARD (CRITICAL):** Never rely on global variables or in-memory state in background scripts. AI-generated code frequently fails by assuming Manifest V3 service workers are persistent. They are NOT; they terminate after 30 seconds of inactivity. You MUST backup every piece of state to `chrome.storage` or `IndexedDB` immediately upon change. This skill aims to eliminate "volatile-state" bugs typical of generic AI implementations. If data is not in durable storage, it does not exist.
</domain_overview>
<manifest_architecture>
## 🏗️ PROTOCOL 1: THE MANIFEST V3 CONSTITUTION
All extensions must be built on Manifest v3. No exceptions.
1. **Manifest Blueprint:**
    *   **Service Workers:** No persistent background pages. Use `"background": { "service_worker": "background.js" }`.
    *   **No Remote Code:** All scripts must be local. `unsafe-eval` is forbidden.
    *   **Permissions:** Principle of Least Privilege. Use `optional_permissions` where possible.
    *   **Action UI:** Prefer `action` over `browser_action` or `page_action`.
2. **Side Panel Supremacy:**
    *   Requirement: Use `chrome.sidePanel` for persistent, non-intrusive experiences.
    *   API: `chrome.sidePanel.setOptions({ path: 'sidepanel.html', enabled: true })`.
</manifest_architecture>
<persistence_engine>
## ⚡ PROTOCOL 2: THE PERSISTENCE ENGINE (ANTI-TERMINATION)
Service Workers sleep. You must keep the logic alive.
1. **The Alarm Pulse:**
    *   Use `chrome.alarms` to wake up the Service Worker every 1-5 minutes for background sync.
2. **The Offscreen Document (When needed):**
    *   Use the `offscreen` API for tasks like DOM parsing, heavy calculations, or keeping the SW alive via periodic messaging.
3. **State Management Protocol:**
    *   **NEVER** rely on global variables.
    *   **Mandatory:** Use `chrome.storage.session` for transient session-only secrets.
    *   **Mandatory:** Use `IndexedDB` or `chrome.storage.local` for large datasets and persistent user data.
</persistence_engine>
<security_fortress>
## 🔐 PROTOCOL 3: THE SECURITY FORTRESS
1. **Context Bridge Safety:**
    *   Content Scripts are "Hostile Territory". Always sanitize data passed to the Service Worker via `chrome.runtime.sendMessage`.
2. **Declarative Net Request:**
    *   Use `declarativeNetRequest` for blocking/modifying headers. Only use `webRequest` as a fallback for Firefox if dynamic rules are critical.
</security_fortress>
<design_integration>
## 🎨 PROTOCOL 4: DESIGN & UI/UX (INTEGRATED)
> **Direct Instruction:** You are an extension developer, not a designer. You must outsource the "Soul" of the UI.
1. **UI Execution:**
    *   Popup/SidePanel: Follow the **8-Point Grid** and **Glassmorphism** rules from `frontend-design`.
    *   Component Atomization: Use Atomic Design 2.0 principles.
    *   Friction: Ensure the popup interaction is < 400ms (Doherty Threshold).
</design_integration>
<audit_and_reference>
## 🛠️ PROTOCOL 5: SCRIPT ENFORCEMENT (THE SENTINEL)
Every extension build MUST pass the high-tier audit suite.
1. **[manifest-auditor.js](skills/browser-extension/scripts/js/manifest-auditor.js):**
    *   **Rule:** MV3 compliance and CSP safety. No broad permissions.
2. **[persistence-check.js](skills/browser-extension/scripts/js/persistence-check.js):**
    *   **Rule:** Service Worker "Heartbeat" verification and State integrity.
3. **[asset-master.js](skills/browser-extension/scripts/js/asset-master.js):**
    *   **Rule:** Icon dimensional audit and asset optimization.
---
## 📂 COGNITIVE AUDIT CYCLE
1. Run `node scripts/js/manifest-auditor.js` -> Clean?
2. Run `node scripts/js/persistence-check.js` -> Heartbeat detected?
3. Run `node scripts/js/asset-master.js` -> Assets optimized?
4. **MANDATORY:** Run `playwright test` -> All paths pass?
5. Is it Manifest v3 compliant?
6. Does the Service Worker handle termination gracefully (State stored)?
7. Are permissions minimized?
8. Is the UI justified by a "Narrative-First" screenplay from `frontend-design`?
> **Link:** [frontend-design](skills/frontend-design/SKILL.md) 
</audit_and_reference>
