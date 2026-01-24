<art_philosophy>
## 🎨 Code-Based Artistry (CSS & SVG Architect)

> **Philosophy:** When an Asset Generator (Image Model) is unavailable, the Architect must forge visuals using **Code**. This is not "placeholder art"; this is **Vector Engineering**. We build objects like we build buildings: foundation first, then structure, then surface, then light.

### 0. The "No-Primitive" Mandate
*   **Composite Complexity:** Never use a single primitive (e.g., `<rect>`) to represent a complex object. A "Sword" is not one line; it is a Handle (Leather), a Guard (Metal), a Blade (Steel), and an Edge (Light).
*   **Procedural Integrity:** SVG paths must be constructed mathematically (Cubic Bezier `C` commands) to ensure organic curvature, avoiding the "blocky" look of basic shapes.
</art_philosophy>

<geometric_protocols>
## 📐 Geometric Composition Protocol

### 1. The Assembly Line Strategy
Break every object into Z-Index Layers:
1.  **Silhouette (Shadow):** The base shape, usually `filter: blur()` or dark opacity.
2.  **Base Material (Body):** The main color/gradient.
3.  **Texture (Detail):** Noise, patterns, or grain using `mask-image` or `background-image`.
4.  **Lighting (Volume):**
    *   *Highlight:* White/Yellow gradient at top-left.
    *   *Core Shadow:* Dark gradient at bottom-right.
    *   *Rim Light:* 1px inset border or path glow.
    *   *Reflection:* Sharp diagonal white gradient (`linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.8) 50%, transparent 60%)`).

### 2. Procedural SVG Mastery
*   **Path Construction:** Use `d="M... C..."` for everything.
    *   *M (Move):* Start point.
    *   *L (Line):* Hard structures (Buildings, Tech).
    *   *C (Cubic Bezier):* Organic curves (Nature, Cloth).
    *   *Q (Quadratic):* Simple arcs.
*   **Coordinate System:** Always define a `viewBox="0 0 100 100"` and work in normalized units (% or relative) for scalability.
</geometric_protocols>

<material_library>
## 🧪 2025 Material Library (CSS/LCH)

### 1. Advanced Color Spaces (LCH/HWB)
**Rule:** Use `lch()` or `lab()` for gradients to avoid "Grey Dead Zones" in the middle of transitions.
*   *Vibrant Metal:* `linear-gradient(135deg, lch(90% 0 0), lch(40% 0 0))` (Chrome).
*   *Deep Magic:* `conic-gradient(lch(50% 132 300), lch(90% 100 100))` (Neon).

### 2. Photorealistic Textures
#### Polished Steel (Katana Blade)
```css
background: linear-gradient(
  90deg,
  #999 0%,
  #fff 20%, /* Sharp Highlght */
  #555 25%, /* Hard Reflection Edge */
  #ccc 100%
);
box-shadow: inset 0 0 5px rgba(0,0,0,0.5); /* Depth */
```

#### Holographic Glass
```css
background: rgba(255, 255, 255, 0.05);
backdrop-filter: blur(10px);
border-top: 1px solid rgba(255, 255, 255, 0.5); /* Rim Light */
border-left: 1px solid rgba(255, 255, 255, 0.5);
box-shadow: 
  0 4px 30px rgba(0, 0, 0, 0.1),
  inset 0 0 20px rgba(255,255,255,0.1);
```

#### Organic Surface (Wood/Leather)
Use SVG Filters within CSS:
```css
filter: url('#grain'); /* Define <filter> with feTurbulence in your SVG defs */
```
</material_library>

<human_emulation>
## 🧠 Human Emulation Protocols (The "Imperfection" Standard)

> **Insight:** Humans do not draw perfect lines. Real materials have wear, tear, and noise. To emulate high-fidelity human design, you must deliberately introduce "Ordered Chaos".

### 1. The Surface Imperfection Rule
Pure colors (`#000`) look digital and fake.
*   **Noise Overlay:** Always add a subtle noise layer to break the digital smoothness.
    ```css
    .texture-overlay {
      background-image: url("data:image/svg+xml,...<feTurbulence.../>");
      opacity: 0.03;
      mix-blend-mode: overlay;
      pointer-events: none;
    }
    ```
*   **Irregular Borders:** Never use perfect `50%` radius for organic objects. Use `border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%` for "blobby" natural shapes.

### 2. Lighting Physics (Fresnel & Caustics)
*   **Fresnel Effect:** Edges are clearer/brighter than the center on curved surfaces. Use `box-shadow: inset` to simulate this.
*   **Bloom:** Light bleeds. Use `filter: drop-shadow(0 0 8px color)` instead of `box-shadow` for glowing elements to get a smoother falloff.

### 3. Blend Mode Alchemy
Do not just stack opacities. Use Photoshop-style blending for richness:
*   `mix-blend-mode: color-dodge` for neon glows.
*   `mix-blend-mode: overlay` for texture mapping on surfaces.
*   `mix-blend-mode: multiply` for shadows (keeps underlying color saturation).
</human_emulation>

<implementation_rules>
## 🛠️ Implementation Rules

1.  **Usage Trigger:** Use this reference when the User asks for a specific visual object ("Draw a robot") and `generate_image` is unavailable or code-based rendering is preferred.
2.  **Component Structure:** Create a dedicated component (e.g., `<KatanaVisual />`). Do not inline huge SVG paths into the main page logic.
3.  **Responsive Art:** Use `vector-effect="non-scaling-stroke"` on SVG paths to maintain line weight during resizing.
</implementation_rules>
