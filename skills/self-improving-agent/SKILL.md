---
name: self-improving-agent
description: Captures learnings, errors, and corrections to enable continuous improvement. Use when (1) A command or operation fails unexpectedly, (2) User corrects Clau... (3) You want to document a process for future reference, (4) You encounter a new tool or workflow that should be remembered.
---

# Self-Improving Agent

This skill enables continuous learning and improvement by capturing:
- Command failures and their solutions
- User corrections and feedback
- New processes and workflows
- Tool usage patterns

## When to Use

1. **After a command fails** - Document the error and solution
2. **When user corrects you** - Capture the correction for future reference
3. **After learning something new** - Document the process
4. **When encountering a new tool** - Record how to use it

## Workflow

### 1. Capture the Learning

When something notable happens:
- What was the situation?
- What was the problem/solution?
- What can be improved?

### 2. Document in MEMORY.md

Add to the appropriate section:
```markdown
## Learning: [Topic]
**Date:** YYYY-MM-DD
**Context:** [What happened]
**Solution:** [How it was solved]
**Reference:** [Link to file/line]
```

### 3. Update Daily Log

Record in `memory/YYYY-MM-DD.md`:
```markdown
### Learning: [Brief description]
- Discovered: [What was learned]
- Applied: [How it was used]
- Result: [Outcome]
```

### 4. Create Skill if Repeatable

If this is a repeatable process:
- Create a new skill in `/root/.openclaw/workspace/skills/`
- Include scripts, references, and assets
- Document in SKILL.md

## Integration with Existing Systems

### Auto-Learning Capture
The system already runs `auto-learning-capture.sh` which:
- Documents daily learnings
- Updates MEMORY.md
- Suggests skill creation

### Self-Improvement Skill
The existing `self-improvement` skill in workspace:
- Runs at end of sessions
- Captures accomplishments
- Documents mistakes
- Creates skills from knowledge

## Best Practices

1. **Be specific** - Include exact commands, errors, and solutions
2. **Link to context** - Reference files, lines, and commits
3. **Tag learnings** - Use categories like `[BUG]`, `[WORKFLOW]`, `[TOOL]`
4. **Review regularly** - Periodically review MEMORY.md for patterns

## Example Learnings

### Example 1: Command Failure
```markdown
## Learning: Supabase RLS with Service Key
**Date:** 2026-03-04
**Context:** Anon key blocked by RLS, couldn't read data
**Solution:** Use service_role key to bypass RLS
**Code:** 
```javascript
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'; // service_role
```
**Reference:** memory/mission-control-v2-documentation.md
```

### Example 2: User Correction
```markdown
## Learning: Mission Control Data Sources
**Date:** 2026-03-04
**Context:** User corrected that radio stats are in nielsen_weekly_metrics, not agenda_items
**Solution:** Updated API calls to use correct table
**Files Changed:** mission-control-gh-pages/index.html
```

## Related Skills

- `self-improvement` - Automatic session-end learning capture
- `skill-creator` - Create new skills from knowledge
