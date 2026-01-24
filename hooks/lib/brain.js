/**
 * Brain (Long-Term Memory) Operations
 * Manages brain.jsonl for persistent project context across sessions
 * 
 * @module hooks/lib/brain
 */

const fs = require('fs');
const path = require('path');
const { getMaestroDir, ensureMaestroDir, getTimestamp, logDebug } = require('./utils');

const LOG_PREFIX = '[BRAIN]';

/**
 * Get brain.jsonl file path.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {string} brain.jsonl path
 */
function getBrainPath(projectRoot = null) {
  return path.join(getMaestroDir(projectRoot), 'brain.jsonl');
}

/**
 * Read all entries from brain.jsonl.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {Array<object>} Array of brain entries
 */
function readBrain(projectRoot = null) {
  const brainPath = getBrainPath(projectRoot);
  const entries = [];

  if (!fs.existsSync(brainPath)) {
    return entries;
  }

  try {
    const content = fs.readFileSync(brainPath, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());

    for (const line of lines) {
      try {
        entries.push(JSON.parse(line));
      } catch (err) {
        logDebug(LOG_PREFIX, `Failed to parse line: ${line.substring(0, 50)}...`);
      }
    }
  } catch (err) {
    logDebug(LOG_PREFIX, `Error reading brain: ${err.message}`);
  }

  return entries;
}

/**
 * Write entries to brain.jsonl (overwrites existing).
 * 
 * @param {Array<object>} entries - Entries to write
 * @param {string} [projectRoot] - Project root path
 */
function writeBrain(entries, projectRoot = null) {
  const maestroDir = ensureMaestroDir(projectRoot);
  const brainPath = path.join(maestroDir, 'brain.jsonl');

  try {
    const content = entries.map(e => JSON.stringify(e)).join('\n') + '\n';
    fs.writeFileSync(brainPath, content, 'utf-8');
    logDebug(LOG_PREFIX, `Wrote ${entries.length} entries to brain.jsonl`);
  } catch (err) {
    logDebug(LOG_PREFIX, `Error writing brain: ${err.message}`);
  }
}

/**
 * Append a single entry to brain.jsonl.
 * 
 * @param {object} entry - Entry to append
 * @param {string} [projectRoot] - Project root path
 */
function appendToBrain(entry, projectRoot = null) {
  const maestroDir = ensureMaestroDir(projectRoot);
  const brainPath = path.join(maestroDir, 'brain.jsonl');

  try {
    fs.appendFileSync(brainPath, JSON.stringify(entry) + '\n', 'utf-8');
    logDebug(LOG_PREFIX, `Appended entry type=${entry.type} to brain.jsonl`);
  } catch (err) {
    logDebug(LOG_PREFIX, `Error appending to brain: ${err.message}`);
  }
}

/**
 * Read brain entries by type.
 * 
 * @param {string} type - Entry type to filter
 * @param {string} [projectRoot] - Project root path
 * @returns {Array<object>} Filtered entries
 */
function readBrainByType(type, projectRoot = null) {
  const entries = readBrain(projectRoot);
  return entries.filter(e => e.type === type);
}

/**
 * Read preserved data from brain.jsonl.
 * Preserves tech_stack, architecture, scripts, and compact entries.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {object} Preserved data categorized
 */
function readPreservedBrain(projectRoot = null) {
  const preserved = {
    errors: [],
    decisions: [],
    completed: [],
    goals: [],
    tech: [],
    compacts: [],
    others: [] // Catch-all to prevent data loss
  };

  const entries = readBrain(projectRoot);

  for (const entry of entries) {
    const type = entry.type;

    if (['tech_stack', 'architecture', 'scripts'].includes(type)) {
      preserved.tech.push(entry);
    } else if (type === 'compact') {
      preserved.compacts.push(entry);
    } else if (type === 'error') {
      preserved.errors.push(entry);
    } else if (type === 'decision') {
      preserved.decisions.push(entry);
    } else if (type === 'completed') {
      preserved.completed.push(entry);
    } else if (type === 'goal') {
      preserved.goals.push(entry);
    } else {
      preserved.others.push(entry);
    }
  }

  return preserved;
}

