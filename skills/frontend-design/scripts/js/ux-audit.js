#!/usr/bin/env node
/**
 * MAESTRO ELITE FRONTEND AUDITOR (2025 Edition)
 * 
 * Enforces the standards defined in:
 * - frontend_reference.md (Aesthetic & Technical Standards)
 * - animation_reference.md (Motion Physics & Continuity)
 * - css_art_reference.md (Code-Based Artistry & Procedural SVG)
 * - security-protocols.md (Frontend Security)
 */

const fs = require('fs');
const path = require('path');

// 2025 Standard Configuration
const CONFIG = {
  bannedTokens: {
    colors: [
      '#6b46c1', 'purple-600', 'fuchsia', 'indigo-500',
      'slate-500', 'gray-200', 'zinc-900',
      'blue-500', 'green-500', 'red-500' // Generic primaries
    ],
    layouts: ['bento', 'masonry', 'split-screen'],
    words: ['lorem', 'ipsum', 'coming soon', 'John Doe'],
    radius: ['rounded-md', 'rounded-lg', 'rounded-sm'], // Enforce purpose-driven radii
    libraries: ['bootstrap', 'bulma', 'foundation', 'material-ui', 'mui']
  },
  motion: {
    banned: ['ease-in-out', 'linear', 'transition-all', 'duration-200', 'duration-300'],
    required: ['type: "spring"', 'stiffness', 'damping', 'layout'],
    jank: ['width', 'height', 'top', 'left', 'right', 'bottom', 'margin', 'padding']
  },
  art: {
    primitives: ['<rect', '<circle', '<ellipse', '<line', '<polygon'],
    requiredColors: ['lch(', 'lab(', 'oklch(']
  },
  security: {
    banned: [
      'dangerouslySetInnerHTML', 'eval(', 'new Function',
      'localStorage.', 'onclick=', 'javascript:'
    ]
  }
};

/**
 * Scan a single file for design & security violations.
 */
function scanFile(filepath) {
  const issues = [];
  let content = '';

  try {
    content = fs.readFileSync(filepath, 'utf-8');
  } catch (err) {
    return [`[ERROR] Could not read file: ${err.message}`];
  }

  const ext = path.extname(filepath);

  // Skip non-code files
  if (!['.tsx', '.jsx', '.ts', '.js', '.vue', '.svelte', '.css'].includes(ext)) {
    return [];
  }

  const isCss = ext === '.css';
  const isArtComponent = filepath.toLowerCase().includes('visual') ||
    filepath.toLowerCase().includes('art') ||
    filepath.toLowerCase().includes('icon') ||
    content.includes('@css-art');

  // --- 1. MOTION PHYSICS & PERFORMANCE (2025 Standard) ---

  if (content.includes('framer-motion') || content.includes('animate-') || content.includes('transition')) {
    // A. Physics Check
    if (content.includes('ease-in-out') || (content.includes('duration-') && !content.includes('spring'))) {
      issues.push(`[MOTION-ROBOTIC] Time-based animation/easing detected. Standard requires Physics (Springs: Stiffness/Damping).`);
    }

    // B. Jank Check (Layout Thrashing)
    const animatingProps = content.match(/animate=\{\{([^}]+)\}\}/);
    if (animatingProps) {
      CONFIG.motion.jank.forEach(prop => {
        if (animatingProps[1].includes(prop)) {
          issues.push(`[PERF-JANK] Critical: Animating '${prop}' causes layout thrashing. Use 'transform' (scale/translate) or 'layout' prop.`);
        }
      });
    }
    if (content.match(/transition-[a-z]+/)) {
      if (content.includes('transition-all')) {
        issues.push(`[PERF-JANK] 'transition-all' is lazy and non-performant. Specify properties (opacity, transform).`);
      }
    }

    // C. Continuity
    if (content.includes('layout') === false && (content.includes('List') || content.includes('Grid') || content.includes('.map'))) {
      issues.push(`[MOTION-CONTINUITY] List/Grid detected without 'layout' prop (Framer Motion). Items must shuffle positions smoothly, not jump.`);
    }
  }

  // --- 2. CSS ART INTEGRITY (For Art/Visual Components) ---

  if (isArtComponent) {
    // A. Anti-Primitive Check
    CONFIG.art.primitives.forEach(prim => {
      if (content.includes(prim)) {
        issues.push(`[ART-PRIMITIVE] Found '${prim}' in Art Component. Use procedural '<path>' commands for organic shape complexity.`);
      }
    });

    // B. Color Space Mandate
    if (content.includes('rgb(') || content.includes('#')) {
      if (!content.includes('lch(') && !content.includes('lab(') && !content.includes('oklch(')) {
        issues.push(`[ART-COLOR] Legacy RGB/Hex detected in Art Component. Use LCH/LAB for photorealistic gradients.`);
      }
    }

    // C. Gradient Mandate (No Flat Colors)
    if (content.includes('background:') || content.includes('fill:')) {
      if (!content.includes('gradient')) {
        issues.push(`[ART-FLAT] Flat color filling detected. Construct material textures using Multi-Stop Gradients.`);
      }
    }
  }

  // --- 3. MICRO-INTERACTION & HAPTICS ---

  if (content.toLowerCase().includes('button') || content.includes('clickable')) {
    if (!content.includes('scale') && !content.includes('whileTap') && !content.includes('active:scale')) {
      issues.push(`[HAPTIC-VISUAL] Interactive element found without 'Press' effect (scale: 0.97 on active/tap).`);
    }
  }

  // --- 4. AESTHETIC INTEGRITY & TOKENS ---

  CONFIG.bannedTokens.colors.forEach(color => {
    if (content.includes(color)) {
      issues.push(`[AESTHETIC-CRIME] Banned generic color token '${color}'. Use Semantic Tokens (primary/accent) or Tinted Greys.`);
    }
  });

  if (content.includes('backdrop-blur') || content.includes('backdrop-filter')) {
    if (!content.includes('border') && !content.includes('shadow') && !content.includes('inset')) {
      issues.push(`[VISUAL-FLAT] "Dirty Glass" detected. Glassmorphism REQUIREs rim lighting (border) or inner-depth (shadow/inset) to look physical.`);
    }
  }

  if (content.includes('via.placeholder') || content.includes('lorem ipsum')) {
    issues.push(`[ANTI-LAZY] Placeholder content detected. Generate Narrative-Consistent fake data.`);
  }

  // --- 5. SECURITY & HYGIENE ---

  CONFIG.security.banned.forEach(token => {
    if (content.includes(token)) {
      issues.push(`[SECURITY-CRITICAL] Banned unsafe/legacy pattern detected: '${token}'.`);
    }
  });

  // --- 6. MODERN CSS / SCROLL ---
  if (isCss || content.includes('style=')) {
    if (content.includes('scroll-behavior') && !content.includes('scroll(') && !content.includes('view(')) {
      // Warning about native scroll animations
    }
  }

  return issues;
}

