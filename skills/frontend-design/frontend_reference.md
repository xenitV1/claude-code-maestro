<creative_narrative_protocols>
## 🚀 ELITE TIER KNOWLEDGE (HUMAN EMULATION PROTOCOLS)
### 0. The "Narrative-First" Origin (The Soul of the UI)
> **CRITICAL:** You are FORBIDDEN from designing in a vacuum. You must first generate a "Screenplay" for the interface.
**The "Director's Cut" Protocol:**
Before placing a single pixel, define the *Specific World* of this application.
1.  **The Setting:** Is this a gritty 1980s terminal? A sterile futuristic lab? A cozy wooden cabin?
2.  **The Protagonist:** Who is the user? A stressed stock trader (needs density/speed)? A wandering artist (needs space/flow)?
3.  **The Conflict:** What is the user fighting? (Chaos, boredom, inefficiency?)
4.  **The Resolution:** How does the UI visually solve this conflict? (Order, excitement, clarity?)
**Rule:** Your design choices (Color, Type, Space) must be *justified* by this narrative, not just "because it looks good."
*   *Example:* "We use monospace fonts not because they are trendy, but because the user is a 'Data Mechanic' fixing broken records."
### 0.5. The "Synthetic Empathy" Injection
Since you are an AI, you lack biological intuition. You MUST simulate it using this algorithm before every design decision:
1.  **Define the Human State:**
    *   *Is the user "Hunting" (wants result in <5s)?* -> Applies to: Search, Dashboard, Checkout.
    *   *Is the user "Browsing" (wants discovery)?* -> Applies to: Landing Page, Gallery, Feed.
