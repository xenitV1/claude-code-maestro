#!/usr/bin/env node
/**
 * RALPH WIGGUM: Surgical Reflection Loop
 * =====================================
 * Implements the Generate → Reflect → Refine cycle for surgical code optimization.
 * 
 * Philosophy: "The first draft is never the final draft."
 */

const crypto = require('crypto');

// Issue Severity
const IssueSeverity = {
  NONE: 'none',
  MINOR: 'minor',
  MAJOR: 'major',
  CRITICAL: 'critical'
};

// Issue Categories
const IssueCategory = {
  EDGE_CASE_MISSING: 'edge_case_missing',
  INPUT_VALIDATION: 'input_validation',
  ERROR_HANDLING: 'error_handling',
  SECURITY_VULNERABILITY: 'security_vulnerability',
  PERFORMANCE: 'performance',
  CODE_STYLE: 'code_style',
  LOGIC_ERROR: 'logic_error',
  MISSING_TEST: 'missing_test',
  INCOMPLETE_IMPLEMENTATION: 'incomplete_implementation'
};

/**
 * ReflectionIssue - An issue found during code reflection.
 */
class ReflectionIssue {
  constructor(category, severity, description, location, suggestedFix) {
    this.category = category;
    this.severity = severity;
    this.description = description;
    this.location = location;
    this.suggestedFix = suggestedFix;
  }

  toDict() {
    return {
      category: this.category,
      severity: this.severity,
      description: this.description,
      location: this.location,
      suggested_fix: this.suggestedFix
    };
  }
}

/**
 * ReflectionResult - Result of a reflection cycle.
 */
class ReflectionResult {
  constructor(iteration, issues, overallSeverity, refinementNeeded, codeChecksum) {
    this.iteration = iteration;
    this.issues = issues;
    this.overallSeverity = overallSeverity;
    this.refinementNeeded = refinementNeeded;
    this.codeChecksum = codeChecksum;
    this.timestamp = new Date().toISOString();
  }

  toDict() {
    return {
      iteration: this.iteration,
      issues: this.issues.map(i => i.toDict()),
      overall_severity: this.overallSeverity,
      refinement_needed: this.refinementNeeded,
      code_checksum: this.codeChecksum,
      timestamp: this.timestamp
    };
  }
}

/**
 * ReflectionLoop - Implements the Generate → Reflect → Refine cycle.
 */
class ReflectionLoop {
  constructor(options = {}) {
    this.edgeCases = options.edgeCases || [];
    this.maxIterations = options.maxIterations || 50;
    this.autoFixMinor = options.autoFixMinor !== false;
    this.history = [];
    this.stagnationChecksums = [];
  }

  _computeChecksum(code) {
    return crypto.createHash('md5').update(code).digest('hex').substring(0, 12);
  }

  _detectStagnation(checksum) {
    if (this.stagnationChecksums.includes(checksum)) {
      return true;
    }
    this.stagnationChecksums.push(checksum);
    if (this.stagnationChecksums.length > 10) {
      this.stagnationChecksums.shift();
    }
    return false;
  }

  /**
   * Perform reflection on generated code.
   */
  reflect(code, context = {}) {
    const iteration = this.history.length + 1;
    const checksum = this._computeChecksum(code);

    // Check for stagnation
    if (this._detectStagnation(checksum)) {
      const result = new ReflectionResult(
        iteration,
        [new ReflectionIssue(
          IssueCategory.LOGIC_ERROR,
          IssueSeverity.CRITICAL,
          'STAGNATION DETECTED: Same code seen before. Need different approach.',
          'entire_codebase',
          'Try a completely different algorithm or ask for clarification.'
        )],
        IssueSeverity.CRITICAL,
        true,
        checksum
      );
      this.history.push(result);
      return result;
    }

    const issues = [];

    // Run static analysis checks
    issues.push(...this._checkEdgeCases(code));
    issues.push(...this._checkInputValidation(code));
    issues.push(...this._checkErrorHandling(code));
    issues.push(...this._checkSecurity(code));
    issues.push(...this._checkCompleteness(code));

    // Determine overall severity
    let overall = IssueSeverity.NONE;
    if (issues.some(i => i.severity === IssueSeverity.CRITICAL)) {
      overall = IssueSeverity.CRITICAL;
    } else if (issues.some(i => i.severity === IssueSeverity.MAJOR)) {
      overall = IssueSeverity.MAJOR;
    } else if (issues.some(i => i.severity === IssueSeverity.MINOR)) {
      overall = IssueSeverity.MINOR;
    }

    // Determine if refinement needed
    let refinementNeeded = [IssueSeverity.CRITICAL, IssueSeverity.MAJOR].includes(overall);
    if (this.autoFixMinor && overall === IssueSeverity.MINOR) {
      refinementNeeded = true;
    }

    const result = new ReflectionResult(iteration, issues, overall, refinementNeeded, checksum);
    this.history.push(result);
    return result;
  }

