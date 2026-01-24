#!/usr/bin/env node
/**
 * Stop Hook for Maestro Plugin (Ralph Wiggum Controller)
 * Controls whether Claude can exit or must continue iterating.
 *
 * @event Stop, SubagentStop
 */

const {
  findProjectRoot,
  logDebug,
  readStdin,
  outputJson
} = require('./lib/utils');

const Ralph = require('./lib/ralph');

const LOG_PREFIX = '[STOP]';

/**
 * Main hook entry point.
 */
async function main() {
  const projectRoot = findProjectRoot();

  logDebug(LOG_PREFIX, '='.repeat(60));
  logDebug(LOG_PREFIX, 'STOP HOOK TRIGGERED');

  try {
    const hookInput = await readStdin();
    const inputData = JSON.stringify(hookInput);

    // Check if this is a SubagentStop event
    const hookEvent = hookInput.hookEventName || '';
    const isSubagentStop = hookEvent === 'SubagentStop' ||
      inputData.toLowerCase().includes('subagent');

    if (isSubagentStop) {
      logDebug(LOG_PREFIX, 'SUBAGENT STOP detected - allowing subagent to complete');
      outputJson({});
      process.exit(0);
      return;
    }

    // Check Ralph Wiggum iteration state
    const decision = Ralph.getBlockDecision();

    if (!decision.block) {
      // Allow exit
      logDebug(LOG_PREFIX, `Exit allowed: ${decision.reason}`);

      // Cleanup if completed
      if (decision.completed) {
        logDebug(LOG_PREFIX, 'Ralph Wiggum completed - cleaning up state');
        Ralph.clearState();
      }

      outputJson({});
      process.exit(0);
      return;
    }

    // Block exit - Ralph wants more iterations
    logDebug(LOG_PREFIX, `Exit BLOCKED: ${decision.reason} (${decision.current}/${decision.max})`);

    // Build continuation message
    const continuationMessage = `
🔄 RALPH WIGGUM 2.0: ELITE PERSISTENCE ACTIVE

## 📊 Iteration Status
**Progress:** ${decision.current} / ${decision.max}

## ⚠️ TASK COMPLETION BLOCKED

Ralph Wiggum requires more iterations to ensure quality standards are met.

### Next Steps:
1. Continue testing and fixing issues
2. Run tests again to verify fixes
3. Check verification matrix coverage
4. Ensure all critical tests pass

The task will remain blocked until:
- All tests pass OR
- Maximum iterations reached OR
- Manual completion signal received

---

**To manually complete:** Create .maestro/ralph.complete file
**To stop early:** Delete .maestro/ralph.active file
`;

    // Block the exit with continuation prompt
    outputJson({
      block: true,
      message: continuationMessage.trim(),
      iteration: decision.current,
      maxIterations: decision.max
    });

    process.exit(0);

  } catch (err) {
    logDebug(LOG_PREFIX, `Error: ${err.message}`);
    outputJson({});
  }
}

main();
