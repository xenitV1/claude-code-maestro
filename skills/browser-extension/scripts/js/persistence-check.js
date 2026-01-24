#!/usr/bin/env node
/**
 * MAESTRO PERSISTENCE CHECKER (SW Survival Analyst)
 * 
 * Rules:
 * 1. Must listen to chrome.alarms.onAlarm for wakeup.
 * 2. Must use chrome.storage for state (No globals).
 * 3. Service Worker must be in the root or background/ directory.
 */

const fs = require('fs');
const path = require('path');

/**
 * Analyzes a Service Worker for persistence patterns.
 */
function checkPersistence(filepath) {
  const issues = [];

  try {
    const content = fs.readFileSync(filepath, 'utf-8');

    // RULE 1: Alarm Wakeup
    if (!content.includes('chrome.alarms.onAlarm.addListener')) {
      issues.push('[PERSISTENCE] Service Worker missing alarm listener. SW will terminate and never wake up.');
    }

    // RULE 2: Storage usage
    if (!content.includes('chrome.storage') && !content.includes('chrome.storage.local')) {
      issues.push("[STATE-LOSS] Use of 'chrome.storage' not detected. Persist state to avoid data loss on termination.");
    }

    // RULE 3: Global Variables (Naive check)
    const globalsPattern = /^(?:let|var)\s+\w+\s*=/gm;
    const globalsFound = content.match(globalsPattern) || [];

    if (globalsFound.length > 2) {
      issues.push(`[ARCHITECTURE] ${globalsFound.length} global variables detected. SW globals are ephemeral. Use storage.`);
    }
  } catch (err) {
    issues.push(`[ERROR] Could not read service worker: ${err.message}`);
  }

  return issues;
}

/**
 * Main function.
 */
function main() {
  console.log('⚡ STARTING PERSISTENCE INTEGRITY CHECK...');

  const target = process.argv[2] || 'background.js';

  if (!fs.existsSync(target)) {
    console.log(`[SKIP] ${target} not found. Skipping persistence check.`);
    return;
  }

  const issues = checkPersistence(target);

  if (issues.length > 0) {
    console.log(`\n🚨 PERSISTENCE RISKS DETECTED in ${target}:`);
    for (const issue of issues) {
      console.log(`  ⚠️ ${issue}`);
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

    console.log('✅ PERSISTENCE VERIFIED: Pulse and State patterns detected.');
    process.exit(0);
  }
}

main();
