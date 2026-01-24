/**
 * Ralph Wiggum State Manager
 *
 * Manages Ralph Wiggum iteration state for autonomous QA mode.
 * This module handles:
 * - Creating and updating .maestro/ralph.state
 * - Tracking iteration counts
 * - Managing completion signals
 *
 * @module hooks/lib/ralph
 */

const fs = require('fs');
const path = require('path');

const {
  findProjectRoot,
  getMaestroDir,
  logDebug
} = require('./utils');

const LOG_PREFIX = '[RALPH]';

/**
 * Get the Ralph state file path
 * @returns {string} Full path to ralph.state
 */
function getStateFilePath() {
  const projectRoot = findProjectRoot();
  const maestroDir = getMaestroDir(projectRoot);
  return path.join(maestroDir, 'ralph.state');
}

/**
 * Get the Ralph completion file path
 * @returns {string} Full path to ralph.complete
 */
function getCompleteFilePath() {
  const projectRoot = findProjectRoot();
  const maestroDir = getMaestroDir(projectRoot);
  return path.join(maestroDir, 'ralph.complete');
}

/**
 * Get the Ralph active sentinel file path
 * @returns {string} Full path to ralph.active
 */
function getActiveFilePath() {
  const projectRoot = findProjectRoot();
  const maestroDir = getMaestroDir(projectRoot);
  return path.join(maestroDir, 'ralph.active');
}

/**
 * Ralph state structure
 * @typedef {Object} RalphState
 * @property {number} max - Maximum iterations
 * @property {number} current - Current iteration count
 * @property {string} mode - Ralph mode (all/debug/feature)
 * @property {string[]} features - Active features
 * @property {number} startedAt - Timestamp when started
 * @property {number} lastUpdate - Timestamp of last update
 */

/**
 * Read Ralph state from file
 * @returns {RalphState|null} State object or null if not exists
 */
function readState() {
  const statePath = getStateFilePath();
  if (!fs.existsSync(statePath)) {
    return null;
  }

  try {
    const content = fs.readFileSync(statePath, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    logDebug(LOG_PREFIX, `Error reading state: ${err.message}`);
    return null;
  }
}

/**
 * Write Ralph state to file
 * @param {RalphState} state - State to write
 */
function writeState(state) {
  const statePath = getStateFilePath();
  const maestroDir = path.dirname(statePath);

  // Ensure .maestro directory exists
  if (!fs.existsSync(maestroDir)) {
    fs.mkdirSync(maestroDir, { recursive: true });
  }

  state.lastUpdate = Date.now();
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
  logDebug(LOG_PREFIX, `State updated: ${state.current}/${state.max}`);
}

/**
 * Initialize Ralph state
 * @param {number} maxIterations - Maximum iterations
 * @param {string} mode - Ralph mode (all/debug/feature)
 * @param {string[]} features - Active features
 * @returns {RalphState} Created state
 */
function initializeState(maxIterations, mode = 'all', features = []) {
  const state = {
    max: maxIterations,
    current: 0,
    mode: mode,
    features: features,
    startedAt: Date.now(),
    lastUpdate: Date.now()
  };

  writeState(state);

  // Create active sentinel
  const activePath = getActiveFilePath();
  fs.writeFileSync(activePath, '');

  logDebug(LOG_PREFIX, `State initialized: ${maxIterations} iterations, mode=${mode}`);
  return state;
}

/**
 * Increment iteration counter
 * @returns {RalphState|null} Updated state or null if not active
 */
function incrementIteration() {
  const state = readState();
  if (!state) {
    return null;
  }

  state.current++;
  writeState(state);
  return state;
}

/**
 * Check if Ralph is currently active
 * @returns {boolean} True if Ralph is active
 */
function isActive() {
  const state = readState();
  const activePath = getActiveFilePath();
  return state !== null && fs.existsSync(activePath);
}

/**
 * Check if Ralph should continue iterating
 * @returns {boolean} True if should continue
 */
function shouldContinue() {
  const state = readState();
  if (!state) {
    return false;
  }

  // Check if completed
  const completePath = getCompleteFilePath();
  if (fs.existsSync(completePath)) {
    logDebug(LOG_PREFIX, 'Completion signal detected');
    return false;
  }

  // Check if max iterations reached
  return state.current < state.max;
}

/**
 * Check if exit should be blocked
 * @returns {Object} Block decision
 */
function getBlockDecision() {
  if (!isActive()) {
    return { block: false, reason: 'Ralph not active' };
  }

  const state = readState();
  if (!state) {
    return { block: false, reason: 'No state found' };
  }

  // Check completion signal
  const completePath = getCompleteFilePath();
  if (fs.existsSync(completePath)) {
    return { block: false, reason: 'Completion signal detected', completed: true };
  }

  // Increment iteration
  const newState = incrementIteration();
  if (!newState) {
    return { block: false, reason: 'Failed to increment' };
  }

  // Check if should continue
  if (newState.current <= newState.max) {
    return {
      block: true,
      reason: `Iteration ${newState.current}/${newState.max}`,
      current: newState.current,
      max: newState.max
    };
  }

  return { block: false, reason: 'Max iterations reached', completed: true };
}

/**
 * Mark Ralph as complete
 */
function markComplete() {
  const completePath = getCompleteFilePath();
  const maestroDir = path.dirname(completePath);

  if (!fs.existsSync(maestroDir)) {
    fs.mkdirSync(maestroDir, { recursive: true });
  }

  fs.writeFileSync(completePath, 'completed');
  logDebug(LOG_PREFIX, 'Marked as complete');
}

/**
 * Clear Ralph state (cleanup)
 */
function clearState() {
  const statePath = getStateFilePath();
  const activePath = getActiveFilePath();
  const completePath = getCompleteFilePath();

  if (fs.existsSync(statePath)) {
    fs.unlinkSync(statePath);
  }
  if (fs.existsSync(activePath)) {
    fs.unlinkSync(activePath);
  }
  if (fs.existsSync(completePath)) {
    fs.unlinkSync(completePath);
  }

  logDebug(LOG_PREFIX, 'State cleared');
}

/**
 * Get current iteration status
 * @returns {Object|null} Status object or null
 */
function getStatus() {
  const state = readState();
  if (!state) {
    return null;
  }

  const completePath = getCompleteFilePath();
  const isComplete = fs.existsSync(completePath);

  return {
    current: state.current,
    max: state.max,
    mode: state.mode,
    features: state.features,
    isComplete: isComplete,
    startedAt: state.startedAt,
    lastUpdate: state.lastUpdate
  };
}

module.exports = {
  getStateFilePath,
  getCompleteFilePath,
  getActiveFilePath,
  readState,
  writeState,
  initializeState,
  incrementIteration,
  isActive,
  shouldContinue,
  getBlockDecision,
  markComplete,
  clearState,
  getStatus
};