/**
 * Format brain.jsonl for AI context display.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {string|null} Formatted brain summary
 */
function formatBrainForContext(projectRoot = null) {
  const entries = readBrain(projectRoot);

  if (entries.length === 0) {
    return null;
  }

  const categories = {
    goal: [],
    decision: [],
    completed: [],
    error: [],
    tech_stack: null,
    architecture: null,
    scripts: null,
    compact: []
  };

  for (const entry of entries) {
    const type = entry.type;

    if (type === 'tech_stack') {
      categories.tech_stack = entry;
    } else if (type === 'architecture') {
      categories.architecture = entry;
    } else if (type === 'scripts') {
      categories.scripts = entry;
    } else if (type === 'compact') {
      const ts = entry.ts || '';
      const summary = entry.summary || '';
      if (summary) {
        categories.compact.push(`[${ts}] ${summary}`);
      }
    } else if (categories[type] !== undefined) {
      const content = entry.content || entry.decision || entry.error;
      if (content) {
        categories[type].push(content);
      }
    }
  }

  const output = [];

  // Tech Stack Section
  const tech = categories.tech_stack;
  const arch = categories.architecture;
  const scripts = categories.scripts;

  if (tech) {
    output.push('### 🔧 Tech Stack');
    if (tech.project_name) output.push(`**Project:** ${tech.project_name}`);
    if (tech.frameworks && tech.frameworks.length) {
      output.push(`**Frameworks:** ${tech.frameworks.join(', ')}`);
    }
    if (tech.key_deps && tech.key_deps.length) {
      output.push(`**Key Dependencies:** ${tech.key_deps.slice(0, 8).join(', ')}`);
    }
    if (tech.dev_tools && tech.dev_tools.length) {
      output.push(`**Dev Tools:** ${tech.dev_tools.join(', ')}`);
    }
    if (tech.package_manager) {
      output.push(`**Package Manager:** ${tech.package_manager}`);
    }
  }

  if (arch) {
    output.push('\n### 🏗️ Architecture');
    if (arch.patterns && arch.patterns.length) {
      output.push(`**Patterns:** ${arch.patterns.join(', ')}`);
    }
    if (arch.key_directories && arch.key_directories.length) {
      output.push(`**Key Dirs:** ${arch.key_directories.slice(0, 6).join(', ')}`);
    }
    if (arch.entry_points && arch.entry_points.length) {
      output.push(`**Entry Points:** ${arch.entry_points.slice(0, 3).join(', ')}`);
    }
  }

  if (scripts && scripts.available) {
    output.push('\n### 📜 Available Scripts');
    const scriptList = Object.entries(scripts.available).slice(0, 5);
    for (const [name, cmd] of scriptList) {
      const cmdShort = cmd.length > 50 ? cmd.substring(0, 50) + '...' : cmd;
      output.push(`- \`${name}\`: ${cmdShort}`);
    }
  }

  // Compact History
  if (categories.compact.length > 0) {
    output.push('\n### 📦 Recent project history (Compacted)');
    // STRICTLY show only the single LATEST one to avoid verbosity
    const latest = categories.compact[categories.compact.length - 1];
    output.push(`👉 **LATEST:** ${latest}`);
  }

  // Standard Brain Sections
  if (categories.goal.length > 0) {
    output.push('\n### 🎯 Project Goals');
    for (const g of categories.goal.slice(-3)) {
      output.push(`- ${g}`);
    }
  }

  if (categories.decision.length > 0) {
    output.push('\n### 🧠 Key Decisions');
    for (const d of categories.decision.slice(-3)) { // Reduced from 5 to 3
      // Truncate long decisions
      const decisionText = d.length > 200 ? d.substring(0, 200) + '...' : d;
      output.push(`- ${decisionText}`);
    }
  }

  if (categories.completed.length > 0) {
    output.push('\n### ✅ Completed');
    for (const c of categories.completed.slice(-3)) { // Reduced from 5 to 3
      // Truncate long completed items
      const completedText = c.length > 150 ? c.substring(0, 150) + '...' : c;
      output.push(`- ${completedText}`);
    }
  }

  if (categories.error.length > 0) {
    output.push('\n### 🚓 Known Issues/Errors');
    for (const e of categories.error.slice(-2)) { // Reduced from 3 to 2
      // Truncate long errors
      const errorText = e.length > 300 ? e.substring(0, 300) + '...' : e;
      output.push(`- ${errorText}`);
    }
  }

  return output.length > 0 ? output.join('\n') : 'No established long-term memory yet.';
}

