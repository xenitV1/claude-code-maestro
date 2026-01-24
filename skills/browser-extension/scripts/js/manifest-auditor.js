#!/usr/bin/env node
/**
 * MAESTRO MANIFEST AUDITOR (The Extension Sentinel)
 * 
 * Rules:
 * 1. Manifest v3 is mandatory.
 * 2. No 'unsafe-eval' in CSP.
 * 3. No overly broad host permissions.
 * 4. Mandatory action and background definitions.
 */

const fs = require('fs');
const path = require('path');

/**
 * Audit manifest.json for security and compliance.
 */
function auditManifest(filepath) {
  const issues = [];

  try {
    const content = fs.readFileSync(filepath, 'utf-8');
    const data = JSON.parse(content);

    // RULE 1: Manifest Version
    if (data.manifest_version !== 3) {
      issues.push("[V3-MANDATE] Manifest version must be 3. MV2 is deprecated and insecure.");
    }

    // RULE 2: CSP Security
    const csp = data.content_security_policy || {};
    const extensionPagesCsp = csp.extension_pages || '';
    if (extensionPagesCsp.includes('unsafe-eval') || extensionPagesCsp.includes('unsafe-inline')) {
      issues.push("[SECURITY-CSP] 'unsafe-eval' or 'unsafe-inline' detected in CSP. Critical security risk.");
    }

    // RULE 3: Host Permissions
    const hostPermissions = data.host_permissions || [];
    const dangerousHosts = ['<all_urls>', '*://*/*', 'http://*/*', 'https://*/*'];

    for (const host of hostPermissions) {
      if (dangerousHosts.includes(host)) {
        issues.push(`[LEAST-PRIVILEGE] Broad host permission '${host}' detected. Use specific domains.`);
      }
    }

    // RULE 4: Core Components
    if (!data.background || !data.background.service_worker) {
      issues.push("[ARCHITECTURE] Missing 'background.service_worker'. MV3 requires service worker.");
    }

    if (!data.action) {
      issues.push("[UX-ARCH] Missing 'action' definition. MV3 extensions should use 'action' for UI.");
    }

  } catch (err) {
    issues.push(`[ERROR] Could not parse manifest.json: ${err.message}`);
  }

  return issues;
}

/**
 * Main function.
 */
function main() {
  console.log('🛡️ STARTING MANIFEST SECURITY AUDIT...');

  let target = process.argv[2] || 'manifest.json';

  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    target = path.join(target, 'manifest.json');
  }

  if (!fs.existsSync(target)) {
    console.log(`[SKIP] ${target} not found. Skipping manifest audit.`);
    return;
  }

  const issues = auditManifest(target);

  if (issues.length > 0) {
    console.log(`\n🚨 ${issues.length} MANIFEST VIOLATIONS FOUND:`);
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

    console.log('✅ MANIFEST VERIFIED: Security & Compliance standards met.');
    process.exit(0);
  }
}

main();
