#!/usr/bin/env node
/**
 * RALPH WIGGUM: Surgical QA Engine (Refactored)
 * ============================================
 * Lean orchestrator strictly focused on:
 * - Autonomous Debugging (Harness Control)
 * - Code Reflection (Integrity & Clean Code)
 * 
 * "I'm helping!" — Focus: Root Cause Surgery.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// Import Reflection module
let ReflectionLoop;
try {
  ({ ReflectionLoop } = require('./reflection-loop'));
} catch (err) {
  // Standalone mode handled internally
}

/**
 * RalphSurgicalEngine - Narrowed orchestrator for Debug & Clean Code.
 */
class RalphSurgicalEngine {
  static MAX_ITERATIONS = 50;
  static MAX_CONSECUTIVE_SAME_ERRORS = 3;

  constructor(options = {}) {
    this.projectRoot = options.projectRoot || process.cwd();
    this.stateDir = path.join(this.projectRoot, '.maestro');
    this.stateFile = options.stateFile || path.join(this.stateDir, 'ralph_surgical_state.json');

    this.reflectionLoop = ReflectionLoop ? new ReflectionLoop({
      maxIterations: RalphSurgicalEngine.MAX_ITERATIONS
    }) : null;

    this.state = {
      consecutive_same_errors: 0,
      last_error_fingerprint: '',
      total_iterations: 0,
      current_phase: 'standby'
    };

    this._loadState();
  }

  _loadState() {
    if (fs.existsSync(this.stateFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
        this.state = { ...this.state, ...data };
      } catch (err) {
        // Ignore
      }
    }
  }

  _saveState() {
    if (!fs.existsSync(this.stateDir)) {
      fs.mkdirSync(this.stateDir, { recursive: true });
    }
    fs.writeFileSync(this.stateFile, JSON.stringify({
      ...this.state,
      updated_at: new Date().toISOString()
    }, null, 2));
  }

  // =========================================================================
  // SURGICAL PHASE 1: REFLECTION
  // =========================================================================

  runReflection(code) {
    this.state.current_phase = 'reflection';
    if (!this.reflectionLoop) return [null, 'Reflection module missing.'];

    const result = this.reflectionLoop.reflect(code);
    this.state.total_iterations++;
    this._saveState();
    return [result, this.reflectionLoop.getRefinementGuidance(result)];
  }

  // =========================================================================
  // SURGICAL PHASE 2: DEBUG HARNESS
  // =========================================================================

  runTestCommand(command) {
    this.state.current_phase = 'debugging';
    try {
      const result = spawnSync(command, {
        shell: true,
        cwd: this.projectRoot,
        encoding: 'utf-8'
      });

      const passed = result.status === 0;
      const output = (result.stdout || '') + (result.stderr || '');

      if (!passed) {
        const fingerprint = this._simpleHash(output.substring(0, 500));
        if (fingerprint === this.state.last_error_fingerprint) {
          this.state.consecutive_same_errors++;
        } else {
          this.state.consecutive_same_errors = 1;
          this.state.last_error_fingerprint = fingerprint;
        }
      } else {
        this.state.consecutive_same_errors = 0;
      }

      this._saveState();
      return [passed, output];
    } catch (err) {
      return [false, err.message];
    }
  }

  _simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    return String(Math.abs(hash));
  }

  shouldPivot() {
    if (this.state.consecutive_same_errors >= RalphSurgicalEngine.MAX_CONSECUTIVE_SAME_ERRORS) {
      return [true, 'Same error repeated. Architectural pivot required.'];
    }
    if (this.state.total_iterations >= RalphSurgicalEngine.MAX_ITERATIONS) {
      return [true, 'Max surgical iterations reached.'];
    }
    return [false, null];
  }
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const engine = new RalphSurgicalEngine();

  if (args[0] === 'reflect') {
    const [res, guidance] = engine.runReflection(args[1]);
    console.log(guidance);
  } else if (args[0] === 'test') {
    const [passed, out] = engine.runTestCommand(args.slice(1).join(' '));
    console.log(passed ? '✅ SUCCESS' : '❌ FAILED');
  } else if (args[0] === 'status') {
    console.log(JSON.stringify(engine.state, null, 2));
  }
}

module.exports = { RalphSurgicalEngine };