/**
 * Write tech stack info to brain.jsonl.
 * 
 * @param {object} techInfo - Tech stack information
 * @param {object} structure - Project structure information
 * @param {string} [projectRoot] - Project root path
 */
function writeTechToBrain(techInfo, structure, projectRoot = null) {
  const preserved = readPreservedBrain(projectRoot);
  const ts = getTimestamp();

  // Create new tech entries
  const techEntry = {
    type: 'tech_stack',
    ts,
    project_name: techInfo.name,
    project_version: techInfo.version,
    description: techInfo.description,
    frameworks: techInfo.frameworks || [],
    framework_versions: techInfo.frameworkVersions || {},
    key_deps: techInfo.keyDeps || [],
    dev_tools: techInfo.devTools || [],
    package_manager: techInfo.packageManager,
    node_version: techInfo.nodeVersion,
    module_type: techInfo.type
  };

  const archEntry = {
    type: 'architecture',
    ts,
    project_type: structure.type,
    patterns: structure.patterns || [],
    key_directories: structure.keyDirectories || [],
    entry_points: structure.entryPoints || []
  };

  const scriptsEntry = {
    type: 'scripts',
    ts,
    available: techInfo.scripts || {}
  };

  // Reconstruct entries: New tech entries first, then everything else
  const newEntries = [
    techEntry,
    archEntry,
    scriptsEntry,
    ...preserved.compacts,
    ...preserved.goals,
    ...preserved.decisions,
    ...preserved.completed,
    ...preserved.errors,
    ...preserved.others
  ];

  writeBrain(newEntries, projectRoot);
  logDebug(LOG_PREFIX, 'Tech stack written to brain.jsonl');
}

/**
 * Deduplicate an array while preserving order.
 * 
 * @param {Array} arr - Array to deduplicate
 * @returns {Array} Deduplicated array
 */
function dedupe(arr) {
  return [...new Set(arr)];
}

/**
 * Extract the last assistant message (likely the compact summary) from a transcript.
 * 
 * @param {string} transcriptPath - Path to JSONL transcript
 * @returns {string|null} Extracted summary or null
 */
function extractLastSummary(transcriptPath) {
  if (!transcriptPath || !fs.existsSync(transcriptPath)) {
    return null;
  }

  try {
    // Safety check for exceptionally large transcripts
    const stats = fs.statSync(transcriptPath);
    if (stats.size > 100 * 1024 * 1024) { // 100MB safety fuse
      logDebug('[BRAIN]', 'Transcript abnormally large (>100MB), skipping extraction');
      return null;
    }

    const content = fs.readFileSync(transcriptPath, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());

    let lastAssistantMessage = null;

    // Read backwards to find last message that looks like a summary
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const entry = JSON.parse(lines[i]);

        // DETECTION 1: Explicit flag (The most reliable way in new Claude Code versions)
        if (entry.isCompactSummary || entry.is_compact_summary) {
          const content = entry.message?.content;
          if (typeof content === 'string') {
            lastAssistantMessage = content;
          } else if (Array.isArray(content)) {
            for (const block of content) {
              if (block.type === 'text') {
                lastAssistantMessage = block.text;
                // Don't break here, take the last text block if multiple exist
              }
            }
          }
          if (lastAssistantMessage) return lastAssistantMessage; // Found explicit summary, return immediately
        }

        // DETECTION 2: Pattern matching (fallback)
        if (entry.type === 'assistant' || entry.type === 'user') { // Sometimes summaries appear as user messages in compact
          const msgContent = entry.message?.content;
          if (!msgContent) continue;

          // Normalize to array of text blocks
          const blocks = typeof msgContent === 'string'
            ? [{ type: 'text', text: msgContent }]
            : (Array.isArray(msgContent) ? msgContent : []);

          for (const block of blocks) {
            if (block.type === 'text') {
              const text = block.text || '';

              // Keywords and length check
              // We tightened the check to avoid false positives
              const isSummary = text.length > 50 && (
                (text.includes('This session is being continued from a previous conversation')) ||
                (text.includes('The following is a compact summary')) ||
                (text.includes('compact') && text.includes('summary') && text.includes('context'))
              ) && !text.includes('<local-command-stdout>');

              if (isSummary) {
                lastAssistantMessage = text;
                return lastAssistantMessage; // Found highly probable summary, return immediately (since we read backwards)
              }
            }
          }
        }
      } catch (err) {
        // Skip invalid JSON lines
      }
    }

    return lastAssistantMessage;
  } catch (err) {
    logDebug('[BRAIN]', `Error extracting summary: ${err.message}`);
    return null;
  }
}

