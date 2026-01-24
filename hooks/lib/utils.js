/**
 * Maestro Hook Utilities
 * Cross-platform utility functions for all Maestro hooks
 * 
 * @module hooks/lib/utils
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Find the project root directory.
 * 
 * Priority order:
 * 1. CLAUDE_PROJECT_DIR environment variable (set by Claude Code)
 * 2. CLAUDE_WORKING_DIR environment variable (fallback)
 * 3. Search upward from current directory for root markers
 * 
 * @param {string} [startDir] - Starting directory for search
 * @returns {string} Project root path
 */
function findProjectRoot(startDir = null) {
  // Priority 1: Use CLAUDE_PROJECT_DIR if set by Claude Code
  const claudeProjectDir = process.env.CLAUDE_PROJECT_DIR;
  if (claudeProjectDir && fs.existsSync(claudeProjectDir)) {
    logDebug('[UTILS]', `Project root from CLAUDE_PROJECT_DIR: ${claudeProjectDir}`);
    return claudeProjectDir;
  }

  // Priority 2: Use CLAUDE_WORKING_DIR if set
  const claudeWorkingDir = process.env.CLAUDE_WORKING_DIR;
  if (claudeWorkingDir && fs.existsSync(claudeWorkingDir)) {
    logDebug('[UTILS]', `Project root from CLAUDE_WORKING_DIR: ${claudeWorkingDir}`);
    return claudeWorkingDir;
  }

  // Priority 3: Search upward from startDir
  let current = path.resolve(startDir || process.cwd());
  const rootMarkers = ['.git', 'package.json', '.claude', 'pyproject.toml', 'Cargo.toml'];

  // Walk up the directory tree
  while (true) {
    for (const marker of rootMarkers) {
      const markerPath = path.join(current, marker);
      if (fs.existsSync(markerPath)) {
        return current;
      }
    }

    const parent = path.dirname(current);
    if (parent === current) {
      // Reached filesystem root
      break;
    }
    current = parent;
  }

  // Fallback: return original directory
  return startDir || process.cwd();
}

/**
 * Get the .maestro directory path.
 * Always in project root, never in subdirectories.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {string} .maestro directory path
 */
function getMaestroDir(projectRoot = null) {
  const root = projectRoot || findProjectRoot();
  return path.join(root, '.maestro');
}

/**
 * Ensure .maestro directory exists in project root.
 * 
 * @param {string} [projectRoot] - Project root path
 * @returns {string} .maestro directory path
 */
function ensureMaestroDir(projectRoot = null) {
  const maestroDir = getMaestroDir(projectRoot);
  if (!fs.existsSync(maestroDir)) {
    fs.mkdirSync(maestroDir, { recursive: true });
  }
  return maestroDir;
}

/**
 * Get the plugin root directory.
 * 
 * @returns {string} Plugin root path
 */
function getPluginRoot() {
  return process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, '..', '..');
}

/**
 * Get the Claude projects directory (cross-platform).
 * 
 * @returns {string} Claude projects directory path
 */
function getClaudeProjectsDir() {
  if (process.platform === 'win32') {
    // Windows: Claude Code uses USERPROFILE\.claude\projects (not APPDATA)
    // Check both locations for compatibility
    const userProfile = process.env.USERPROFILE || os.homedir();
    const userProfilePath = path.join(userProfile, '.claude', 'projects');
    if (fs.existsSync(userProfilePath)) {
      return userProfilePath;
    }
    // Fallback to APPDATA for older installations
    const appData = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
    return path.join(appData, '.claude', 'projects');
  }
  // macOS/Linux: Use home directory
  return path.join(os.homedir(), '.claude', 'projects');
}

/**
 * Normalize a project path for Claude's folder naming convention.
 * Claude Code normalizes paths: C:\Users\foo -> C--Users-foo
 * 
 * @param {string} rawPath - Raw file system path
 * @returns {string} Normalized path string
 */
function normalizeProjectPath(rawPath) {
  if (process.platform === 'win32' && rawPath.includes(':')) {
    let [drive, rest] = rawPath.split(':');
    // Force drive letter to uppercase for consistent matching
    drive = drive.toUpperCase();
    // Remove leading slashes and replace all slashes/dots with dashes
    const normalized = rest.replace(/^[\\/]+/, '').replace(/[\\/]/g, '-').replace(/\./g, '-');
    return `${drive}--${normalized}`;
  }
  return rawPath.replace(/[\\/]/g, '-').replace(/\./g, '-');
}

/**
 * Log message to stderr (for debugging).
 * Only logs when MAESTRO_DEBUG=1
 * 
 * @param {string} prefix - Log prefix (e.g., '[BRAIN]')
 * @param {string} msg - Message to log
 */
function logDebug(prefix, msg) {
  if (process.env.MAESTRO_DEBUG === '1') {
    process.stderr.write(`${prefix} ${msg}\n`);
  }
}

/**
 * Read a file safely with size limit.
 * 
 * @param {string} filePath - Path to file
 * @param {number} [maxSize=100000] - Maximum file size in bytes
 * @returns {string|null} File contents or null if failed/too large
 */
function readFileSafe(filePath, maxSize = 100000) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const stats = fs.statSync(filePath);
    if (stats.size > maxSize) {
      logDebug('[UTILS]', `File too large, skipping: ${filePath}`);
      return null;
    }
    return fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    logDebug('[UTILS]', `Error reading ${filePath}: ${err.message}`);
    return null;
  }
}

/**
 * Remove ANSI escape codes from text.
 * 
 * @param {string} text - Text with potential ANSI codes
 * @returns {string} Clean text
 */
function cleanAnsi(text) {
  // ANSI escape code pattern
  return text.replace(/\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])/g, '');
}

