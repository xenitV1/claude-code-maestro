#!/usr/bin/env node
/**
 * RALPH WIGGUM: Surgical Harness (The Autonomous Orchestrator)
 * ============================================================
 * Lean orchestrator strictly focused on:
 * - Autonomous Debugging (Test Loop Control)
 * - Forensic Investigation (Root Cause Tracing)
 * 
 * Rules:
 * 1. Fresh Context: Captures error and prepares the next turn.
 * 2. Persistence Wins: Loops until zero errors or stagnation.
 * 3. Disk is State: Uses checksums to detect "Loop Traps."
 * 4. Forensic Search: Identify root cause before patching.
 * 5. Reflection Loop: Self-critique and refine code integrity.
 * 6. Circuit Breaker: Intelligent pivot strategies when stuck.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

/**
 * CircuitBreaker - Enhanced Circuit Breaker with intelligent pivot strategies.
 */
class CircuitBreaker {
  static MAX_SAME_ERROR = 3;
  static MAX_ITERATIONS = 50;
  static TOKEN_BUDGET = 100000;

  constructor(stateFile = null) {
    this.stateFile = stateFile || path.join(process.cwd(), '.maestro', 'circuit_breaker.json');
    this.errorHistory = [];
    this.iterationCount = 0;
    this.pivotCount = 0;
    this.lastStableCommit = null;
    this._loadState();
  }

  _loadState() {
    if (fs.existsSync(this.stateFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
        this.errorHistory = data.error_history || [];
        this.iterationCount = data.iteration_count || 0;
        this.pivotCount = data.pivot_count || 0;
        this.lastStableCommit = data.last_stable_commit;
      } catch (err) {
        // Ignore
      }
    }
  }

