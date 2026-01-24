#!/usr/bin/env node
/**
 * Pre-Compact Hook - Compact Summary Capture
 * Captures compact summaries before/after manual /compact command
 * and persists them to brain.jsonl for cross-session memory.
 *
 * @event PreCompact
 * @matcher manual - Triggered by /compact command
 */

const fs = require('fs');
const path = require('path');

const {
  findProjectRoot,
  getMaestroDir,
  ensureMaestroDir,
  getClaudeProjectsDir,
  normalizeProjectPath,
  loadState,
  saveState,
  logDebug,
  readStdin,
  outputJson
} = require('./lib/utils');

const {
  readBrain,
  writeBrain,
  appendToBrain,
  extractLastSummary,
  writeCompactToBrain
} = require('./lib/brain');

const LOG_PREFIX = '[PRE-COMPACT]';

/**
 * Find the current active session transcript.
 */
function getCurrentTranscript() {
  try {
    const claudeProjectsDir = getClaudeProjectsDir();
    if (!fs.existsSync(claudeProjectsDir)) {
      return null;
    }

    const projectRoot = findProjectRoot();
    const cwdNormalized = normalizeProjectPath(projectRoot);
    let projectDir = null;

    // Find matching project directory (case-insensitive for Windows compatibility)
    const entries = fs.readdirSync(claudeProjectsDir);
    for (const entry of entries) {
      if (entry.toLowerCase() === cwdNormalized.toLowerCase()) {
        projectDir = path.join(claudeProjectsDir, entry);
        break;
      }
    }

    // Prefix match fallback (case-insensitive)
    if (!projectDir) {
      for (const entry of entries) {
        const entryLower = entry.toLowerCase();
        const cwdLower = cwdNormalized.toLowerCase();
        if (cwdLower && (entryLower.startsWith(cwdLower) || cwdLower.startsWith(entryLower))) {
          projectDir = path.join(claudeProjectsDir, entry);
          break;
        }
      }
    }

    if (!projectDir) {
      return null;
    }

    // Find most recent JSONL file
    const jsonlFiles = fs.readdirSync(projectDir)
      .filter(f => f.endsWith('.jsonl'))
      .map(f => ({
        name: f,
        path: path.join(projectDir, f),
        mtime: fs.statSync(path.join(projectDir, f)).mtimeMs
      }))
      .sort((a, b) => b.mtime - a.mtime);

    if (jsonlFiles.length > 0) {
      return jsonlFiles[0].path;
    }

    return null;
  } catch (err) {
    logDebug(LOG_PREFIX, `Error finding transcript: ${err.message}`);
    return null;
  }
}


/**
 * Main hook entry point.
 */
async function main() {
  const projectRoot = findProjectRoot();

  logDebug(LOG_PREFIX, '='.repeat(60));
  logDebug(LOG_PREFIX, 'PRE-COMPACT HOOK TRIGGERED');
  logDebug(LOG_PREFIX, `Project Root: ${projectRoot}`);

  try {
    // Read hook input
    const hookInput = await readStdin();
    logDebug(LOG_PREFIX, `Hook input: trigger=${hookInput.trigger}, custom_instructions=${hookInput.custom_instructions ? 'yes' : 'no'}`);

    // Only process manual compacts
    if (hookInput.trigger !== 'manual') {
      outputJson({});
      return;
    }

    // Get current transcript
    const transcriptPath = hookInput.transcript_path || getCurrentTranscript();
    logDebug(LOG_PREFIX, `Current transcript: ${transcriptPath ? path.basename(transcriptPath) : 'none'}`);

    if (!transcriptPath) {
      outputJson({});
      return;
    }

    // Extract last summary from transcript
    const summary = extractLastSummary(transcriptPath);
    logDebug(LOG_PREFIX, `Summary found: ${summary ? 'yes (' + summary.length + ' chars)' : 'no'}`);

    if (summary) {
      // Write to brain.jsonl
      writeCompactToBrain(summary, projectRoot);

      // Also save to state for reference if needed
      saveState('last-compact', {
        summary: summary.substring(0, 5000),
        timestamp: Date.now(),
        trigger: 'manual'
      }, projectRoot);

      // Output context for the new session
      outputJson({
        type: 'compact_capture',
        hookSpecificOutput: {
          hookEventName: 'PreCompact',
          additionalContext: `
✅ Current summary captured and saved to brain.jsonl.
Note: Compaction will now continue and a new summary will be generated.
`
        }
      });

      logDebug(LOG_PREFIX, 'Pre-compact hook completed successfully');
    } else {
      // It's normal to not find a summary in PreCompact because it hasn't been generated yet for this compaction.
      // But we output OK anyway.
      outputJson({});
      logDebug(LOG_PREFIX, 'No pre-existing compact summary found in current transcript.');
    }

  } catch (err) {
    logDebug(LOG_PREFIX, `Hook error: ${err.message}`);
    logDebug(LOG_PREFIX, `Stack: ${err.stack}`);
    outputJson({});
  }
}

main();