/**
 * Write compact summary to brain.jsonl.
 * 
 * @param {string} summary - The summary text
 * @param {string} [projectRoot] - Project root path
 * @returns {boolean} True if successfully saved
 */
function writeCompactToBrain(summary, projectRoot = null) {
  try {
    if (!summary || summary.length < 100) {
      logDebug('[BRAIN]', 'Summary too short, skipping');
      return false;
    }

    // Read preserved brain data
    const preserved = readPreservedBrain(projectRoot);

    // Create new compact entry
    const compactEntry = {
      type: 'compact',
      summary: summary, // Limits removed as requested
      ts: getTimestamp()
    };

    // Filter and combine compact entries (keep last 10)
    // We deduplicate by content (stripping whitespace) to avoid doubles
    const cleanSummary = summary.trim();
    const existingCompacts = preserved.compacts
      .filter(e => {
        const existingText = (e.summary || e.content || '').trim();
        return existingText !== cleanSummary;
      });

    // Take last 9 and add the new one
    const finalCompacts = [...existingCompacts.slice(-9), compactEntry];

    // PROTECTION: If the most recent compact in preserved is IDENTICAL to the new one,
    // and it was added VERY recently (less than 5s ago), it might be a duplicate capture.
    if (preserved.compacts.length > 0) {
      const last = preserved.compacts[preserved.compacts.length - 1];
      const lastText = (last.summary || last.content || '').trim();
      if (lastText === cleanSummary) {
        logDebug('[BRAIN]', 'Duplicate summary detected, skipping write');
        return true; // Consider it handled
      }
    }

    // Reconstruct brain entries (Ordering: Tech -> Compacts -> Goals -> Decisions -> Others)
    const entries = [];

    // 1. Tech entries
    entries.push(...preserved.tech);

    // 2. Compact entries
    entries.push(...finalCompacts);

    // 3. Goals
    entries.push(...preserved.goals.slice(-10));

    // 4. Decisions
    entries.push(...preserved.decisions.slice(-20));

    // 5. Completed
    entries.push(...preserved.completed.slice(-20));

    // 6. Errors
    entries.push(...preserved.errors.slice(-10));

    // 7. Others (preserve everything else)
    entries.push(...preserved.others);

    writeBrain(entries, projectRoot);
    logDebug('[BRAIN]', `Compact summary saved to brain.jsonl (${summary.length} chars)`);
    return true;

  } catch (err) {
    logDebug('[BRAIN]', `Error writing compact to brain: ${err.message}`);
    return false;
  }
}

module.exports = {
  getBrainPath,
  readBrain,
  writeBrain,
  appendToBrain,
  readBrainByType,
  readPreservedBrain,
  formatBrainForContext,
  writeTechToBrain,
  extractLastSummary,
  writeCompactToBrain,
  dedupe
};