  _saveState() {
    const dir = path.dirname(this.stateFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(this.stateFile, JSON.stringify({
      error_history: this.errorHistory.slice(-20),
      iteration_count: this.iterationCount,
      pivot_count: this.pivotCount,
      last_stable_commit: this.lastStableCommit,
      updated_at: new Date().toISOString()
    }, null, 2));
  }

  recordError(errorOutput, exitCode) {
    this.iterationCount++;

    const fingerprint = crypto.createHash('md5').update(errorOutput).digest('hex').substring(0, 12);
    const category = this._categorizeError(errorOutput);

    const entry = {
      iteration: this.iterationCount,
      fingerprint,
      category,
      exit_code: exitCode,
      timestamp: new Date().toISOString(),
      output_preview: errorOutput.substring(0, 200)
    };

    this.errorHistory.push(entry);
    this._saveState();

    return entry;
  }

  _categorizeError(output) {
    const outputLower = output.toLowerCase();

    if (outputLower.includes('syntaxerror') || outputLower.includes('indentationerror')) {
      return 'syntax';
    } else if (outputLower.includes('importerror') || outputLower.includes('modulenotfounderror')) {
      return 'import';
    } else if (outputLower.includes('typeerror')) {
      return 'type';
    } else if (outputLower.includes('attributeerror')) {
      return 'attribute';
    } else if (outputLower.includes('keyerror') || outputLower.includes('indexerror')) {
      return 'access';
    } else if (outputLower.includes('assertionerror') || outputLower.includes('fail')) {
      return 'test_failure';
    } else if (outputLower.includes('timeout')) {
      return 'timeout';
    } else if (outputLower.includes('connection') || outputLower.includes('network')) {
      return 'network';
    }
    return 'unknown';
  }

  shouldPivot() {
    if (this.errorHistory.length === 0) {
      return [false, null, null];
    }

    // Check max iterations
    if (this.iterationCount >= CircuitBreaker.MAX_ITERATIONS) {
      return [true, 'Maximum iterations reached', 'ask_clarification'];
    }

    // Check consecutive same errors
    if (this.errorHistory.length >= CircuitBreaker.MAX_SAME_ERROR) {
      const lastN = this.errorHistory.slice(-CircuitBreaker.MAX_SAME_ERROR);
      const fingerprints = lastN.map(e => e.fingerprint);
      if (new Set(fingerprints).size === 1) {
        return [true, `Same error repeated ${CircuitBreaker.MAX_SAME_ERROR} times`, 'different_algorithm'];
      }
    }

    // Check error category pattern
    if (this.errorHistory.length >= 3) {
      const categories = this.errorHistory.slice(-3).map(e => e.category);
      if (categories.every(c => c === 'syntax')) {
        return [true, 'Persistent syntax errors', 'break_into_pieces'];
      }
      if (categories.every(c => c === 'import')) {
        return [true, 'Persistent import errors', 'check_dependencies'];
      }
    }

    return [false, null, null];
  }

  getPivotGuidance(strategy) {
    const guidance = {
      different_algorithm: `
🔄 PIVOT STRATEGY: Different Algorithm

The same error keeps occurring. The current approach is fundamentally flawed.

ACTION REQUIRED:
1. STOP what you're doing
2. Delete or comment out the problematic code
3. Research alternative algorithms for this problem
4. Start with a completely different approach
5. Run tests after each small change

DO NOT: Try to patch the existing code again.
`,
      break_into_pieces: `
🔄 PIVOT STRATEGY: Divide and Conquer

The problem is too complex to solve at once.

ACTION REQUIRED:
1. Identify the smallest testable unit
2. Create a separate function for just that unit
3. Write a test for just that function
4. Make the test pass
5. Only then add the next piece

DO NOT: Try to implement everything at once.
`,
      ask_clarification: `
🔄 PIVOT STRATEGY: Seek Clarification

After many attempts, the requirements may be unclear or impossible.

ACTION REQUIRED:
1. STOP implementation attempts
2. List the specific blockers encountered
3. Formulate clear questions about requirements
4. Ask the user for clarification
5. Do NOT proceed until requirements are clear

DO NOT: Keep trying the same approach.
`,
      check_dependencies: `
🔄 PIVOT STRATEGY: Check Dependencies

Import errors suggest missing or misconfigured dependencies.

ACTION REQUIRED:
1. Check if all required packages are installed
2. Verify package versions match requirements
3. Check virtual environment activation
4. Run: npm install / pip install -r requirements.txt
5. Check for circular imports

DO NOT: Assume imports will magically work.
`,
      rollback: `
🔄 PIVOT STRATEGY: Rollback to Stable State

Recent changes broke something that was working.

ACTION REQUIRED:
1. Find the last known working commit
2. Run: git stash (save current work)
3. Run: git checkout <last-good-commit>
4. Verify tests pass
5. Reapply changes more carefully

DO NOT: Keep building on broken foundation.
`
    };

    return guidance[strategy] || `Unknown strategy: ${strategy}`;
  }

  recordSuccess() {
    try {
      const result = spawnSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf-8' });
      if (result.status === 0) {
        this.lastStableCommit = result.stdout.trim();
      }
    } catch (err) {
      // Ignore
    }

    this.errorHistory = [];
    this.iterationCount = 0;
    this._saveState();
  }

  reset() {
    this.errorHistory = [];
    this.iterationCount = 0;
    this.pivotCount++;
    this._saveState();
  }
}

/**
 * Run audit command and return status + output.
 */
function runAudit(command, cwd = null) {
  try {
    const result = spawnSync(command, {
      shell: true,
      encoding: 'utf-8',
      cwd: cwd || process.cwd()
    });
    return [result.status || 0, (result.stdout || '') + (result.stderr || '')];
  } catch (err) {
    return [1, err.message];
  }
}

/**
 * Format error output for readability.
 */
function formatErrorLog(output, maxLines = 20) {
  const lines = output.trim().split('\n');

  const relevant = [];
  for (let i = 0; i < lines.length; i++) {
    const lineLower = lines[i].toLowerCase();
    if (['error', 'fail', 'assert', 'exception', 'traceback'].some(kw => lineLower.includes(kw))) {
      const start = Math.max(0, i - 2);
      const end = Math.min(lines.length, i + 3);
      relevant.push(...lines.slice(start, end));
    }
  }

  if (relevant.length > 0) {
    // Dedupe and limit
    const outputLines = [...new Set(relevant)].slice(0, maxLines);
    return outputLines.join('\n');
  }
  return lines.slice(0, maxLines).join('\n');
}

/**
 * Main harness loop with enhanced circuit breaker.
 */
function main() {
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log('🔄 RALPH WIGGUM: Surgical Autonomous Orchestrator');
    console.log('\nUsage: node ralph-harness.js <command> [options]');
    console.log('\nOptions:');
    console.log('  --max-loops N    Maximum loop iterations (default: 50)');
    console.log('  --elite          Enable elite mode (stricter)');
    console.log('  --project DIR    Project directory');
    process.exit(1);
  }

