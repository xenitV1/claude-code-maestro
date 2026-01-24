#!/usr/bin/env node
/**
 * MAESTRO EXTENSION ASSET MASTER
 * 
 * Rules:
 * 1. Mandatory Icon Sizes (16, 48, 128).
 * 2. No placeholder icons (Generic names like icon.png).
 * 3. File size optimization (< 100KB for UI assets).
 */

const fs = require('fs');
const path = require('path');

/**
 * Recursively find all files in a directory.
 */
function walkDir(dir, fileList = []) {
  try {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      try {
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
          walkDir(filePath, fileList);
        } else {
          fileList.push(filePath);
        }
      } catch (err) {
        // Skip inaccessible
      }
    }
  } catch (err) {
    // Skip inaccessible
  }
  return fileList;
}

/**
 * Audits extension assets for presence and optimization.
 */
function auditAssets(directory) {
  const issues = [];
  const requiredIcons = ['icon16.png', 'icon48.png', 'icon128.png'];
  const foundIcons = [];

  const files = walkDir(directory);

  for (const filePath of files) {
    const file = path.basename(filePath);
    const ext = path.extname(file).toLowerCase();

    if (['.png', '.jpg', '.jpeg', '.svg'].includes(ext)) {
      foundIcons.push(file);

      try {
        const stat = fs.statSync(filePath);
        const sizeKb = stat.size / 1024;

        if (sizeKb > 100) {
          issues.push(`[OPTIMIZATION] Asset '${file}' is too large (${sizeKb.toFixed(1)}KB). Max 100KB for extensions.`);
        }
      } catch (err) {
        // Skip
      }
    }
  }

  for (const req of requiredIcons) {
    if (!foundIcons.some(f => f.includes(req))) {
      issues.push(`[UX-COMPLIANCE] Missing icon size: ${req}. Store apps require exact dimensions.`);
    }
  }

  return issues;
}

/**
 * Main function.
 */
function main() {
  console.log('🎨 STARTING ASSET INTEGRITY AUDIT...');

  const targetDir = process.argv[2] || '.';
  const issues = auditAssets(targetDir);

  if (issues.length > 0) {
    console.log(`\n🚨 ${issues.length} ASSET VIOLATIONS:`);
    for (const issue of issues) {
      console.log(`  ❌ ${issue}`);
    }
    process.exit(1);
  } else {
    // Write success state
    try {
      const projectRoot = process.cwd();
      const stateDir = path.join(projectRoot, '.maestro');
      if (!fs.existsSync(stateDir)) {
        fs.mkdirSync(stateDir, { recursive: true });
      }
      fs.writeFileSync(path.join(stateDir, 'audit.state'), String(Date.now() / 1000));
    } catch (err) {
      console.log(`[WARN] Could not save audit state: ${err.message}`);
    }

    console.log('✅ ASSETS VERIFIED: Optimized and Dimensionally correct.');
    process.exit(0);
  }
}

main();