  _checkEdgeCases(code) {
    const issues = [];
    const codeLower = code.toLowerCase();

    const edgeCasePatterns = {
      empty: ['if not ', 'if len(', 'is None', '=== null', '!= null', '!== undefined'],
      null: ['is None', 'is not None', '=== null', '!== null', '!= null'],
      zero: ['== 0', '=== 0', '> 0', '< 0', '<= 0', '>= 0'],
      negative: ['< 0', '<= 0', 'is_negative', 'abs(', 'Math.abs'],
      overflow: ['MAX_', 'MIN_', 'overflow', 'MAX_SAFE', 'Number.MAX']
    };

    for (const [edgeType, patterns] of Object.entries(edgeCasePatterns)) {
      if (!patterns.some(p => codeLower.includes(p.toLowerCase()))) {
        if (['empty', 'null'].includes(edgeType)) {
          issues.push(new ReflectionIssue(
            IssueCategory.EDGE_CASE_MISSING,
            IssueSeverity.MAJOR,
            `No explicit handling for ${edgeType} values detected`,
            'input_parameters',
            `Add check: if (!value || value === null) return error`
          ));
        }
      }
    }

    return issues;
  }

  _checkInputValidation(code) {
    const issues = [];
    const codeLower = code.toLowerCase();

    // Check for file handling without validation
    if (codeLower.includes('file') || codeLower.includes('upload')) {
      if (!codeLower.includes('mimetype') && !codeLower.includes('content_type') && !codeLower.includes('content-type')) {
        issues.push(new ReflectionIssue(
          IssueCategory.INPUT_VALIDATION,
          IssueSeverity.CRITICAL,
          'File upload without MIME type validation',
          'file_handling',
          'Validate file.mimetype against allowed types list'
        ));
      }

      if (!codeLower.includes('size') && !codeLower.includes('length')) {
        issues.push(new ReflectionIssue(
          IssueCategory.INPUT_VALIDATION,
          IssueSeverity.MAJOR,
          'File upload without size validation',
          'file_handling',
          'Check file.size against MAX_FILE_SIZE constant'
        ));
      }
    }

    return issues;
  }

  _checkErrorHandling(code) {
    const issues = [];

    const hasTry = code.includes('try:') || code.includes('try {');
    const hasCatch = code.includes('except') || code.includes('catch');

    const asyncPatterns = ['await ', 'async ', '.then(', 'Promise'];
    const hasAsync = asyncPatterns.some(p => code.includes(p));

    if (hasAsync && !hasCatch) {
      issues.push(new ReflectionIssue(
        IssueCategory.ERROR_HANDLING,
        IssueSeverity.MAJOR,
        'Async operations without error handling',
        'async_code',
        'Wrap async calls in try-catch or add .catch() handler'
      ));
    }

    // Check for bare except (Python)
    if (code.includes('except:') && !code.includes('except Exception')) {
      issues.push(new ReflectionIssue(
        IssueCategory.ERROR_HANDLING,
        IssueSeverity.MINOR,
        'Bare except clause catches all exceptions including KeyboardInterrupt',
        'exception_handling',
        "Use 'except Exception as e:' to be more specific"
      ));
    }

    return issues;
  }