  // Parse arguments
  let command = args[0];
  let maxLoops = 50;
  let eliteMode = false;
  let projectDir = process.cwd();

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--max-loops' && args[i + 1]) {
      maxLoops = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--elite') {
      eliteMode = true;
    } else if (args[i] === '--project' && args[i + 1]) {
      projectDir = path.resolve(args[i + 1]);
      i++;
    }
  }

  console.log('='.repeat(60));
  console.log('🔄 RALPH WIGGUM: SURGICAL AUTONOMOUS ORCHESTRATOR');
  console.log('='.repeat(60));
  console.log(`Target Command: ${command}`);
  console.log(`Max Iterations: ${maxLoops}`);
  console.log(`Project: ${projectDir}`);
  console.log(`Elite Mode: ${eliteMode ? 'ACTIVE' : 'Standard'}`);
  console.log('='.repeat(60));

  // Initialize circuit breaker
  const circuitBreaker = new CircuitBreaker(
    path.join(projectDir, '.maestro', 'circuit_breaker.json')
  );

  const previousChecksums = [];

  for (let i = 1; i <= maxLoops; i++) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`📍 ITERATION ${i}/${maxLoops}`);
    console.log('='.repeat(60));

    // Run the command
    const [code, output] = runAudit(command, projectDir);

    // SUCCESS
    if (code === 0) {
      console.log('\n✅ SUCCESS SIGNAL DETECTED!');
      console.log('='.repeat(60));
      console.log('All tests/audits passed. Persistence loop concluded.');
      console.log('='.repeat(60));

      circuitBreaker.recordSuccess();
      process.exit(0);
    }

    // FAILURE - Record and analyze
    const errorEntry = circuitBreaker.recordError(output, code);
    const currentChecksum = crypto.createHash('md5').update(output).digest('hex');

    console.log(`\n❌ AUDIT FAILED (Exit Code: ${code})`);
    console.log(`   Error Category: ${errorEntry.category}`);
    console.log(`   Fingerprint: ${errorEntry.fingerprint}`);

    // Check for stagnation (legacy check)
    if (previousChecksums.includes(currentChecksum)) {
      console.log('\n🚨 STAGNATION DETECTED: Identical error output!');
    }
    previousChecksums.push(currentChecksum);

    // Check circuit breaker
    const [shouldPivot, reason, strategy] = circuitBreaker.shouldPivot();

    if (shouldPivot) {
      console.log('\n' + '='.repeat(60));
      console.log('🚨 CIRCUIT BREAKER TRIGGERED');
      console.log('='.repeat(60));
      console.log(`Reason: ${reason}`);
      console.log(circuitBreaker.getPivotGuidance(strategy));
      console.log('='.repeat(60));
      console.log('\nAutomation cannot solve this problem.');
      console.log('Manual intervention or strategy change required.');

      circuitBreaker.reset();
      process.exit(1);
    }

    // Show error log
    console.log('\n--- ERROR LOG (Filtered) ---');
    console.log(formatErrorLog(output));
    console.log('----------------------------');

    // Show guidance
    console.log('\n[RALPH SURGICAL GUIDANCE]');
    console.log("1. Read the error carefully");
    console.log("2. Check your memory: view_file('.maestro/brain.jsonl')");
    console.log("3. Make a MINIMAL fix targeting the root cause");
    console.log("4. Don't repeat the same fix that didn't work");

    if (errorEntry.category === 'syntax') {
      console.log('\n💡 TIP: Syntax error detected - check for typos, missing colons, incorrect indentation');
    } else if (errorEntry.category === 'import') {
      console.log('\n💡 TIP: Import error - check if package is installed, correct module path');
    } else if (errorEntry.category === 'test_failure') {
      console.log('\n💡 TIP: Test failure - read the assertion, understand expected vs actual');
    }

    // Progress indicator
    const remaining = maxLoops - i;
    if (remaining > 0) {
      console.log(`\n⏳ ${remaining} iteration(s) remaining...`);
    }
  }

  // Max loops exhausted
  console.log('\n' + '='.repeat(60));
  console.log('🚨 MAX ITERATIONS EXHAUSTED');
  console.log('='.repeat(60));
  console.log('Persistence limit reached without success.');
  console.log('\nCircuit breaker recommends:');
  console.log(circuitBreaker.getPivotGuidance('ask_clarification'));

  process.exit(1);
}

// Export for module use
module.exports = {
  CircuitBreaker,
  runAudit,
  formatErrorLog
};

if (require.main === module) {
  main();
}