/**
 * Get current timestamp in ISO format.
 * 
 * @returns {string} Timestamp string
 */
function getTimestamp() {
  return new Date().toISOString().replace('T', ' ').substring(0, 19);
}

/**
 * Get current time in HH:MM:SS format.
 * 
 * @returns {string} Time string
 */
function getTimeOnly() {
  return new Date().toISOString().substring(11, 19);
}

/**
 * Read JSON from stdin (for hook input).
 * 
 * @returns {Promise<object>} Parsed JSON object
 */
function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';

    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });

    process.stdin.on('end', () => {
      if (!data.trim()) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(data));
      } catch (err) {
        logDebug('[UTILS]', `JSON parse error: ${err.message}`);
        resolve({});
      }
    });

    process.stdin.on('error', (err) => {
      logDebug('[UTILS]', `stdin error: ${err.message}`);
      resolve({});
    });

    // Handle case where stdin is already closed or empty
    if (process.stdin.readableEnded) {
      resolve({});
    }
  });
}

/**
 * Output JSON to stdout (for hook output).
 * 
 * @param {object} data - Data to output
 */
function outputJson(data) {
  console.log(JSON.stringify(data));
}

/**
 * Smart truncation - keeps beginning and end for context.
 * 
 * @param {string} text - Text to truncate
 * @param {number} maxLen - Maximum length
 * @returns {string} Truncated text
 */
function truncateSmart(text, maxLen) {
  if (text.length <= maxLen) {
    return text;
  }

  // Keep 60% from start, 40% from end
  const startLen = Math.floor(maxLen * 0.6);
  const endLen = maxLen - startLen - 20; // Reserve space for separator

  return text.substring(0, startLen) + '\n...[truncated]...\n' + text.substring(text.length - endLen);
}

/**
 * Calculate MD5 hash of a string (simple implementation for change detection).
 * 
 * @param {string} content - Content to hash
 * @returns {string} Hash string
 */
function simpleHash(content) {
  const crypto = require('crypto');
  return crypto.createHash('md5').update(content).digest('hex');
}

/**
 * Get file hash for change detection.
 * 
 * @param {string} filePath - Path to file
 * @returns {string|null} File hash or null if failed
 */
function getFileHash(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const content = fs.readFileSync(filePath);
    return simpleHash(content.toString());
  } catch (err) {
    return null;
  }
}

const { execSync } = require('child_process');

/**
 * Check if the current project is a Git repository.
 * 
 * @param {string} projectRoot - Project root path
 * @returns {boolean} True if Git repo
 */
function isGitProject(projectRoot) {
  try {
    return fs.existsSync(path.join(projectRoot, '.git'));
  } catch (err) {
    return false;
  }
}

/**
 * Get changed files using Git (much faster than recursive scan).
 * 
 * @param {string} projectRoot - Project root path
 * @returns {string[]} Array of relative file paths
 */
function getGitDirtyFiles(projectRoot) {
  try {
    // --porcelain=v1 gives a predictable, machine-readable output
    const output = execSync('git status --porcelain=v1', { cwd: projectRoot, encoding: 'utf-8' });
    return output.split('\n')
      .map(line => line.substring(3).trim())
      .filter(line => line.length > 0);
  } catch (err) {
    logDebug('[UTILS]', `Git status failed: ${err.message}`);
    return [];
  }
}

/**
 * Save state to .maestro directory.
 * 
 * @param {string} name - State file name (without extension)
 * @param {object} data - Data to save
 * @param {string} [projectRoot] - Project root path
 */
function saveState(name, data, projectRoot = null) {
  try {
    const maestroDir = ensureMaestroDir(projectRoot);
    const stateFile = path.join(maestroDir, `${name}.state`);
    fs.writeFileSync(stateFile, JSON.stringify(data, null, 2), 'utf-8');
  } catch (err) {
    logDebug('[UTILS]', `Error saving state ${name}: ${err.message}`);
  }
}

/**
 * Load state from .maestro directory.
 * 
 * @param {string} name - State file name
 * @param {string} [projectRoot] - Project root path
 * @returns {object|null} State data or null
 */
function loadState(name, projectRoot = null) {
  try {
    const maestroDir = getMaestroDir(projectRoot);
    const stateFile = path.join(maestroDir, `${name}.state`);
    if (fs.existsSync(stateFile)) {
      return JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
    }
  } catch (err) {
    logDebug('[UTILS]', `Error loading state ${name}: ${err.message}`);
  }
  return null;
}

/**
 * Check if a tool is read-only (unlikely to change project state).
 * 
 * @param {string} toolName - Name of the tool
 * @returns {boolean} True if read-only
 */
function isReadOnlyTool(toolName) {
  const readOnlyTools = [
    'view_file', 'Read', 'read_file',
    'list_dir', 'LS', 'ls', 'dir',
    'grep_search', 'Grep', 'search',
    'find_by_name', 'Glob', 'glob',
    'read_url_content', 'read_browser_page',
    'list_resources', 'read_resource',
    'command_status', 'read_terminal',
    'AskUserQuestion', 'ask'
  ];
  return readOnlyTools.includes(toolName);
}

module.exports = {
  findProjectRoot,
  getMaestroDir,
  ensureMaestroDir,
  getPluginRoot,
  getClaudeProjectsDir,
  isGitProject,
  getGitDirtyFiles,
  saveState,
  loadState,
  isReadOnlyTool,
  normalizeProjectPath,
  logDebug,
  readFileSafe,
  cleanAnsi,
  getTimestamp,
  getTimeOnly,
  readStdin,
  outputJson,
  truncateSmart,
  simpleHash,
  getFileHash
};