  _checkSecurity(code) {
    const issues = [];

    // SQL injection patterns
    const sqlPatterns = ['f"SELECT', "f'SELECT", '+ sql', '% sql', '.format(sql', '`SELECT'];
    for (const pattern of sqlPatterns) {
      if (code.toLowerCase().includes(pattern.toLowerCase())) {
        issues.push(new ReflectionIssue(
          IssueCategory.SECURITY_VULNERABILITY,
          IssueSeverity.CRITICAL,
          'Potential SQL injection: string formatting in SQL query',
          'database_query',
          'Use parameterized queries: cursor.execute(sql, [param])'
        ));
        break;
      }
    }

    // Path traversal
    if (code.includes('../') || code.includes('..\\')) {
      issues.push(new ReflectionIssue(
        IssueCategory.SECURITY_VULNERABILITY,
        IssueSeverity.CRITICAL,
        'Potential path traversal vulnerability',
        'file_path_handling',
        'Use path.basename() and validate against allowed directories'
      ));
    }

    // Hardcoded secrets
    const secretPatterns = ['password = "', 'api_key = "', 'secret = "', 'token = "', "password = '", "apiKey = '"];
    for (const pattern of secretPatterns) {
      if (code.toLowerCase().includes(pattern.toLowerCase())) {
        issues.push(new ReflectionIssue(
          IssueCategory.SECURITY_VULNERABILITY,
          IssueSeverity.CRITICAL,
          'Hardcoded secret detected',
          'credentials',
          "Use environment variables: process.env.SECRET_KEY"
        ));
        break;
      }
    }

    return issues;
  }

  _checkCompleteness(code) {
    const issues = [];

    // Check for TODO/FIXME
    const incompletePatterns = ['TODO', 'FIXME', 'XXX', 'HACK', 'pass  #', '...  #'];
    for (const pattern of incompletePatterns) {
      if (code.includes(pattern)) {
        issues.push(new ReflectionIssue(
          IssueCategory.INCOMPLETE_IMPLEMENTATION,
          IssueSeverity.MAJOR,
          `Incomplete implementation marker found: ${pattern}`,
          'code_body',
          'Complete the implementation before marking as done'
        ));
      }
    }

    // Check for NotImplementedError
    if (code.includes('NotImplementedError') || code.includes('raise NotImplemented') || code.includes('throw new Error("Not implemented")')) {
      issues.push(new ReflectionIssue(
        IssueCategory.INCOMPLETE_IMPLEMENTATION,
        IssueSeverity.CRITICAL,
        'NotImplementedError found - incomplete implementation',
        'function_body',
        'Implement the missing functionality'
      ));
    }

    return issues;
  }

  /**
   * Generate guidance for the agent to refine the code.
   */
  getRefinementGuidance(result) {
    if (!result.refinementNeeded) {
      return '✅ No refinement needed. Code passes all checks.';
    }

    let guidance = `
## 🔄 REFLECTION LOOP - Iteration ${result.iteration}

**Overall Severity:** ${result.overallSeverity.toUpperCase()}
**Issues Found:** ${result.issues.length}

### Issues to Address:

`;

    const critical = result.issues.filter(i => i.severity === IssueSeverity.CRITICAL);
    const major = result.issues.filter(i => i.severity === IssueSeverity.MAJOR);
    const minor = result.issues.filter(i => i.severity === IssueSeverity.MINOR);

    if (critical.length > 0) {
      guidance += '#### 🔴 CRITICAL (Must Fix):\n';
      critical.forEach((issue, i) => {
        guidance += `
${i + 1}. **${issue.category}** at \`${issue.location}\`
   - Problem: ${issue.description}
   - Fix: ${issue.suggestedFix}
`;
      });
    }

    if (major.length > 0) {
      guidance += '\n#### 🟠 MAJOR (Should Fix):\n';
      major.forEach((issue, i) => {
        guidance += `
${i + 1}. **${issue.category}** at \`${issue.location}\`
   - Problem: ${issue.description}
   - Fix: ${issue.suggestedFix}
`;
      });
    }

    if (minor.length > 0) {
      guidance += '\n#### 🟡 MINOR (Nice to Fix):\n';
      minor.forEach((issue, i) => {
        guidance += `${i + 1}. ${issue.description} → ${issue.suggestedFix}\n`;
      });
    }

    guidance += `
### Next Steps:
1. Address all CRITICAL issues first
2. Then fix MAJOR issues
3. Refine code and run reflection again
4. Repeat until no CRITICAL/MAJOR issues remain

**Iteration Limit:** ${this.maxIterations - result.iteration} remaining
`;
    return guidance;
  }

