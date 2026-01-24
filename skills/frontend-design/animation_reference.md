<animation_philosophy>
## 🎬 Motion as Meaning (2025 Protocol)

> **Core Philosophy:** Animation is not decoration; it is **information**. It explains state changes, guides attention, and creates a tactile connection between the user and the digital glass. In 2025, motion must be **Physics-Based** (springs) rather than **Time-Based** (easing curves). The interface must feel like it has mass, friction, and fluid dynamics.

### 0. The "No-Jank" Mandate
*   **Performance First:** Animations MUST run at 60fps (or 120fps on ProMotion).
*   **Composite Layers Only:** Animate `transform` and `opacity`. NEVER animate `width`, `height`, `left`, `top` (triggers layout thrashing).
*   **Reduced Motion:** Always respect `prefers-reduced-motion` media query.
</animation_philosophy>

<animation_principles>
## 📐 The 12 Principles of UX Motion (Adapted for 2025)

1.  **Expectation:** Objects should behave as expected based on their physical appearance (e.g., heavy cards move slow).
2.  **Continuity:** The user's eye must be guided. No object should "teleport" or pop into existence without origin. Use View Transitions.
3.  **Narrative:** Motion creates a story. (e.g., An item falling into a cart implies "saved").
4.  **Deformation (Squash & Stretch):** Interactive elements should deform slightly on stress (click/drag) to show elasticity.
5.  **Follow-Through:** Movement shouldn't stop instantly. It should settle (spring damping).
6.  **Staging:** Only animate ONE primary focal point at a time. Don't overwhelm.
7.  **Speed Control:** Enter FAST, Exit FAST, animate changes SLOW.
    *   *Rule:* Interactions initiating (100-200ms). System processing (200-300ms).
8.  **Spatial Awareness:** Elements must respect the Z-axis. Modals come *forward*, backgrounds recede.
9.  **Obscuration:** Using blur/masks to indicate state (e.g., Background blurs when a modal opens).
10. **Parallax:** Depth cueing. Faster objects are closer. Use for Scrollytelling.
11. **Dimensionality:** 2D planes can flip/fold to reveal 3D nature.
12. **Character:** Motion defines brand personality (Bouncy = Playful, Rigid = Corporate).
</animation_principles>

<animation_types_2025>
## 🌪️ 2025 Animation Taxonomy (The Full Spectrum)

### 1. Macro-Animation (Structural)
*   **The "Spatial Morph":** Pages don't just load; they *transform*. A card expands to become the full page (View Transitions API).
*   **Scrollytelling 2.0:** The scrollbar is the timeline. Content reveals, pins, and evolves as the user descends.
*   **Parallax 2.0:** Multi-plane depth where foreground, content, and background move at different rates to simulate 3D space.

### 2. Micro-Type (Kinetic Typography)
*   **Variable Font Breathing:** Fonts that subtly change weight/width on hover or in response to scroll speed.
*   **Glitch & Decode:** Characters scramble before settling (Cyberpunk/Tech aesthetic).
*   **Liquid Text:** Text that acts like a fluid, rippling or distorting on interaction.

### 3. Organic & Liquid Motion
*   **Fluid Gradients:** Mesh gradients that deform and flow like liquid (WebGL/Shaders).
*   **Morphing SVG Shapes:** Blobs or containers that change shape organically to fit content.
*   **Ripple Effects:** Interactions causing a disturbance in the "surface" of the UI (e.g., button clicks sending ripples through adjacent elements).

### 4. 3D & Immersive
*   **Real-Time Spline Scenes:** Embedded 3D objects that react to mouse position or scroll.
*   **Glass Distortion:** Background blurring that shifts as elements move behind frosted glass (refraction simulation).
*   **Depth Stacking:** Using Z-index translation to create deep, diorama-like layered effects.

### 5. AI-Adaptive Motion
*   **Context-Aware Micro-interactions:** Hover effects that "know" what you might do next (magnetic pull that gets stronger based on cursor velocity).
*   **Smart Loading States:** Skeletons that pulse at the *actual* network speed (or simulated) rather than a generic loop.
</animation_types_2025>

<technical_standards>
## 🔧 Technical Stack & Implementation

### 1. The Toolbelt (2025 Standard)
*   **Framer Motion (React Standard):** The default for component-level motion (Exit animations, layout shifts).
*   **CSS View Transitions API:** For page-to-page morphing and shared element transitions. Use this over JS libraries for full-page routing.
*   **Scroll-Driven Animations (CSS):** Use native `animation-timeline: scroll()` instead of scroll-jacking JS listeners where possible.
*   **Rive:** For interactive vector animations (replacing Lottie for state-machines).
*   **Three.js / React-Three-Fiber:** Reserved for "Hero" moments and complex 3D backgrounds.

### 2. Physics vs. Easing
*   **Banned:** `ease-in-out` (too robotic).
*   **Required:** Spring Physics (Mass, Stiffness, Damping).
    *   *Snappy:* `stiffness: 400, damping: 30` (Micro-interactions, buttons).
    *   *Fluid:* `stiffness: 100, damping: 20` (Modals, drawers).
    *   *Heavy:* `stiffness: 50, damping: 10` (Background parallax).

### 3. Micro-Interaction Library
*   **The "Press" Effect:** Scale down to `0.97` on `active`.
*   **The "Magnetic" Pull:** Buttons attract the cursor slightly within a 20px radius.
*   **The "Squish":** Subtle deformation on impact (using SVG filters or vertex shaders).
</technical_standards>

<code_reference>
## 💻 Implementation Snippets

### Framer Motion (The "Pop" Spring)
```jsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click Me
</motion.button>
```

### CSS Scroll-Driven Animation (Native)
```css
@keyframes revealed {
  from { opacity: 0; transform: translateY(100px); }
  to { opacity: 1; transform: translateY(0); }
}

.scrolling-element {
  animation: revealed linear both;
  animation-timeline: view();
  animation-range: entry 25% cover 50%;
}
```

### Kinetic Typography (Tailwind v4)
```css
/* Variable font weight animation */
.kinetic-text {
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.kinetic-text:hover {
  font-variation-settings: 'wght' 800;
}
```
</code_reference>