/**
 * Recursive File Finder
 */
function findFiles(dir, extensions) {
  let results = [];
  try {
    const list = fs.readdirSync(dir);
    list.forEach(file => {
      const fullPath = path.join(dir, file);
      if (['node_modules', '.git', '.maestro', 'dist', 'build', '.next'].includes(file)) return;

      const stat = fs.statSync(fullPath);
      if (stat && stat.isDirectory()) {
        results = results.concat(findFiles(fullPath, extensions));
      } else {
        if (extensions.includes(path.extname(file))) {
          results.push(fullPath);
        }
      }
    });
  } catch (err) { }
  return results;
}

/**
 * Main Execution
 */
function main() {
  console.log('\n🔍 MAESTRO ELITE FRONTEND AUDITOR (2025 Protocol)\n' + '='.repeat(50));

  const targetDir = process.argv[2] || '.';
  const extensions = ['.tsx', '.jsx', '.vue', '.svelte', '.html', '.css', '.svg', '.js', '.ts'];

  const files = findFiles(targetDir, extensions);
  let totalIssues = 0;

  if (files.length === 0) {
    console.log(`ℹ️  No frontend files found to audit in: ${targetDir}`);
    return;
  }

  console.log(`\nScanning ${files.length} files for Architectural, Motion & Art violations...\n`);

  files.forEach(file => {
    const issues = scanFile(file);
    if (issues.length > 0) {
      console.log(`📂 ${path.relative(process.cwd(), file)}`);
      issues.forEach(issue => {
        console.log(`   ❌ ${issue}`);
        totalIssues++;
      });
      console.log('');
    }
  });

  console.log('='.repeat(50));
  if (totalIssues > 0) {
    console.log(`🚨 FAILURE: ${totalIssues} violations found.`);
    console.log(`   Action: Check 'frontend_reference.md', 'animation_reference.md', or 'css_art_reference.md'`);
    process.exit(1);
  } else {
    console.log(`✅ SUCCESS: System Integrity Verified (Art, Motion, Logic, Security).`);
    process.exit(0);
  }
}

main();