  getLoopStatus() {
    return {
      total_iterations: this.history.length,
      max_iterations: this.maxIterations,
      remaining: this.maxIterations - this.history.length,
      last_severity: this.history.length > 0 ? this.history[this.history.length - 1].overallSeverity : null,
      is_complete: this.history.length > 0 && !this.history[this.history.length - 1].refinementNeeded,
      history: this.history.map(r => r.toDict())
    };
  }

  reset() {
    this.history = [];
    this.stagnationChecksums = [];
  }
}

/**
 * ReflectionPromptGenerator - Generates prompts for the AI agent to self-reflect.
 */
class ReflectionPromptGenerator {
  static generateReflectPrompt(code, edgeCases) {
    const edgeCaseList = edgeCases.slice(0, 10).map(ec => `   - ${ec}`).join('\n');
    const codePreview = code.length > 2000 ? code.substring(0, 2000) + '...' : code;

    return `
## 🔄 SELF-REFLECTION CHECKPOINT

You have just generated the following code:

\`\`\`
${codePreview}
\`\`\`

### CRITICAL REVIEW REQUIRED

Before proceeding, answer these questions honestly:

1. **Edge Cases:** Does this code handle these scenarios?
${edgeCaseList}

2. **Input Validation:**
   - Are all inputs validated before use?
   - What happens with null/empty values?
   - Are there length/size limits?

3. **Error Handling:**
   - What happens when external calls fail?
   - Are errors logged with context?
   - Is there cleanup in failure cases?

4. **Security:**
   - Is user input sanitized?
   - Are database queries parameterized?
   - Are file paths validated?

5. **Completeness:**
   - Are there any TODO/FIXME markers?
   - Is every function fully implemented?
   - Are all edge cases covered?

### OUTPUT FORMAT

Respond with a JSON critique:
\`\`\`json
{
    "issues_found": [
        {"severity": "critical|major|minor", "description": "...", "fix": "..."}
    ],
    "overall_severity": "none|minor|major|critical",
    "needs_refinement": true|false
}
\`\`\`

If \`needs_refinement\` is true, provide the refined code in your next response.
`;
  }

  static generateRefinePrompt(issues) {
    const issueList = issues.map(i => `- [${i.severity.toUpperCase()}] ${i.description}: ${i.suggestedFix}`).join('\n');

    return `
## 🔧 CODE REFINEMENT REQUIRED

The following issues were found and must be fixed:

${issueList}

### INSTRUCTIONS:
1. Fix ALL critical issues - these are blockers
2. Fix major issues - these affect reliability
3. Consider minor issues if time permits
4. After fixing, the code will be reflected upon again

Provide the COMPLETE refined code, not just patches.
`;
  }
}

// CLI Interface
function main() {
  const sampleCode = `
def upload_pdf(file):
    # Save file to disk
    path = f"/uploads/{file.filename}"
    with open(path, 'wb') as f:
        f.write(file.read())
    return path
`;

  console.log('🔄 RALPH WIGGUM 2.0 - Reflection Loop Demo\n');
  console.log('Sample code:');
  console.log(sampleCode);
  console.log('\n' + '='.repeat(60) + '\n');

  const loop = new ReflectionLoop();
  const result = loop.reflect(sampleCode);

  console.log(loop.getRefinementGuidance(result));
}

// Export for module use
module.exports = {
  ReflectionLoop,
  ReflectionIssue,
  ReflectionResult,
  ReflectionPromptGenerator,
  IssueSeverity,
  IssueCategory
};

if (require.main === module) {
  main();
}