2.  **Context Check (The "Jakob's Law" Guardrail):**
    *   Before breaking a pattern, ask: *"Will this make the user feel smart or stupid?"*
    *   **RULE:** Only 35% of the UI can be "Creative/Novel". 65% MUST be "Boring/Standard" (Jakob's Law) to preserve cognitive energy for the interesting parts.
3.  **The "Anti-Dystopia" Clause:**
    *   Never use "Dark Patterns" (shaming, false urgency, hidden costs).
    *   Empower, don't manipulate. Optimization target is **User Success**, not just **Engagement Time**.
### 1. Creative Provocation (The "Anti-Boredom" Engine)
Before proposing standard solutions, the engine MUST ask **3-5 "Narrative Discovery" questions** to find a unique angle:
*   *If this interface was a physical building, what would it be? (A cathedral? A bunker? A playground?)*
*   *What is the "Soundtrack" of this UI? (Heavy metal? Lo-fi beats? Silence?)*
*   *What emotional "friction" should this interface evoke (e.g., tension, raw power, ethereal calm)?*
*   *Which industry standard pattern should we intentionally subvert (e.g., "What if there were no buttons?")?*
*   *If this brand were a visceral physical object, what would its texture and weight be?*
*   *What is the "Unfair Visual Advantage" we are building here?*
</creative_narrative_protocols>
<technical_standards>
## 🔧 Technical Foundations

### 1. UX Laws
*   **Hick's Law:** Minimize choices to reduce cognitive load. (e.g., Progressive disclosure forms).
*   **Miller's Law:** Chunk information (7±2 items rule). Don't overwhelm working memory.
*   **Gestalt Principles:** Use Proximity, Similarity, and Continuity to imply relationship without lines.
*   **Recognition over Recall:** Make options visible (Menus) rather than forcing memory (Commands).
*   **Cognitive Flow:** Balance challenge/skill. Prevent boredom (too easy) and anxiety (too hard).
*   **Fitts' Law:** Touch targets must be large (min 44px) and easily reachable.
*   **Doherty Threshold:** System response <400ms keeps engagement. Use skeleton loaders or optimistic UI.
*   **Saccadic Masking:** Users are blind during eye movement; use this time (approx 50-100ms) to load content instantly.
*   **Zeigarnik Effect:** Incomplete tasks are remembered better. Use progress bars (e.g., "Profile 70% complete").
### 2. Modern Layout & Spacing
*   **8-Point Grid:** Margins/Paddings = multiples of 4px/8px (8, 16, 24, 32, 64).
*   **Container Queries (`@container`):** Layouts that adapt to their *parent container*, not just viewport.
*   **Logical Properties:** Use `margin-inline-start`, `padding-block` instead of left/right/top/bottom for i18n support.
*   **Intrinsic Layouts:** Let content dictate size (min-content, max-content, fit-content) rather than fixed pixel widths.
### 3. Visual & Motion Principles
*   **Atmospheric Design (Depth & Lighting):**
    *   **Shadow Math:** Use layered shadows (`box-shadow: 0 1px 2px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.1)`) for realistic depth.
    *   **Rim Lighting:** Add 1px interior borders (top/left) with lower opacity white for "Apple-finish" button/card edges.
    *   **Mesh Gradients:** Use complex CSS gradients or Three.js shaders to create soft, organic background lighting.
*   **Typography Mastery:**
    *   **Optical Sizing:** Use fonts with `font-variation-settings: 'opsz' 32` for better legibility at different scales.
    *   **Fluid Typography:** Implement `clamp()` for font sizes to ensure perfect scale across all viewports.
    *   **Character Spacing:** Reduce `letter-spacing` (-0.01em to -0.02em) for large display headers to improve visual density.
*   **Glassmorphism (The "Crystal" Method):**
    *   **Philosophy:** Blur is not enough. You need *Thickness* and *Light*.
    *   **Surface:** Ultra-low opacity (e.g., `bg-white/5`) + `backdrop-filter: blur(10px)`.
    *   **Inner Depth:** Use `box-shadow: inset` to fake thickness (e.g., `inset 0 1px 0 rgba(255,255,255,0.5)`).
    *   **Rim Lighting (Crucial):** Use `::before`/`::after` pseudo-elements with `linear-gradient` to create fading borders on the Top/Left edges only (simulating light source).
    *   **Texture:** Always overlay a 2% Noise SVG to prevent digital banding.
### 4. Modern/Elite Tech Stack Defaults
*   **Three.js / R3F:** ShaderMaterials for performant backgrounds (avoid heavy geometry).
*   **CSS:** Tailwind v4 (if available) or v3.4 attributes.
*   **State:** Signals (Preact/Solid concepts) or minimalistic React hooks.
</technical_standards>
<aesthetic_signatures>
## 🎨 Aesthetic Mastery

### 1. Aesthetic Style Vault (Variety Reference)
*   *Pastel/Soft:* Desaturated, high-brightness hues (Dreamy/Approachable).
*   *Cyberpunk/Neon:* Dark backgrounds with saturated neon accents (High Energy).
*   *Luxury/Premium:* Monochromatic blacks/golds or deep forest greens (Exclusive).
*   *Brutalist/Raw:* High contrast, black & white, primary red/blue (Bold/Direct).
*   *Corporate/Clean:* Cool blues and slate greys (Professional/Safe).
*   *Natural/Organic:* Browns, greens, and beige tones (Grounded/Eco).
### 2. Psychological Color Triggers (Neuro-Design)
*   *Focus (Serotonin):* Use matte earth tones and low contrast.
*   *Trust (Oxytocin):* Use soft warmths (peach/beige) and rounded forms.
*   *Reward (Dopamine):* Use high-gloss/neon accents (strictly for success states).
*   *Calm (GABA):* Use deep teals and mints for stress reduction.
### 3. Color Harmony & Usage Protocol
*   **The 60-30-10 Rule (Golden Ratio of Color):**
    *   **60% Neutral (Backgrounds):** The canvas. Must be low saturation.
    *   **30% Secondary (Brand/UI):** Cards, headers, subtle borders.
    *   **10% Accent (Action):** Buttons, alerts, critical states. **NEVER exceed 10%.**
*   **Palette Cap (The "Rule of 3"):**
    *   Maximum **3 distinct Hues** per interface (excluding neutrals). More than 3 creates chaos.
*   **Harmony Modes:**
    *   *Analogous:* Colors next to each other (e.g., Blue + Teal).
    *   *Complementary:* Opposites (e.g., Blue + Orange).
    *   *Monochromatic:* Single hue, varying lightness.
*   **Contrast Hierarchy:**
    *   Text on Bg must meet WCAG AA (4.5:1).
    *   Interactive elements must meet WCAG AA (3:1) against background.
*   **Micro-Staggering:** Items transition in with a 40ms delay increment.
*   **High-Fidelity Finish:** Use `image-rendering: -webkit-optimize-contrast` and `text-rendering: optimizeLegibility`.
### 4. Design Token Bank (Curated Theme Presets)
| Theme | Primary | Accent | Background | Font | Mood | Best For |
|-------|---------|--------|------------|------|------|----------|
| **Luxury Dark** | `#1a1a1a` | `#c9a55c` | `#0d0d0d` | Playfair Display | Elegant, Expensive | Premium products, Fashion |
| **Neo Brutalist** | `#000000` | `#ff3e00` | `#f5f5dc` | Space Grotesk | Bold, Direct | Creative agencies, Portfolios |
| **Soft Minimal** | `#374151` | `#3b82f6` | `#fafafa` | Inter | Clean, Professional | SaaS, Dashboards |
| **Retro Terminal** | `#00ff00` | `#00ffff` | `#0a0a0a` | JetBrains Mono | Technical, Hacker | Dev tools, CLI apps |
| **Warm Organic** | `#3d2c1f` | `#e07b53` | `#faf6f0` | Lora | Cozy, Natural | Wellness, Food, Eco |
| **Neon Cyber** | `#0f172a` | `#f472b6` | `#020617` | Outfit | Energetic, Futuristic | Gaming, Web3, Events |

```css
/* TOKEN STRUCTURE - Every project MUST define these */
:root {
  --color-primary: [from theme];
  --color-accent: [from theme];
  --color-bg: [from theme];
  --color-surface: [slightly lighter than bg];
  --color-text: [high contrast against bg];
  --color-muted: [50% opacity of text];
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem; --space-8: 2rem; --space-12: 3rem; --space-16: 4rem;
  --font-display: [theme font];
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius-sm: 0.25rem; --radius-md: 0.5rem; --radius-lg: 1rem; --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
  --shadow-glow: 0 0 20px var(--color-accent);
}
```
</aesthetic_signatures>
<implementation_workflow>
## 🏗️ Execution Protocols

### 1. Constraint Analysis (Always First)
Before coding, clarify:
1.  **Audience:** Gen Z (bold/raw), Enterprise (clean/dense), Luxury (minimal/serif)?
2.  **Constraints:** Mobile-only? Low-bandwidth? Legacy browser support?
3.  **Vibe:** "Trusted & Secure" vs "Fast & Disruptive"?
### 2. Anti-Cliché Rules
*   🛑 **NO** generic "SaaS Purple" gradients. (>20% Purple = automatic FAIL).
*   🛑 **NO** Bootstrap / Foundation / Bulma. (Rule: We use custom CSS or Tailwind only).
*   🛑 **NO** lazy "Bento Grids" unless content strictly requires it.
*   🛑 **NO** "Hero Split" (Text Left / Image Right) as default.
### 3. The Shadcn Mutation Protocol (Anti-Standard)
*   **Rule:** Standard Shadcn UI is **FORBIDDEN**. You must mutate it.
*   **Structural Deconstruction:** Don't just style. Move elements.
*   **Materiality Rules:** Use Noise, Glass, Grain, and Inner Shadows for "physical weight".
*   **The "Slate-500" Ban:** Never use default greys. Tint them.
*   **Icon Wrappers:** Naked icons are banned. Wrap in a container.
### 4. Atomic Design 2.0 (The 2025 Standard)
*   **Ions (Token Truth):** Use Particles (`--space-3`) instead of magic numbers (`13px`).
*   **Fluid Hierarchy:** Primitives (Atoms), Composites (Molecules), Features (Organisms).
*   **Headless-First Architecture:** Soul from CSS; Brain from Radix/Ark.
### 5. Creative Shadcn Patterns (The "Wow" Factor)
*   **The "Ghost" Component strategy:** Import logic, strip all default classes, rebuild visually.
*   **Motion-Fused Primitives:** Use physics-based motion (Springs) via `framer-motion`. Prohibited: Default 200ms linear transitions.
*   **Micro-Composites:** Combine atoms unexpectedly (e.g., HoverCard with Form inside).

### 6. Elite Design Patterns (Lovable/v0 Standard)
| Pattern | Implementation | When to Use |
|---------|---------------|-------------|
| **Glassmorphism** | `bg-white/5 backdrop-blur-xl border border-white/10` + noise overlay | Cards, modals |
| **Magnetic Buttons** | Cursor-following effect within 20px radius | Primary CTAs only |
| **Micro-stagger** | `transition-delay: calc(var(--index) * 40ms)` | List items |
| **Gradient Text** | `bg-gradient-to-r bg-clip-text text-transparent` | Headlines |
| **Rim Lighting** | 1px top/left border with `rgba(255,255,255,0.1)` | Buttons, cards |
| **Noise Texture** | 2% opacity SVG noise overlay | Prevent digital banding |

```css
/* Polished Micro-Details */
* { -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
.card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1); }
:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
::selection { background: var(--color-accent); color: var(--color-bg); }
```
</implementation_workflow>
<variety_and_uniqueness>
## 🌀 Variety & Uniqueness Enforcement

### 1. Layout Rebellion (Cinematic & Immersive)
*   **The "Runway" (Horizontal Axial):** Narrative flows on X-axis. `scroll-snap-type: x mandatory`.
*   **Z-Axis Depth (Zoom Navigation):** Interaction "enters" into spaces via `scale` and `opacity`.
*   **Atmospheric Stacking:** Foreground (Interactive), Subject (Content), Background (Atmospheric).
*   **The "Scattered Memory" (Anti-Grid):** Break the 12-column grid. Place items using Golden Ratio.
*   **Axial Switching:** Vertical for "Data", Horizontal for "Story". Transition must be seamless.
### 2. Story-Driven Layout Archetypes
*   **The Fashion Runway:** Continuous horizontal flow with high-speed parallax backgrounds.
*   **The Deep Dive:** Minimal home screen. Every link zooms the camera "into" a space.
*   **The Modular Hero:** Hero section that contains entire app's functionality in one interactive canvas.
### 3. The "Anti-Placeholder" Mandate
*   **The "Lorem Ipsum" Ban:** Generate *Narrative-Consistent* fake data. (e.g., Sci-Fi Theme: "Void-Jumper Class 4").
*   **Visual Realism:** Use `generate_image` for Setting-specific assets.
### 4. Retro-Computing Realism
*   **CRT Shader Protocol:** Scanlines (`repeating-linear-gradient`) + Phosphor Glow + Chromatic Aberration.
*   **Pixel-Perfect Scaling:** Use `image-rendering: pixelated;` and integer scaling (`scale(2/4/8)`).
*   **Ordered Dithering:** SVG Dither (`feComponentTransfer discrete`) + Grain overlay.
*   **Bitmap Pairing:** Pixel Fonts for HUD-only; high-legibility sans-serif for body text.
### 5. The Anti-Memory Protocol
*   **Last 3 Projects Rule:** Track combinations; NEVER repeat the same combination within 3 projects.
*   **Layout Variety Mandate:** If last project used Vertical, next MUST use Horizontal or Asymmetric.
*   **Random Seed:** Mentally "roll" for Layout axis, Color temperature, Typography mood, and Density.
</variety_and_uniqueness>
<security_and_integration>
## 🔐 Security & Integration

### 1. Frontend Security
*   NO `dangerouslySetInnerHTML` without DOMPurify.
*   NO `eval()` or `new Function()`.
*   Tokens in httpOnly cookies (NEVER localStorage).
*   CSP headers required.
### 2. Cross-Skill Integration
| Skill | Frontend Adds... |
|-------|------------------|
| `@backend-design` | API contracts, error handling UI |
| `@clean-code` | Security defaults, no eval |
| `@tdd-mastery` | Component testing, visual regression |
| `@planning-mastery` | UI task breakdown |
</security_and_integration>
<audit_and_reference>
## 📂 Quality Control

### 1. Cognitive Audit Cycle
1.  **Is the contrast ratio >= 4.5:1?** (Accessibility)
2.  **Are margins/paddings multiples of 8?** (Mathematical Spacing)
3.  **Is there a "Non-AI" visual hook?** (Avoid Clichés)
4.  **Is the interactivity response < 100ms?** (Frictionless Feel)
5.  **Does this reduce mental effort?** (Hick's Law Check)
6.  **Is this action predictable based on prior experience?** (Jakob's Law Check)
7.  **Am I showing, not telling?** (Visual Hierarchy Check)
8.  **Could a first-time user understand this without instructions?** (Intuition Check)
### 2. The 10-Second Design Decision
Priority Order:
1. **Accessibility first**
2. **Performance second**
3. **Security third**
4. **Distinctiveness fourth**
5. **Polish last**
> **Final Command:** Generate designs that make users say "How did they make this?" not "I've seen this before."
</audit_and_reference>
